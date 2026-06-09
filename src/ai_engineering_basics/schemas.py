from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ValidationResult:
    ok: bool
    value: Any = None
    errors: tuple[str, ...] = ()


def parse_json_object(text: str) -> ValidationResult:
    try:
        value = json.loads(text)
    except json.JSONDecodeError as first_error:
        repaired = extract_first_json_object(text)
        if repaired is None:
            return ValidationResult(False, errors=(str(first_error),))
        try:
            value = json.loads(repaired)
        except json.JSONDecodeError as second_error:
            return ValidationResult(False, errors=(str(second_error),))
    if not isinstance(value, dict):
        return ValidationResult(False, errors=("Expected a JSON object.",))
    return ValidationResult(True, value=value)


def extract_first_json_object(text: str) -> str | None:
    start = text.find("{")
    if start == -1:
        return None

    depth = 0
    in_string = False
    escaped = False
    for index, char in enumerate(text[start:], start=start):
        if escaped:
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if char == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[start : index + 1]
    return None


def validate_schema(value: dict[str, Any], schema: dict[str, Any]) -> ValidationResult:
    errors: list[str] = []
    _validate(value, schema, path="$", errors=errors)
    return ValidationResult(not errors, value=value if not errors else None, errors=tuple(errors))


def _validate(value: Any, schema: dict[str, Any], *, path: str, errors: list[str]) -> None:
    expected_type = schema.get("type")
    if expected_type and not _matches_type(value, expected_type):
        errors.append(f"{path}: expected {expected_type}, got {type(value).__name__}")
        return

    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: expected one of {schema['enum']!r}, got {value!r}")

    if expected_type == "object":
        required = schema.get("required", [])
        for field in required:
            if field not in value:
                errors.append(f"{path}.{field}: required field missing")
        properties = schema.get("properties", {})
        for field, child_schema in properties.items():
            if field in value:
                _validate(value[field], child_schema, path=f"{path}.{field}", errors=errors)

    if expected_type == "array":
        item_schema = schema.get("items")
        if item_schema:
            for index, item in enumerate(value):
                _validate(item, item_schema, path=f"{path}[{index}]", errors=errors)


def _matches_type(value: Any, expected_type: str) -> bool:
    if expected_type == "object":
        return isinstance(value, dict)
    if expected_type == "array":
        return isinstance(value, list)
    if expected_type == "string":
        return isinstance(value, str)
    if expected_type == "number":
        return isinstance(value, int | float) and not isinstance(value, bool)
    if expected_type == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected_type == "boolean":
        return isinstance(value, bool)
    if expected_type == "null":
        return value is None
    return True
