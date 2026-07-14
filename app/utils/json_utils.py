"""Утилиты для безопасного разбора JSON-ответов."""

import json
import re
from typing import Any

from app.exceptions import AIResponseFormatError
from app.prompts.subject_prompts import normalize_detected_subject


def parse_openai_json_response(raw_text: str) -> dict[str, Any]:
    """Безопасно разобрать JSON-ответ от модели."""
    if not isinstance(raw_text, str):
        raise AIResponseFormatError(
            "ИИ вернул ответ в неправильном формате. Попробуйте ещё раз."
        )

    text = raw_text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text, flags=re.IGNORECASE)
    text = text.strip()

    if not text:
        raise AIResponseFormatError(
            "ИИ вернул пустой ответ. Попробуйте ещё раз."
        )

    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                data = json.loads(text[start:end + 1])
            except json.JSONDecodeError as exc:
                raise AIResponseFormatError(
                    "ИИ вернул ответ в неправильном формате. Попробуйте ещё раз."
                ) from exc
        else:
            raise AIResponseFormatError(
                "ИИ вернул ответ в неправильном формате. Попробуйте ещё раз."
            )

    if not isinstance(data, dict):
        raise AIResponseFormatError(
            "ИИ вернул ответ в неправильном формате. Попробуйте ещё раз."
        )

    required_fields = [
        "detected_subject",
        "short_answer",
        "steps",
        "formulas",
        "explanation",
        "verification",
    ]

    for field in required_fields:
        if field not in data:
            raise AIResponseFormatError(
                "ИИ вернул ответ в неправильном формате. Попробуйте ещё раз."
            )

    def _normalize_list(value: Any) -> list[str]:
        if isinstance(value, list):
            return [str(item).strip() for item in value if item is not None]
        if value is None:
            return []
        return [str(value).strip()]

    result = {
        "detected_subject": normalize_detected_subject(
            str(data["detected_subject"]).strip()
        ),
        "short_answer": str(data["short_answer"]).strip(),
        "steps": _normalize_list(data["steps"]),
        "formulas": _normalize_list(data["formulas"]),
        "explanation": str(data["explanation"]).strip(),
        "verification": str(data["verification"]).strip(),
    }

    return result
