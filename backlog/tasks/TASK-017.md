# Task: Implement ContentService.generate_quiz()

| Field        | Value                |
|--------------|----------------------|
| **Task ID**  | TASK-017             |
| **Story**    | STORY-009            |
| **Status**   | To Do                |
| **Assignee** | develop-agent        |
| **Estimate** | 3h                   |

## Description

Add the `generate_quiz()` method to ContentService that generates a quiz via the AI API, validates the response against the quiz schema, retries on validation failure (up to 2 times), and persists the quiz in the database.

## Implementation Details

**Files to create/modify:**
- `src/services/content_service.py` — Add generate_quiz() method

**Approach:**
```python
async def generate_quiz(self, lesson_id: int, topic: str, level: str, db) -> dict:
    """Generate and persist an AI-powered quiz.

    Steps:
    1. Build quiz prompt via PromptManager
    2. Send to GitHubModelsClient
    3. Validate response with validate_quiz_response()
    4. On validation failure, retry up to 2 times
    5. Persist quiz in quizzes table
    6. Return QuizResponse with assigned quiz_id
    """
    messages = self.prompt_manager.build_quiz_prompt(topic, level, num_questions=3)

    last_error = None
    for attempt in range(3):  # Initial + 2 retries
        raw_json = await self.client.generate(messages, max_tokens=self.quiz_max_tokens)

        try:
            quiz = validate_quiz_response(raw_json, lesson_id, topic, level)
            # Persist quiz
            quiz_repo = QuizRepository(db)
            quiz_id = await quiz_repo.create_quiz(
                lesson_id=lesson_id,
                questions_json=json.dumps([q.model_dump() for q in quiz.questions])
            )
            quiz.quiz_id = quiz_id
            return quiz.model_dump()
        except AIResponseValidationError as e:
            last_error = e
            logger.warning("Quiz validation failed (attempt %d/3): %s", attempt + 1, e)
            continue

    # All retries exhausted
    raise last_error or AIResponseValidationError("Quiz generation failed after 3 attempts")
```

## API Changes

N/A — internal service method.

## Data Model Changes

N/A — uses existing quizzes table.

## Acceptance Criteria

- [ ] generate_quiz() builds prompt and sends to AI API
- [ ] Valid AI JSON is parsed into QuizResponse with validated questions
- [ ] Malformed AI JSON triggers retry (up to 2 retries = 3 total attempts)
- [ ] After all retries fail, AIResponseValidationError is raised (becomes HTTP 502)
- [ ] Valid quiz is persisted in quizzes table with questions_json
- [ ] Returned quiz includes the assigned quiz_id from the database

## Test Requirements

- **Unit tests:** Test with valid AI response; test retry on first malformed + second valid; test all retries fail
- **Integration tests:** Test quiz generation and persistence with mocked AI
- **Edge cases:** AI returns valid JSON on retry; AI returns 3 malformed responses

## Parent References

| Ref Type | ID               |
|----------|------------------|
| Story    | STORY-009        |
| Epic     | EPIC-002         |
| BRD      | BRD-FR-005, BRD-AI-002, BRD-AI-003 |

## Definition of Done

- [ ] Code written and follows project conventions
- [ ] All tests passing (`pytest`)
- [ ] No linting errors
- [ ] PR opened and reviewed
- [ ] Acceptance criteria verified
