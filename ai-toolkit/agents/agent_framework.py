"""
AI Agents Framework
====================
ReAct-style autonomous agent with tool-use and multi-agent orchestration.
"""

from __future__ import annotations

import json
import logging
import os
from typing import Any, Callable

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


# ---------------------------------------------------------------------------
# Tool registry
# ---------------------------------------------------------------------------

TOOL_REGISTRY: dict[str, Callable[..., str]] = {}


def register_tool(name: str) -> Callable:
    """Decorator to register a function as an agent tool."""
    def decorator(fn: Callable) -> Callable:
        TOOL_REGISTRY[name] = fn
        return fn
    return decorator


@register_tool("calculator")
def calculator(expression: str) -> str:
    """Evaluate a simple arithmetic expression safely."""
    import ast as _ast

    _SAFE_NODE_TYPES = (
        _ast.Expression, _ast.BinOp, _ast.UnaryOp,
        _ast.Add, _ast.Sub, _ast.Mult, _ast.Div, _ast.Mod, _ast.Pow,
        _ast.USub, _ast.UAdd,
        _ast.Constant,
    )
    _MAX_OPERAND = 1e15

    def _check(node: _ast.AST) -> None:
        if not isinstance(node, _SAFE_NODE_TYPES):
            raise ValueError(f"Unsafe node type: {type(node).__name__}")
        if isinstance(node, _ast.Constant):
            if isinstance(node.value, (int, float)) and abs(node.value) > _MAX_OPERAND:
                raise ValueError("Operand exceeds allowed magnitude")
        for child in _ast.iter_child_nodes(node):
            _check(child)

    def _eval(node: _ast.AST) -> float:
        if isinstance(node, _ast.Constant):
            return float(node.value)
        if isinstance(node, _ast.BinOp):
            left  = _eval(node.left)
            right = _eval(node.right)
            ops = {
                _ast.Add:  lambda a, b: a + b,
                _ast.Sub:  lambda a, b: a - b,
                _ast.Mult: lambda a, b: a * b,
                _ast.Div:  lambda a, b: a / b if b != 0 else float("inf"),
                _ast.Mod:  lambda a, b: a % b if b != 0 else float("nan"),
                _ast.Pow:  lambda a, b: a ** b if abs(b) <= 100 else float("inf"),
            }
            fn = ops.get(type(node.op))
            if fn is None:
                raise ValueError("Unsupported operator")
            return fn(left, right)
        if isinstance(node, _ast.UnaryOp):
            operand = _eval(node.operand)
            if isinstance(node.op, _ast.USub): return -operand
            if isinstance(node.op, _ast.UAdd): return +operand
        raise ValueError("Unsupported expression")

    try:
        tree = _ast.parse(expression.strip(), mode="eval")
        _check(tree)
        return str(_eval(tree.body))
    except Exception as exc:
        return f"Error: {exc}"


@register_tool("search")
def web_search(query: str) -> str:
    """Placeholder for a web search tool."""
    return f"[Simulated search results for: {query!r}]"


@register_tool("memory_store")
def memory_store(key: str, value: str) -> str:
    """Store a key-value pair in agent memory."""
    _AGENT_MEMORY[key] = value
    return f"Stored {key!r}"


@register_tool("memory_retrieve")
def memory_retrieve(key: str) -> str:
    """Retrieve a value from agent memory."""
    return _AGENT_MEMORY.get(key, f"Key {key!r} not found.")


_AGENT_MEMORY: dict[str, str] = {}


# ---------------------------------------------------------------------------
# ReAct Agent
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """You are a helpful AI agent. You have access to the following tools:

{tools}

To use a tool, respond with JSON in this format:
{{"thought": "...", "action": "<tool_name>", "action_input": "<input>"}}

When you have a final answer, respond with:
{{"thought": "...", "final_answer": "..."}}
"""


class ReActAgent:
    """A minimal ReAct (Reasoning + Acting) agent powered by OpenAI."""

    def __init__(self, model: str = "gpt-4o", max_steps: int = 10) -> None:
        from openai import OpenAI  # type: ignore
        self._client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        self._model = model
        self._max_steps = max_steps

    def _tools_description(self) -> str:
        return "\n".join(
            f"- {name}: {fn.__doc__ or 'No description.'}"
            for name, fn in TOOL_REGISTRY.items()
        )

    def run(self, user_query: str) -> str:
        messages: list[dict[str, str]] = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT.format(tools=self._tools_description()),
            },
            {"role": "user", "content": user_query},
        ]

        for step in range(self._max_steps):
            response = self._client.chat.completions.create(
                model=self._model,
                messages=messages,
                temperature=0,
            )
            raw = response.choices[0].message.content.strip()
            logger.info("Step %d: %s", step + 1, raw)
            messages.append({"role": "assistant", "content": raw})

            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                return raw

            if "final_answer" in data:
                return data["final_answer"]

            action = data.get("action")
            action_input = data.get("action_input", "")
            if action and action in TOOL_REGISTRY:
                result = TOOL_REGISTRY[action](action_input)
                messages.append({"role": "user", "content": f"Tool result: {result}"})
            else:
                messages.append({"role": "user", "content": "Tool not found."})

        return "Max steps reached without a final answer."


# ---------------------------------------------------------------------------
# Multi-agent orchestration (simple supervisor pattern)
# ---------------------------------------------------------------------------

class MultiAgentOrchestrator:
    """Supervisor that routes tasks to specialised sub-agents."""

    def __init__(self) -> None:
        self._agents: dict[str, ReActAgent] = {}

    def register_agent(self, name: str, agent: ReActAgent) -> None:
        self._agents[name] = agent

    def dispatch(self, agent_name: str, query: str) -> str:
        if agent_name not in self._agents:
            raise ValueError(f"No agent named {agent_name!r}")
        return self._agents[agent_name].run(query)


if __name__ == "__main__":
    result = calculator("2 ** 10 + 42")
    logger.info("Calculator: 2**10 + 42 = %s", result)
    logger.info("Agent framework ready. Set OPENAI_API_KEY to use ReActAgent.")
