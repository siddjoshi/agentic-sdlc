# Task: Implement Custom Exceptions and Exception Handlers

| Field        | Value                |
|--------------|----------------------|
| **Task ID**  | TASK-006             |
| **Story**    | STORY-004            |
| **Status**   | To Do                |
| **Assignee** | develop-agent        |
| **Estimate** | 2h                   |

## Description

Create a custom exception hierarchy and FastAPI exception handlers that convert exceptions into structured JSON error responses. This ensures consistent error formatting across all endpoints.

## Implementation Details

**Files to create/modify:**
- `src/exceptions.py` — Custom exception classes and FastAPI exception handlers
- `src/models/errors.py` — ErrorDetail and ErrorResponse Pydantic models
- `src/main.py` — Register exception handlers in create_app()

**Approach:**

Define exception classes:
```python
class AppError(Exception):
    def __init__(self, code: str, message: str, status_code: int = 500, details: str = None, retry_after: int = None):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details
        self.retry_after = retry_after

class CourseNotFoundError(AppError):
    def __init__(self, course_id: int):
        super().__init__("COURSE_NOT_FOUND", f"Course with ID {course_id} was not found.", 404)

class LessonNotFoundError(AppError):
    def __init__(self, lesson_id: int):
        super().__init__("LESSON_NOT_FOUND", f"Lesson with ID {lesson_id} was not found.", 404)

class QuizNotFoundError(AppError):
    def __init__(self, quiz_id: int):
        super().__init__("QUIZ_NOT_FOUND", f"Quiz with ID {quiz_id} was not found.", 404)

class AIServiceUnavailableError(AppError):
    def __init__(self, details: str = None):
        super().__init__("AI_SERVICE_UNAVAILABLE", "The AI content generation service is temporarily unavailable.", 503, details, retry_after=30)

class AIResponseValidationError(AppError):
    def __init__(self, details: str = None):
        super().__init__("AI_RESPONSE_INVALID", "The AI service returned an invalid response.", 502, details, retry_after=10)
```

Register handler in main.py:
```python
@app.exception_handler(AppError)
async def app_error_handler(request, exc: AppError):
    return JSONResponse(status_code=exc.status_code, content={"error": {"code": exc.code, "message": exc.message, "details": exc.details, "retry_after": exc.retry_after}})
```

Error response models:
```python
class ErrorDetail(BaseModel):
    code: str
    message: str
    details: Optional[str] = None
    retry_after: Optional[int] = None

class ErrorResponse(BaseModel):
    error: ErrorDetail
```

## API Changes

N/A — this is cross-cutting error infrastructure.

## Data Model Changes

N/A

## Acceptance Criteria

- [ ] All custom exceptions extend a base AppError class
- [ ] Exception handler converts AppError to structured JSON response with correct HTTP status
- [ ] 404, 422, 502, 503 error paths all produce consistent error format
- [ ] ErrorResponse model is used for OpenAPI documentation

## Test Requirements

- **Unit tests:** Test each exception class attributes; test exception handler output format
- **Integration tests:** Test raising each exception in a route produces correct HTTP response
- **Edge cases:** Exception with None details; exception chaining

## Parent References

| Ref Type | ID               |
|----------|------------------|
| Story    | STORY-004        |
| Epic     | EPIC-004         |
| BRD      | BRD-FR-012       |

## Definition of Done

- [ ] Code written and follows project conventions
- [ ] All tests passing (`pytest`)
- [ ] No linting errors
- [ ] PR opened and reviewed
- [ ] Acceptance criteria verified
