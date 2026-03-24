"""Tests for GitHubModelsClient — AI HTTP wrapper with retry logic.

Covers: BRD-AI-004, BRD-AI-006, BRD-AI-009, BRD-NFR-005, TASK-012, TASK-019
"""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import httpx
import pytest
import respx

from src.ai.client import GitHubModelsClient
from src.exceptions import AIRateLimitError, AIServiceUnavailableError

pytestmark = pytest.mark.asyncio

ENDPOINT = "https://models.test.ai/inference"
API_KEY = "test-key"
MESSAGES = [
    {"role": "system", "content": "You are a test."},
    {"role": "user", "content": "Hello"},
]
SUCCESS_RESPONSE = {
    "choices": [{"message": {"content": "Generated content here"}}]
}


def _make_client(**kwargs):
    """Create a GitHubModelsClient with test defaults."""
    defaults = {
        "endpoint": ENDPOINT,
        "api_key": API_KEY,
        "model": "gpt-4o",
        "timeout": 5,
        "max_retries": 2,
        "initial_backoff": 0.01,
        "max_backoff": 0.1,
        "jitter_ms": 1,
    }
    defaults.update(kwargs)
    return GitHubModelsClient(**defaults)


class TestGenerateSuccess:
    """Successful generation tests."""

    @respx.mock
    async def test_successful_generation(self):
        """Verify successful response extracts content. [TASK-012] [BRD-AI-001]"""
        client = _make_client()
        respx.post(f"{ENDPOINT}/chat/completions").mock(
            return_value=httpx.Response(200, json=SUCCESS_RESPONSE)
        )
        result = await client.generate(MESSAGES)
        assert result == "Generated content here"
        await client.close()

    @respx.mock
    async def test_sends_correct_headers(self):
        """Verify request includes Bearer token. [TASK-012] [BRD-AI-001]"""
        client = _make_client()
        route = respx.post(f"{ENDPOINT}/chat/completions").mock(
            return_value=httpx.Response(200, json=SUCCESS_RESPONSE)
        )
        await client.generate(MESSAGES)
        request = route.calls[0].request
        assert request.headers["Authorization"] == f"Bearer {API_KEY}"
        assert request.headers["Content-Type"] == "application/json"
        await client.close()

    @respx.mock
    async def test_sends_correct_payload(self):
        """Verify request payload structure. [TASK-012] [BRD-AI-001]"""
        client = _make_client()
        route = respx.post(f"{ENDPOINT}/chat/completions").mock(
            return_value=httpx.Response(200, json=SUCCESS_RESPONSE)
        )
        await client.generate(MESSAGES, max_tokens=1500, temperature=0.5)
        import json
        body = json.loads(route.calls[0].request.content)
        assert body["model"] == "gpt-4o"
        assert body["messages"] == MESSAGES
        assert body["max_tokens"] == 1500
        assert body["temperature"] == 0.5
        await client.close()


class TestRetryOn429:
    """Rate limit (429) retry tests."""

    @respx.mock
    async def test_retries_on_429_then_succeeds(self):
        """Verify retry on 429, then success. [TASK-019] [BRD-AI-004]"""
        client = _make_client()
        route = respx.post(f"{ENDPOINT}/chat/completions").mock(
            side_effect=[
                httpx.Response(429, text="rate limited"),
                httpx.Response(200, json=SUCCESS_RESPONSE),
            ]
        )
        result = await client.generate(MESSAGES)
        assert result == "Generated content here"
        assert route.call_count == 2
        await client.close()

    @respx.mock
    async def test_raises_rate_limit_after_all_retries(self):
        """Verify AIRateLimitError after all retries exhausted. [TASK-019] [BRD-AI-004]"""
        client = _make_client(max_retries=2)
        respx.post(f"{ENDPOINT}/chat/completions").mock(
            return_value=httpx.Response(429, text="rate limited")
        )
        with pytest.raises(AIRateLimitError):
            await client.generate(MESSAGES)
        await client.close()


