#!/usr/bin/env python3
"""
Simple command-line calculator.

Features:
- Supports standard Python arithmetic operators: +, -, *, /, //, %, **
- Allows use of math module functions (e.g., sin(0.5), sqrt(9)).
- Prevents access to built-ins for basic safety.
- Type "quit" or "exit" to leave.
"""

import math
from typing import Any, Dict

# Restricted evaluation environment
SAFE_GLOBALS: Dict[str, Any] = {"__builtins__": None}
# Expose math module functions and constants
SAFE_GLOBALS.update(math.__dict__)


def safe_eval(expr: str) -> Any:
    """Safely evaluate a mathematical expression using Python's eval.

    Only names from the math module (and no built-ins) are available.
    Raises an exception if evaluation fails.
    """
    return eval(expr, SAFE_GLOBALS, {})


def main() -> None:
    print("Simple Calculator (type 'quit' or 'exit' to close)")
    while True:
        try:
            expr = input(">>> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()  # Ensure newline before exiting
            break

        if expr.lower() in {"quit", "exit"}:
            break
        if not expr:
            continue  # Skip empty input

        try:
            result = safe_eval(expr)
            print(result)
        except Exception as exc:
            print(f"Error: {exc}")


if __name__ == "__main__":
    main()