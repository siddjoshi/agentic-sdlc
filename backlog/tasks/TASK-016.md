# Task: Implement Quiz Prompt Template and Validation Schemas

| Field        | Value                |
|--------------|----------------------|
| **Task ID**  | TASK-016             |
| **Story**    | STORY-009            |
| **Status**   | To Do                |
| **Assignee** | develop-agent        |
| **Estimate** | 2h                   |

## Description

Create the Pydantic validation schemas for AI-generated quiz responses and the `validate_quiz_response()` function that parses raw AI JSON output into validated quiz models.

## Implementation Details

**Files to create/modify:**
- `src/ai/schemas.py` — QuizQuestion, QuizResponse models and validate_quiz_response()

**Approach:**
```python
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
import json

class QuizQuestion(BaseModel):
    question: str = Field(..., description="The question text")
    options: list[str] = Field(..., min_length=4, max_length=4)
    correct_answer: str = Field(..., description="Must be one of the options")
    explanation: str = Field(..., description="Why the correct answer is right")

    @field_validator("correct_answer")
    @classmethod
    def correct_answer_must_be_in_options(cls, v, info):
        options = info.data.get("options", [])
        if options and v not in options:
            raise ValueError(f"correct_answer '{v}' must be one of the options")
        return v

class QuizResponse(BaseModel):
    quiz_id: Optional[int] = None
    lesson_id: int
    topic: str
    level: str
    questions: list[QuizQuestion] = Field(..., min_length=3, max_length=5)
    generated_at: datetime = Field(default_factory=datetime.utcnow)

def validate_quiz_response(raw_json: str, lesson_id: int, topic: str, level: str) -> QuizResponse:
    """Parse and validate raw AI JSON into a QuizResponse.

    Args:
        raw_json: Raw JSON string from AI
        lesson_id, topic, level: Context for the response

    Returns:
        Validated QuizResponse

    Raises:
        AIResponseValidationError: If JSON is malformed or fails schema validation
    """
    try:
        questions_data = json.loads(raw_json)
        # Handle case where AI wraps in an object with a "questions" key
        if isinstance(questions_data, dict) and "questions" in questions_data:
            questions_data = questions_data["questions"]
        questions = [QuizQuestion(**q) for q in questions_data]
        return QuizResponse(lesson_id=lesson_id, topic=topic, level=level, questions=questions)
    except (json.JSONDecodeError, ValidationError) as e:
        raise AIResponseValidationError(details=str(e))
```

## API Changes

N/A — internal validation.

## Data Model Changes

N/A

## Acceptance Criteria

- [ ] QuizQuestion enforces exactly 4 options
- [ ] QuizQuestion validates correct_answer is in options
- [ ] QuizResponse enforces 3-5 questions
- [ ] validate_quiz_response() parses valid JSON into QuizResponse
- [ ] validate_quiz_response() raises AIResponseValidationError for malformed JSON
- [ ] Handles both array and {"questions": [...]} JSON formats from AI

## Test Requirements

- **Unit tests:** Test valid quiz JSON; test invalid JSON; test wrong option count; test correct_answer not in options
- **Integration tests:** N/A
- **Edge cases:** AI returns extra fields (should be ignored); AI wraps response in object; empty JSON

## Parent References

| Ref Type | ID               |
|----------|------------------|
| Story    | STORY-009        |
| Epic     | EPIC-002         |
| BRD      | BRD-AI-003, BRD-AI-008 |

## Definition of Done

- [ ] Code written and follows project conventions
- [ ] All tests passing (`pytest`)
- [ ] No linting errors
- [ ] PR opened and reviewed
- [ ] Acceptance criteria verified