class TestRetryOn5xx:
    """Server error (5xx) retry tests."""

    @respx.mock
    async def test_retries_on_500_then_succeeds(self):
        """Verify retry on 500, then success. [TASK-019] [BRD-AI-006]"""
        client = _make_client()
        route = respx.post(f"{ENDPOINT}/chat/completions").mock(
            side_effect=[
                httpx.Response(500, text="server error"),
                httpx.Response(200, json=SUCCESS_RESPONSE),
            ]
        )
        result = await client.generate(MESSAGES)
        assert result == "Generated content here"
        assert route.call_count == 2
        await client.close()

    @respx.mock
    async def test_raises_unavailable_after_all_retries(self):
        """Verify AIServiceUnavailableError after all retries. [TASK-019] [BRD-AI-006]"""
        client = _make_client(max_retries=2)
        respx.post(f"{ENDPOINT}/chat/completions").mock(
            return_value=httpx.Response(503, text="unavailable")
        )
        with pytest.raises(AIServiceUnavailableError):
            await client.generate(MESSAGES)
        await client.close()


class TestRetryOnNetworkError:
    """Network error retry tests."""

    @respx.mock
    async def test_retries_on_connect_error(self):
        """Verify retry on ConnectError. [TASK-019] [BRD-AI-009]"""
        client = _make_client(max_retries=2)
        respx.post(f"{ENDPOINT}/chat/completions").mock(
            side_effect=[
                httpx.ConnectError("Connection refused"),
                httpx.Response(200, json=SUCCESS_RESPONSE),
            ]
        )
        result = await client.generate(MESSAGES)
        assert result == "Generated content here"
        await client.close()

    @respx.mock
    async def test_retries_on_timeout(self):
        """Verify retry on TimeoutException. [TASK-019] [BRD-AI-009]"""
        client = _make_client(max_retries=2)
        respx.post(f"{ENDPOINT}/chat/completions").mock(
            side_effect=[
                httpx.TimeoutException("timed out"),
                httpx.Response(200, json=SUCCESS_RESPONSE),
            ]
        )
        result = await client.generate(MESSAGES)
        assert result == "Generated content here"
        await client.close()

    @respx.mock
    async def test_raises_after_all_network_retries(self):
        """Verify error after all network retries exhausted. [TASK-019] [BRD-NFR-005]"""
        client = _make_client(max_retries=1)
        respx.post(f"{ENDPOINT}/chat/completions").mock(
            side_effect=httpx.ConnectError("Connection refused")
        )
        with pytest.raises(AIServiceUnavailableError):
            await client.generate(MESSAGES)
        await client.close()


class TestNonRetryableErrors:
    """Non-retryable error tests."""

    @respx.mock
    async def test_non_retryable_400_raises_immediately(self):
        """Verify 400 errors raise immediately without retry. [TASK-019] [BRD-AI-006]"""
        client = _make_client()
        route = respx.post(f"{ENDPOINT}/chat/completions").mock(
            return_value=httpx.Response(400, text="bad request")
        )
        with pytest.raises(AIServiceUnavailableError):
            await client.generate(MESSAGES)
        assert route.call_count == 1
        await client.close()


class TestBackoff:
    """Exponential backoff tests."""

    @respx.mock
    async def test_backoff_is_called_between_retries(self):
        """Verify backoff is called between retry attempts. [TASK-019] [BRD-AI-004]"""
        client = _make_client(max_retries=2)
        respx.post(f"{ENDPOINT}/chat/completions").mock(
            side_effect=[
                httpx.Response(429, text="rate limited"),
                httpx.Response(429, text="rate limited"),
                httpx.Response(429, text="rate limited"),
            ]
        )
        with patch.object(client, "_backoff", new_callable=AsyncMock) as mock_backoff:
            with pytest.raises(AIRateLimitError):
                await client.generate(MESSAGES)
            assert mock_backoff.await_count == 2
        await client.close()
