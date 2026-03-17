"""Fitness / scoring heuristics for prompt candidates.

In a production system this module would call an LLM and measure response
quality.  Here we provide a deterministic, dependency-free heuristic scorer
that can be replaced or extended with real LLM-based evaluation.

Scoring criteria (each 0–1, averaged):
  1. **Clarity**      – prompt is not empty and has reasonable length.
  2. **Specificity**  – contains domain-specific or instructional keywords.
  3. **Structure**    – uses punctuation / formatting cues.
  4. **Diversity**    – character and word-level entropy.
  5. **Role framing** – begins with or contains a role / context statement.
"""

from __future__ import annotations

import math
import re
from collections import Counter
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .prompt import Prompt

# Keywords that indicate a well-scoped, instructional prompt
_INSTRUCTIONAL_KEYWORDS = {
    "explain",
    "describe",
    "list",
    "compare",
    "create",
    "generate",
    "summarize",
    "analyze",
    "define",
    "provide",
    "write",
    "design",
    "outline",
    "suggest",
    "evaluate",
    "teach",
    "train",
    "build",
    "improve",
    "evolve",
    "optimize",
}

_ROLE_PATTERNS = re.compile(
    r"\b(you are|act as|as an?|imagine you are|your role is|context:)\b",
    re.IGNORECASE,
)


def _entropy(text: str) -> float:
    """Shannon entropy of character frequencies, normalised to [0, 1]."""
    if not text:
        return 0.0
    counts = Counter(text)
    total = len(text)
    entropy = -sum((c / total) * math.log2(c / total) for c in counts.values())
    # Max possible entropy for ASCII printable is ~6.57 bits; normalise loosely.
    return min(entropy / 6.57, 1.0)


def _clarity_score(text: str) -> float:
    length = len(text.strip())
    if length == 0:
        return 0.0
    # Ideal range: 50–500 characters
    if 50 <= length <= 500:
        return 1.0
    if length < 50:
        return length / 50.0
    # Penalise very long prompts gently
    return max(0.0, 1.0 - (length - 500) / 2000.0)


def _specificity_score(text: str) -> float:
    words = re.findall(r"\b\w+\b", text.lower())
    if not words:
        return 0.0
    hits = sum(1 for w in words if w in _INSTRUCTIONAL_KEYWORDS)
    return min(hits / max(len(words) * 0.1, 1.0), 1.0)


def _structure_score(text: str) -> float:
    score = 0.0
    if re.search(r"[.!?]", text):
        score += 0.4
    if re.search(r"[:,\-]", text):
        score += 0.3
    if "\n" in text or re.search(r"\d+\.", text):
        score += 0.3
    return min(score, 1.0)


def _role_framing_score(text: str) -> float:
    return 1.0 if _ROLE_PATTERNS.search(text) else 0.0


def score_prompt(prompt: "Prompt") -> float:
    """Compute and return a heuristic fitness score in the range [0.0, 1.0].

    The score is also written back to ``prompt.fitness``.
    """
    text = prompt.text
    components = [
        _clarity_score(text),
        _specificity_score(text),
        _structure_score(text),
        _entropy(text),
        _role_framing_score(text),
    ]
    score = sum(components) / len(components)
    prompt.fitness = round(score, 6)
    return prompt.fitness
