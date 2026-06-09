from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

sys.path.append(str(Path(__file__).resolve().parents[2] / "src"))

from ai_engineering_basics.tools import ToolContract, ToolRunner


def lookup_order(arguments: dict[str, Any]) -> dict[str, Any]:
    return {"ok": True, "order_id": arguments["order_id"], "status": "shipped"}


def main() -> None:
    runner = ToolRunner()
    runner.register(
        ToolContract(
            name="lookup_order",
            description="Look up an order status by order ID.",
            input_schema={
                "type": "object",
                "required": ["order_id"],
                "properties": {"order_id": {"type": "string"}},
            },
            idempotent=True,
        ),
        lookup_order,
    )

    valid = runner.run("lookup_order", {"order_id": "ord_123"}, idempotency_key="req_1")
    retry = runner.run("lookup_order", {"order_id": "ord_123"}, idempotency_key="req_1")
    invalid = runner.run("lookup_order", {"order_id": 123})
    hallucinated = runner.run("refund_everything", {"order_id": "ord_123"})

    print("Valid:", valid)
    print("Retry:", retry)
    print("Invalid args:", invalid)
    print("Unknown tool:", hallucinated)


if __name__ == "__main__":
    main()
