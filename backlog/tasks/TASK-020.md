# Task: Implement Quiz Scoring Logic and Submission Route

| Field        | Value                |
|--------------|----------------------|
| **Task ID**  | TASK-020             |
| **Story**    | STORY-011            |
| **Status**   | To Do                |
| **Assignee** | develop-agent        |
| **Estimate** | 3h                   |

## Description

Create the quiz submission route handler `POST /api/v1/quiz/{quiz_id}/submit` that scores user answers against stored quiz data, computes results with per-question feedback, and persists the attempt atomically.

## Implementation Details

**Files to create/modify:**
- `src/routes/quizzes.py` — Quiz submission route handler
- `src/repositories/quiz_repository.py` — Add create_attempt() method
- `src/models/requests.py` — QuizSubmission model
- `src/models/responses.py` — QuizResult, QuestionResult models

**Approach:**
```python
from fastapi import APIRouter, Depends
from src.dependencies import get_db
from src.repositories.quiz_repository import QuizRepository
from src.exceptions import QuizNotFoundError

router = APIRouter(prefix="/api/v1", tags=["quizzes"])

@router.post("/quiz/{quiz_id}/submit", response_model=QuizResult)
async def submit_quiz(
    quiz_id: int,
    submission: QuizSubmission,
    db=Depends(get_db),
):
    repo = QuizRepository(db)
    quiz = await repo.get_quiz(quiz_id)
    if not quiz:
        raise QuizNotFoundError(quiz_id)

    questions = json.loads(quiz["questions_json"])

    # Validate answer count matches question count
    if len(submission.answers) != len(questions):
        raise HTTPException(422, detail=f"Expected {len(questions)} answers, got {len(submission.answers)}")

    # Score answers
    results = []
    score = 0
    for i, question in enumerate(questions):
        correct = submission.answers[i] == question["correct_answer"]
        if correct:
            score += 1
        results.append({"correct": correct, "explanation": question["explanation"]})

    total = len(questions)
    percentage = round(score / total * 100, 1)

    # Persist attempt atomically
    await repo.create_attempt(
        quiz_id=quiz_id,
        user_id=submission.user_id,
        score=score,
        total=total,
        percentage=percentage,
        answers_json=json.dumps(submission.answers),
    )

    return QuizResult(
        quiz_id=quiz_id,
        user_id=submission.user_id,
        score=score,
        total=total,
        percentage=percentage,
        results=results,
    )
```

QuizRepository.create_attempt():
```python
async def create_attempt(self, quiz_id, user_id, score, total, percentage, answers_json) -> int:
    cursor = await self.db.execute(
        "INSERT INTO quiz_attempts (quiz_id, user_id, score, total, percentage, answers_json) VALUES (?, ?, ?, ?, ?, ?)",
        (quiz_id, user_id, score, total, percentage, answers_json)
    )
    await self.db.commit()
    return cursor.lastrowid
```

## API Changes

| Endpoint                          | Method | Description          |
|-----------------------------------|--------|----------------------|
| `/api/v1/quiz/{quiz_id}/submit`   | POST   | Submit quiz answers  |

**Request body:**
```json
{
  "user_id": "user-42",
  "answers": ["YAML", "on", "The runner environment"]
}
```

**Response body:**
```json
{
  "quiz_id": 12,
  "user_id": "user-42",
  "score": 2,
  "total": 3,
  "percentage": 66.7,
  "results": [
    {"correct": true, "explanation": "..."},
    {"correct": false, "explanation": "..."},
    {"correct": true, "explanation": "..."}
  ]
}
```

## Data Model Changes

N/A — uses existing quiz_attempts table.

## Acceptance Criteria

- [ ] POST /api/v1/quiz/{quiz_id}/submit scores answers and returns results
- [ ] Each result includes correct (bool) and explanation
- [ ] Score, total, and percentage are calculated correctly
- [ ] Invalid quiz_id returns HTTP 404
- [ ] Answer count mismatch returns HTTP 422
- [ ] Quiz attempt is persisted atomically in quiz_attempts table
- [ ] Percentage is rounded to 1 decimal place

## Test Requirements

- **Unit tests:** Test scoring with known questions/answers; test 0%, 50%, 100% scores
- **Integration tests:** Full HTTP flow: generate quiz → submit → verify score
- **Edge cases:** All correct; all wrong; empty answers; quiz_id not found

## Parent References

| Ref Type | ID               |
|----------|------------------|
| Story    | STORY-011        |
| Epic     | EPIC-003         |
| BRD      | BRD-FR-006, BRD-FR-011, BRD-NFR-012 |

## Definition of Done

- [ ] Code written and follows project conventions
- [ ] All tests passing (`pytest`)
- [ ] No linting errors
- [ ] PR opened and reviewed
- [ ] Acceptance criteria verified
