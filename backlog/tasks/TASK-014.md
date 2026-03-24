# Task: Implement ContentService.generate_lesson_content()

| Field        | Value                |
|--------------|----------------------|
| **Task ID**  | TASK-014             |
| **Story**    | STORY-008            |
| **Status**   | To Do                |
| **Assignee** | develop-agent        |
| **Estimate** | 2h                   |

## Description

Create the `ContentService` class with the `generate_lesson_content()` method that orchestrates prompt building and AI API calls to produce Markdown lesson content.

## Implementation Details

**Files to create/modify:**
- `src/services/content_service.py` — ContentService class
- `src/ai/schemas.py` — LessonContentResponse model (if not already in models/responses.py)

**Approach:**
```python
from src.ai.client import GitHubModelsClient
from src.ai.prompts import PromptManager

class ContentService:
    def __init__(self, client: GitHubModelsClient, prompt_manager: PromptManager, lesson_max_tokens: int = 2000):
        self.client = client
        self.prompt_manager = prompt_manager
        self.lesson_max_tokens = lesson_max_tokens

    async def generate_lesson_content(self, lesson_id: int, topic: str, level: str, objectives: list[str]) -> dict:
        """Generate AI-powered lesson content.

        Args:
            lesson_id: The lesson ID
            topic: Training topic (e.g., 'GitHub Actions')
            level: Skill level ('beginner' or 'intermediate')
            objectives: List of learning objectives

        Returns:
            Dict with lesson_id, topic, level, content_markdown, generated_at
        """
        messages = self.prompt_manager.build_lesson_prompt(topic, level, objectives)
        content = await self.client.generate(messages, max_tokens=self.lesson_max_tokens)

        return {
            "lesson_id": lesson_id,
            "topic": topic,
            "level": level,
            "content_markdown": content,
            "generated_at": datetime.utcnow().isoformat(),
        }
```

The ContentService receives its dependencies (GitHubModelsClient, PromptManager) via constructor injection. It is instantiated in `src/dependencies.py` and provided to routes via FastAPI `Depends()`.

## API Changes

N/A — internal service method.

## Data Model Changes

N/A

## Acceptance Criteria

- [ ] generate_lesson_content() builds prompt using PromptManager
- [ ] Sends prompt to GitHubModelsClient.generate() with lesson_max_tokens
- [ ] Returns dict matching LessonContentResponse schema
- [ ] Includes lesson_id, topic, level, content_markdown, generated_at
- [ ] Propagates AI errors (AIServiceUnavailableError, etc.) to caller

## Test Requirements

- **Unit tests:** Test with mocked GitHubModelsClient returning sample Markdown; verify response structure
- **Integration tests:** Test full flow with mocked AI API
- **Edge cases:** Empty content from AI; AI returning non-Markdown content

## Parent References

| Ref Type | ID               |
|----------|------------------|
| Story    | STORY-008        |
| Epic     | EPIC-002         |
| BRD      | BRD-FR-004, BRD-AI-001 |

## Definition of Done

- [ ] Code written and follows project conventions
- [ ] All tests passing (`pytest`)
- [ ] No linting errors
- [ ] PR opened and reviewed
- [ ] Acceptance criteria verified
