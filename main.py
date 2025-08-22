#!/usr/bin/env python3
"""
A small, ready-to-run Python CLI.

Commands:
- greet: Print a friendly greeting
- calc:  Perform basic arithmetic on a list of numbers

Usage examples:
  python3 main.py greet --name Alice
  python3 main.py calc --op add 1 2 3
  python3 main.py calc --op div 10 2
"""
from __future__ import annotations

import argparse
import sys
from typing import List


def greet_user(name: str) -> None:
    """Print a friendly greeting."""
    print(f"Hello, {name}!")


def perform_calculation(operation: str, numbers: List[float]) -> float:
    """Perform a basic arithmetic operation on a list of numbers.

    Supported operations: add, sub, mul, div
    - add: sum all numbers
    - sub: subtract all subsequent numbers from the first
    - mul: multiply all numbers
    - div: divide the first by each subsequent number in sequence
    """
    if not numbers:
        raise ValueError("At least one number is required for calculation")

    if operation == "add":
        result = 0.0
        for value in numbers:
            result += value
        return result

    if operation == "sub":
        result = numbers[0]
        for value in numbers[1:]:
            result -= value
        return result

    if operation == "mul":
        result = 1.0
        for value in numbers:
            result *= value
        return result

    if operation == "div":
        result = numbers[0]
        for value in numbers[1:]:
            if value == 0:
                raise ZeroDivisionError("Cannot divide by zero")
            result /= value
        return result

    raise ValueError(f"Unsupported operation: {operation}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="A small, ready-to-run Python CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # greet subcommand
    greet_parser = subparsers.add_parser("greet", help="Print a friendly greeting")
    greet_parser.add_argument("--name", default="World", help="Name to greet (default: World)")

    # calc subcommand
    calc_parser = subparsers.add_parser("calc", help="Perform basic arithmetic")
    calc_parser.add_argument("--op", choices=["add", "sub", "mul", "div"], required=True, help="Operation to perform")
    calc_parser.add_argument("numbers", nargs="+", type=float, help="Numbers to operate on")

    return parser


def main(argv: List[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "greet":
        greet_user(args.name)
        return 0

    if args.command == "calc":
        try:
            result = perform_calculation(args.op, args.numbers)
            print(result)
            return 0
        except ZeroDivisionError as error:
            print(f"Error: {error}", file=sys.stderr)
            return 1
        except ValueError as error:
            print(f"Error: {error}", file=sys.stderr)
            return 2

    # This should be unreachable due to required subparsers
    print("Error: Unknown command", file=sys.stderr)
    return 3


if __name__ == "__main__":
    sys.exit(main())