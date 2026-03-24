# Task: Implement GitHubModelsClient (Async HTTP Wrapper)

| Field        | Value                |
|--------------|----------------------|
| **Task ID**  | TASK-012             |
| **Story**    | STORY-008            |
| **Status**   | To Do                |
| **Assignee** | develop-agent        |
| **Estimate** | 3h                   |

## Description

Create the `GitHubModelsClient` class that wraps all communication with the GitHub Models API via `httpx.AsyncClient`. This client handles sending chat completion requests to GPT-4o, sets the 30-second timeout, and provides the foundation for retry logic (added in TASK-019).

## Implementation Details

**Files to create/modify:**
- `src/ai/client.py` — GitHubModelsClient class

**Approach:**
```python
import httpx
import logging

logger = logging.getLogger("ai.client")

class GitHubModelsClient:
    def __init__(self, api_key: str, endpoint: str, model: str = "gpt-4o", timeout: int = 30):
        self.api_key = api_key
        self.endpoint = endpoint
        self.model = model
        self.timeout = timeout
        self._client = httpx.AsyncClient(
            timeout=httpx.Timeout(timeout),
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }
        )

    async def generate(self, messages: list[dict], max_tokens: int = 2000, temperature: float = 0.7) -> str:
        """Send a chat completion request to the GitHub Models API.

        Args:
            messages: List of chat messages [{role, content}]
            max_tokens: Maximum tokens in the response
            temperature: Sampling temperature

        Returns:
            The text content of the AI response

        Raises:
            AIServiceUnavailableError: If the API is unreachable or returns 5xx
            AIRateLimitError: If rate limited after all retries
        """
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }

        response = await self._client.post(
            f"{self.endpoint}/chat/completions",
            json=payload,
        )

        if response.status_code == 429:
            raise AIRateLimitError(...)
        if response.status_code >= 500:
            raise AIServiceUnavailableError(...)
        response.raise_for_status()

        data = response.json()
        content = data["choices"][0]["message"]["content"]

        # Log at DEBUG level (never log API key)
        logger.debug("AI response: model=%s tokens=%s latency=%.1fms",
                     self.model, data.get("usage", {}), ...)

        return content

    async def close(self):
        await self._client.aclose()
```

## API Changes

N/A — internal service class.

## Data Model Changes

N/A

## Acceptance Criteria

- [ ] GitHubModelsClient sends POST requests to {endpoint}/chat/completions
- [ ] Authorization header uses Bearer token with GITHUB_MODELS_API_KEY
- [ ] Request timeout is set to configured value (default 30s)
- [ ] Successful response extracts text from choices[0].message.content
- [ ] HTTP 429 raises AIRateLimitError
- [ ] HTTP 5xx raises AIServiceUnavailableError
- [ ] Network errors raise AIServiceUnavailableError
- [ ] API key is NEVER logged; model, usage, and latency are logged at DEBUG

## Test Requirements

- **Unit tests:** Mock httpx responses (200, 429, 500, timeout); verify correct exceptions raised; verify content extraction
- **Integration tests:** N/A (external API — use mocks)
- **Edge cases:** Empty response body; missing choices field; connection timeout; network error

## Parent References

| Ref Type | ID               |
|----------|------------------|
| Story    | STORY-008        |
| Epic     | EPIC-002         |
| BRD      | BRD-AI-001, BRD-AI-009, BRD-NFR-008 |

## Definition of Done

- [ ] Code written and follows project conventions
- [ ] All tests passing (`pytest`)
- [ ] No linting errors
- [ ] PR opened and reviewed
- [ ] Acceptance criteria verified
