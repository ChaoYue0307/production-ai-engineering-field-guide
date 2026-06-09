from __future__ import annotations

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2] / "src"))

from ai_engineering_basics.schemas import parse_json_object, validate_schema


ANSWER_SCHEMA = {
    "type": "object",
    "required": ["answer", "confidence"],
    "properties": {
        "answer": {"type": "string"},
        "confidence": {"type": "number"},
    },
}


def main() -> None:
    model_text = 'Sure, here is the JSON: {"answer": "Validate before trust.", "confidence": 0.91}'
    parsed = parse_json_object(model_text)
    if not parsed.ok:
        print("Parse failed:", parsed.errors)
        return

    validation = validate_schema(parsed.value, ANSWER_SCHEMA)
    print("Parsed object:", parsed.value)
    print("Schema valid:", validation.ok)
    print("Errors:", validation.errors)


if __name__ == "__main__":
    main()
