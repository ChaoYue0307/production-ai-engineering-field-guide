from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from ai_engineering_basics.schemas import ValidationResult, validate_schema


ToolFunction = Callable[[dict[str, Any]], dict[str, Any]]


@dataclass(frozen=True)
class ToolContract:
    name: str
    description: str
    input_schema: dict[str, Any]
    idempotent: bool = True

    def validate_arguments(self, arguments: dict[str, Any]) -> ValidationResult:
        return validate_schema(arguments, self.input_schema)


class IdempotencyStore:
    def __init__(self) -> None:
        self._results: dict[str, dict[str, Any]] = {}

    def get(self, key: str) -> dict[str, Any] | None:
        return self._results.get(key)

    def set(self, key: str, result: dict[str, Any]) -> None:
        self._results[key] = result


class ToolRunner:
    def __init__(self, idempotency_store: IdempotencyStore | None = None) -> None:
        self._tools: dict[str, tuple[ToolContract, ToolFunction]] = {}
        self.idempotency_store = idempotency_store or IdempotencyStore()

    def register(self, contract: ToolContract, function: ToolFunction) -> None:
        self._tools[contract.name] = (contract, function)

    def run(
        self,
        name: str,
        arguments: dict[str, Any],
        *,
        idempotency_key: str | None = None,
    ) -> dict[str, Any]:
        if name not in self._tools:
            return {"ok": False, "error": f"Unknown tool: {name}"}

        contract, function = self._tools[name]
        validation = contract.validate_arguments(arguments)
        if not validation.ok:
            return {"ok": False, "error": "Invalid arguments", "details": validation.errors}

        if contract.idempotent and idempotency_key:
            cached = self.idempotency_store.get(idempotency_key)
            if cached is not None:
                return cached | {"cached": True}

        result = function(arguments)
        if contract.idempotent and idempotency_key:
            self.idempotency_store.set(idempotency_key, result)
        return result
