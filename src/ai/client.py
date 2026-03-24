"""Async HTTP client wrapper for the GitHub Models API with retry logic."""

from __future__ import annotations

import asyncio
import logging
import random
import time

import httpx

from src.exceptions import AIRateLimitError, AIServiceUnavailableError

logger = logging.getLogger(__name__)


class GitHubModelsClient:
    """Async HTTP client for the GitHub Models chat completions API.

    Implements exponential backoff with jitter for rate-limit and
    transient-error handling.
    """

    def __init__(
        self,
        endpoint: str,
        api_key: str,
        model: str = "gpt-4o",
        timeout: int = 30,
        max_retries: int = 3,
        initial_backoff: float = 1.0,
        max_backoff: float = 30.0,
        jitter_ms: int = 500,
    ) -> None:
        self._endpoint = endpoint.rstrip("/")
        self._api_key = api_key
        self._model = model
        self._timeout = timeout
        self._max_retries = max_retries
        self._initial_backoff = initial_backoff
        self._max_backoff = max_backoff
        self._jitter_ms = jitter_ms
        self._client = httpx.AsyncClient(timeout=timeout)

    async def generate(
        self,
        messages: list[dict],
        max_tokens: int = 2000,
        temperature: float = 0.7,
    ) -> str:
        """Send a chat completion request and return the text content.

        Retries on HTTP 429 and 5xx responses with exponential backoff.

        Args:
            messages: Chat messages (system + user).
            max_tokens: Maximum tokens in the response.
            temperature: Sampling temperature.

        Returns:
            The generated text from the AI model.

        Raises:
            AIRateLimitError: If 429 persists after all retries.
            AIServiceUnavailableError: If server/network errors persist.
        """
        url = f"{self._endpoint}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self._model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }

        last_error: Exception | None = None

        for attempt in range(self._max_retries + 1):
            try:
                logger.debug(
                    "AI request attempt %d/%d to %s",
                    attempt + 1,
                    self._max_retries + 1,
                    url,
                )
                start = time.monotonic()
                response = await self._client.post(
                    url, json=payload, headers=headers
                )
                elapsed = time.monotonic() - start
                logger.debug("AI response: status=%d latency=%.2fs", response.status_code, elapsed)

                if response.status_code == 200:
                    data = response.json()
                    content = data["choices"][0]["message"]["content"]
                    logger.info(
                        "AI generation success: model=%s tokens_approx=%d latency=%.2fs",
                        self._model,
                        max_tokens,
                        elapsed,
                    )
                    return content

                if response.status_code == 429:
                    last_error = AIRateLimitError(
                        details=f"HTTP 429 on attempt {attempt + 1}"
                    )
                    logger.warning(
                        "Rate limited (429) on attempt %d/%d",
                        attempt + 1,
                        self._max_retries + 1,
                    )
                elif response.status_code >= 500:
                    last_error = AIServiceUnavailableError(
                        details=f"HTTP {response.status_code} on attempt {attempt + 1}"
                    )
                    logger.warning(
                        "Server error (%d) on attempt %d/%d",
                        response.status_code,
                        attempt + 1,
                        self._max_retries + 1,
                    )
                else:
                    # Non-retryable client error
                    raise AIServiceUnavailableError(
                        details=f"Unexpected HTTP {response.status_code}: {response.text[:200]}"
                    )

            except (httpx.ConnectError, httpx.TimeoutException) as exc:
                last_error = AIServiceUnavailableError(
                    details=f"Network error on attempt {attempt + 1}: {type(exc).__name__}"
                )
                logger.warning(
                    "Network error (%s) on attempt %d/%d",
                    type(exc).__name__,
                    attempt + 1,
                    self._max_retries + 1,
                )

            # Back off before next attempt (skip if this was the last attempt)
            if attempt < self._max_retries:
                await self._backoff(attempt)

        # All retries exhausted
        if last_error is not None:
            raise last_error
        raise AIServiceUnavailableError(details="All retries exhausted")

    async def _backoff(self, attempt: int) -> None:
        """Sleep with exponential backoff and jitter."""
        delay = min(self._initial_backoff * (2 ** attempt), self._max_backoff)
        jitter = random.uniform(-self._jitter_ms / 1000, self._jitter_ms / 1000)
        sleep_time = max(0, delay + jitter)
        logger.debug("Backing off %.2fs before retry (attempt %d)", sleep_time, attempt + 1)
        await asyncio.sleep(sleep_time)

    async def close(self) -> None:
        """Close the underlying HTTP client."""
        await self._client.aclose()
