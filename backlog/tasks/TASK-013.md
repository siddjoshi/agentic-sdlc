# Task: Implement PromptManager and Prompt Template Files

| Field        | Value                |
|--------------|----------------------|
| **Task ID**  | TASK-013             |
| **Story**    | STORY-008            |
| **Status**   | To Do                |
| **Assignee** | develop-agent        |
| **Estimate** | 2h                   |

## Description

Create the `PromptManager` class that loads prompt templates from the `prompts/` directory and constructs chat messages for lesson content generation and quiz generation. Also create the two prompt template files.

## Implementation Details

**Files to create/modify:**
- `src/ai/prompts.py` — PromptManager class
- `prompts/lesson_content.txt` — Lesson generation prompt template
- `prompts/quiz_generation.txt` — Quiz generation prompt template

**Approach:**

PromptManager:
```python
from pathlib import Path

class PromptManager:
    def __init__(self, prompts_dir: str = "prompts"):
        self.prompts_dir = Path(prompts_dir)
        self._templates = {}
        self._load_templates()

    def _load_templates(self):
        """Load all .txt templates from prompts directory at startup."""
        for template_file in self.prompts_dir.glob("*.txt"):
            self._templates[template_file.stem] = template_file.read_text()

    def build_lesson_prompt(self, topic: str, level: str, objectives: list[str]) -> list[dict]:
        """Build chat messages for lesson content generation."""
        template = self._templates["lesson_content"]
        objectives_str = "\n".join(f"- {obj}" for obj in objectives)
        user_content = template.format(topic=topic, level=level, objectives=objectives_str)
        return [
            {"role": "system", "content": "You are an expert technical trainer..."},
            {"role": "user", "content": user_content}
        ]

    def build_quiz_prompt(self, topic: str, level: str, num_questions: int = 3) -> list[dict]:
        """Build chat messages for quiz generation."""
        template = self._templates["quiz_generation"]
        user_content = template.format(topic=topic, level=level, num_questions=num_questions)
        return [
            {"role": "system", "content": "You are a quiz generator..."},
            {"role": "user", "content": user_content}
        ]
```

Prompt template `prompts/lesson_content.txt`:
```
Generate a lesson about {topic} at the {level} level.

Learning objectives:
{objectives}

Requirements:
- Write in Markdown format
- Include 2-3 explanatory paragraphs
- Include at least one code example with proper syntax highlighting
- For GitHub Actions topics, use YAML code blocks
- For GitHub Copilot topics, use Python or JavaScript code blocks
- For GitHub Advanced Security topics, use YAML or CodeQL code blocks
- Keep content focused and practical
```

Prompt template `prompts/quiz_generation.txt`:
```
Generate a multiple-choice quiz about {topic} at the {level} level.

Requirements:
- Generate exactly {num_questions} questions
- Each question must have exactly 4 answer options
- Exactly 1 option must be correct
- Include an explanation for the correct answer
- Return as a JSON array of objects with fields: question, options, correct_answer, explanation
- The correct_answer value must exactly match one of the options
```

## API Changes

N/A — internal service class.

## Data Model Changes

N/A

## Acceptance Criteria

- [ ] PromptManager loads templates from prompts/ directory at init
- [ ] build_lesson_prompt() returns chat messages with topic, level, and objectives
- [ ] build_quiz_prompt() returns chat messages requesting JSON quiz output
- [ ] Templates use {topic}, {level}, {objectives}/{num_questions} placeholders
- [ ] Templates are version-controlled text files, not inline strings

## Test Requirements

- **Unit tests:** Test template loading; test build_lesson_prompt output contains topic/level; test build_quiz_prompt output
- **Integration tests:** N/A
- **Edge cases:** Missing template file raises clear error; empty objectives list

## Parent References

| Ref Type | ID               |
|----------|------------------|
| Story    | STORY-008        |
| Epic     | EPIC-002         |
| BRD      | BRD-AI-005, BRD-AI-010 |

## Definition of Done

- [ ] Code written and follows project conventions
- [ ] All tests passing (`pytest`)
- [ ] No linting errors
- [ ] PR opened and reviewed
- [ ] Acceptance criteria verified
