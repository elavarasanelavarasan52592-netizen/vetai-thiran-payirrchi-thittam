import json
from typing import List

from pydantic import BaseModel, Field, ValidationError

from gemini_client import generate_text


class QuizQuestion(BaseModel):
    question: str
    options: List[str] = Field(min_length=4, max_length=4)
    correct_answer: str


class QuizResponse(BaseModel):
    questions: List[QuizQuestion] = Field(min_length=3, max_length=3)


def clean_json_block(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()
        if text.lower().startswith("json"):
            text = text[4:].lstrip()
    return text


def generate_quiz(passage: str) -> dict:
    passage = passage.strip()
    if not passage:
        raise ValueError("Passage cannot be empty.")

    prompt = (
        "Create exactly 3 multiple-choice questions from the passage below. "
        "Each question must have exactly 4 options. The correct_answer must be "
        "exactly one of those option strings. Keep questions educational and "
        "answerable only from the passage. Return ONLY valid JSON with this shape:\n"
        '{"questions":[{"question":"...","options":["...","...","...","..."],'
        '"correct_answer":"..."}]}\n\n'
        f"Passage:\n{passage}"
    )

    raw = generate_text(prompt, temperature=0.2, max_output_tokens=1400)
    cleaned = clean_json_block(raw)

    try:
        parsed = json.loads(cleaned)
        validated = QuizResponse.model_validate(parsed)
    except (json.JSONDecodeError, ValidationError) as exc:
        raise ValueError(f"Quiz JSON could not be parsed: {exc}") from exc

    return validated.model_dump()
