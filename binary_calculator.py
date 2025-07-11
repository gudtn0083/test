#!/usr/bin/env python3
"""
Binary Calculator (command-line).

Usage:
    Run the script and enter expressions composed of binary integers (e.g., 1010) and
    operators: +, -, *, /, //, %, **, &, |, ^, <<, >>.

    Examples:
        1010 + 111   -> 10001
        1101 & 1010  -> 1000
        1 << 10      -> 10000000000

Notes:
    • Only integer binary literals (digits 0 or 1) are recognised. They are converted
      to decimal for evaluation, and the result is printed back in binary.
    • Type "quit" or "exit" to leave.
"""

import re
from typing import Any, Dict

# Safe evaluation context – no built-ins exposed
SAFE_GLOBALS: Dict[str, Any] = {"__builtins__": None}

# Regex to capture standalone binary tokens (sequences of 0/1) not preceded by "0b"
BINARY_TOKEN_RE = re.compile(r"\b[01]+\b")


def _bin_replace(match: re.Match[str]) -> str:
    """Convert a binary number token to its decimal string equivalent."""
    token = match.group(0)
    # Ignore tokens like "0" or "1"? They are valid; convert normally.
    return str(int(token, 2))


def preprocess(expr: str) -> str:
    """Replace binary number tokens in *expr* with their decimal equivalents."""
    return BINARY_TOKEN_RE.sub(_bin_replace, expr)


def safe_eval(expr: str) -> int:
    """Safely evaluate *expr* (after preprocessing) and return an int result."""
    processed = preprocess(expr)
    return eval(processed, SAFE_GLOBALS, {})


def main() -> None:
    print("Binary Calculator (type 'quit' or 'exit' to close)")
    while True:
        try:
            expr = input("bin>>> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if expr.lower() in {"quit", "exit"}:
            break
        if not expr:
            continue

        try:
            result = safe_eval(expr)
            # Ensure result is int; if not, cast.
            if not isinstance(result, int):
                print("Error: result is not an integer")
                continue
            print(bin(result)[2:] if result >= 0 else "-" + bin(-result)[2:])
        except Exception as exc:
            print(f"Error: {exc}")


if __name__ == "__main__":
    main()