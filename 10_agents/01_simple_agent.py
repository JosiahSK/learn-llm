"""
01_simple_agent.py — Building a ReAct Tool-Calling Agent
=======================================================
Demonstrates tool registration, reasoning loops, tool dispatch, and safety boundaries
using modern LangGraph prebuilt ReAct workflows.
"""

import os
import sys
import ast
import operator
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def get_current_time(city: str) -> str:
    """Returns the current timestamp in a specified city."""
    timezones = {
        "london": "Europe/London",
        "new york": "America/New_York",
        "tokyo": "Asia/Tokyo",
        "delhi": "Asia/Kolkata",
    }
    tz = timezones.get(city.lower().strip())
    if not tz:
        return f"Unknown city '{city}'. Supported: {list(timezones.keys())}"
    return datetime.now(ZoneInfo(tz)).strftime("%Y-%m-%d %H:%M:%S")


def safe_calculator(expression: str) -> str:
    """Safely evaluates basic mathematical arithmetic without arbitrary code execution."""
    allowed = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
    }
    try:
        tree = ast.parse(expression.strip(), mode="eval")
        def _eval(node):
            if isinstance(node, ast.Constant):
                return node.value
            if isinstance(node, ast.BinOp) and type(node.op) in allowed:
                return allowed[type(node.op)](_eval(node.left), _eval(node.right))
            raise ValueError("Unsupported operation")
        return str(_eval(tree.body))
    except Exception as exc:
        return f"Calculation error: {exc}"


def main():
    print("=" * 60)
    print("Module 10: ReAct Agent Architecture & Tool Execution")
    print("=" * 60)

    print("\n1. Registered Safe Tools:")
    print("  - get_current_time(city: str)")
    print("  - safe_calculator(expression: str)")

    print("\n2. Simulating Agent Decision Flow:")
    query = "What is the time in Tokyo, and what is 125 multiplied by 8?"
    print(f"User Question: '{query}'")

    print("\nStep 1 (Reasoning): The user asks for Tokyo time and a math calculation.")
    print("Step 2 (Action 1): Call get_current_time('tokyo')")
    time_res = get_current_time("tokyo")
    print(f"       Observation 1 -> {time_res}")

    print("Step 3 (Action 2): Call safe_calculator('125 * 8')")
    math_res = safe_calculator("125 * 8")
    print(f"       Observation 2 -> {math_res}")

    print("Step 4 (Final Answer): Synthesizing findings:")
    print("-" * 50)
    print(f"The current time in Tokyo is {time_res}, and 125 * 8 equals {math_res}.")
    print("-" * 50)
    print("\n[Security Rule] Never use eval() or grant unrestricted shell access to an agent.")


if __name__ == "__main__":
    main()
