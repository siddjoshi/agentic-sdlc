# Task: Add Retry Logic with Exponential Backoff to AI Client

| Field        | Value                |
|--------------|----------------------|
| **Task ID**  | TASK-019             |
| **Story**    | STORY-010            |
| **Status**   | To Do                |
| **Assignee** | develop-agent        |
| **Estimate** | 3h                   |

## Description

Enhance the `GitHubModelsClient.generate()` method with exponential backoff retry logic for HTTP 429 (rate limit) and 5xx (server error) responses. Also handle network errors and request timeouts. Log all AI interactions at appropriate levels.

## Implementation Details

**Files to create/modify:**
- `src/ai/client.py` — Update GitHubModelsClient.generate() with retry logic

**Approach:**
```python
import asyncio
import random
import time
import logging

logger = logging.getLogger("ai.client")

class GitHubModelsClient:
    def __init__(self, api_key, endpoint, model="gpt-4o", timeout=30,
                 max_retries=3, initial_backoff=1.0, max_backoff=30.0, jitter_ms=500):
        self.max_retries = max_retries
        self.initial_backoff = initial_backoff
        self.max_backoff = max_backoff
        self.jitter_ms = jitter_ms
        # ... existing init

    async def generate(self, messages, max_tokens=2000, temperature=0.7) -> str:
        last_exception = None
        for attempt in range(self.max_retries + 1):
            start_time = time.time()
            try:
                response = await self._client.post(
                    f"{self.endpoint}/chat/completions",
                    json={"model": self.model, "messages": messages, "max_tokens": max_tokens, "temperature": temperature},
                )
                latency_ms = (time.time() - start_time) * 1000

                if response.status_code == 429:
                    logger.warning("Rate limited (429) on attempt %d/%d", attempt + 1, self.max_retries + 1)
                    if attempt < self.max_retries:
                        await self._backoff(attempt)
                        continue
                    raise AIRateLimitError("Rate limit exceeded after all retries")

                if response.status_code >= 500:
                    logger.warning("Server error (%d) on attempt %d/%d", response.status_code, attempt + 1, self.max_retries + 1)
                    if attempt < self.max_retries:
                        await self._backoff(attempt)
                        continue
                    raise AIServiceUnavailableError(f"GitHub Models API returned HTTP {response.status_code}")

                response.raise_for_status()
                data = response.json()
                content = data["choices"][0]["message"]["content"]

                logger.debug("AI response: model=%s tokens=%s latency=%.1fms",
                            self.model, data.get("usage"), latency_ms)
                return content

            except (httpx.ConnectError, httpx.TimeoutException) as e:
                latency_ms = (time.time() - start_time) * 1000
                logger.error("Network/timeout error on attempt %d: %s (%.1fms)", attempt + 1, type(e).__name__, latency_ms)
                last_exception = e
                if attempt < self.max_retries:
                    await self._backoff(attempt)
                    continue
                raise AIServiceUnavailableError(details=f"{type(e).__name__}: {str(e)}")

    async def _backoff(self, attempt: int):
        """Exponential backoff with jitter."""
        delay = min(self.initial_backoff * (2 ** attempt), self.max_backoff)
        jitter = random.uniform(-self.jitter_ms / 1000, self.jitter_ms / 1000)
        wait = max(0, delay + jitter)
        logger.debug("Backing off %.2fs before retry (attempt %d)", wait, attempt + 1)
        await asyncio.sleep(wait)
```

## API Changes

N/A — internal client enhancement.

## Data Model Changes

N/A

## Acceptance Criteria

- [ ] HTTP 429 triggers retry with exponential backoff (1s, 2s, 4s base delays)
- [ ] HTTP 5xx triggers retry with same backoff strategy
- [ ] Jitter of ±500ms is applied to each delay
- [ ] Max retries is 3 (configurable)
- [ ] Max backoff delay is 30s (configurable)
- [ ] After all retries exhausted, raises appropriate error
- [ ] httpx.ConnectError and httpx.TimeoutException trigger retry
- [ ] All attempts are logged: WARNING for failures, DEBUG for backoff timing
- [ ] API key is NEVER logged

## Test Requirements

- **Unit tests:** Mock httpx to return 429 then 200; test 3 consecutive 429s raise error; test 5xx retry; test timeout retry; test backoff timing
- **Integration tests:** N/A (use mocks)
- **Edge cases:** All retries fail; first attempt succeeds (no retry needed); mix of 429 and 5xx

## Parent References

| Ref Type | ID               |
|----------|------------------|
| Story    | STORY-010        |
| Epic     | EPIC-002         |
| BRD      | BRD-AI-004, BRD-AI-006, BRD-AI-009, BRD-NFR-005, BRD-NFR-008 |

## Definition of Done

- [ ] Code written and follows project conventions
- [ ] All tests passing (`pytest`)
- [ ] No linting errors
- [ ] PR opened and reviewed
- [ ] Acceptance criteria verified
