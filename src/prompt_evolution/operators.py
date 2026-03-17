"""Evolutionary operators: mutation, crossover, and selection.

These operators transform one or two ``Prompt`` objects into offspring
that inherit and recombine textual features from their parents.

Mutation strategies
-------------------
* ``append_clause``    – append a refining clause from a curated vocabulary.
* ``prepend_role``     – prepend a role-framing statement.
* ``substitute_verb``  – replace a generic verb with a more instructional one.
* ``insert_context``   – insert a context / constraint sentence at a random split.

Crossover strategies
--------------------
* ``sentence_crossover``  – split both parents at sentence boundaries and
                            interleave sentences from each parent.
* ``phrase_splice``       – take the first half of parent A and append the
                            second half of parent B.
"""

from __future__ import annotations

import random
import re
from typing import Sequence

from .prompt import Prompt

# ---------------------------------------------------------------------------
# Vocabulary banks (intergalactic-zoological theme ✨)
# ---------------------------------------------------------------------------

_REFINING_CLAUSES = [
    "Be specific, clear, and concise.",
    "Provide examples where helpful.",
    "Use step-by-step reasoning.",
    "Consider multiple perspectives.",
    "Focus on practical, actionable insights.",
    "Draw on the wisdom of intergalactic zoological science.",
    "Incorporate evolutionary thinking.",
    "Optimise for clarity and depth.",
    "Reference relevant first principles.",
    "Explain as if teaching an intelligent space alien.",
]

_ROLE_PREFIXES = [
    "You are an expert AI prompt engineer. ",
    "Act as a seasoned intergalactic zoologist. ",
    "You are a creative technologist specialising in machine learning. ",
    "As a blockchain educator from the future, ",
    "You are a highly capable AI assistant. ",
    "Imagine you are a master teacher of robotics and AI. ",
    "Act as an evolutionary algorithm specialist. ",
    "You are a quantum-entanglement narrative designer. ",
]

_GENERIC_VERBS = {
    "tell": "explain",
    "say": "describe",
    "make": "generate",
    "do": "perform",
    "show": "demonstrate",
    "talk about": "elaborate on",
    "write about": "compose a detailed analysis of",
}

_CONTEXT_INSERTS = [
    "Consider the intergalactic context and broader implications. ",
    "Keep in mind the needs of both humans and space aliens. ",
    "Factor in evolutionary and adaptive thinking. ",
    "Ensure the response is accessible to learners of all levels. ",
    "Apply cutting-edge prompt engineering best practices. ",
]

# ---------------------------------------------------------------------------
# Mutation helpers
# ---------------------------------------------------------------------------


def _append_clause(text: str, rng: random.Random) -> str:
    clause = rng.choice(_REFINING_CLAUSES)
    separator = " " if text.endswith((".", "!", "?")) else ". "
    return text.rstrip() + separator + clause


def _prepend_role(text: str, rng: random.Random) -> str:
    prefix = rng.choice(_ROLE_PREFIXES)
    if text and text[0].isupper():
        text = text[0].lower() + text[1:]
    return prefix + text


def _substitute_verb(text: str, rng: random.Random) -> str:
    for generic, specific in _GENERIC_VERBS.items():
        pattern = re.compile(r"\b" + re.escape(generic) + r"\b", re.IGNORECASE)
        if pattern.search(text):
            return pattern.sub(specific, text, count=1)
    return text  # no substitution found


def _insert_context(text: str, rng: random.Random) -> str:
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    if len(sentences) < 2:
        return text + " " + rng.choice(_CONTEXT_INSERTS)
    idx = rng.randint(1, len(sentences) - 1)
    insert = rng.choice(_CONTEXT_INSERTS)
    sentences.insert(idx, insert.strip())
    return " ".join(sentences)


_MUTATIONS = [_append_clause, _prepend_role, _substitute_verb, _insert_context]


def mutate(
    prompt: Prompt,
    rng: random.Random | None = None,
    strategy: str | None = None,
) -> Prompt:
    """Return a mutated offspring of *prompt*.

    Parameters
    ----------
    prompt:
        The parent prompt.
    rng:
        Optional :class:`random.Random` instance for reproducibility.
    strategy:
        One of ``"append_clause"``, ``"prepend_role"``,
        ``"substitute_verb"``, ``"insert_context"``.  If ``None``, a
        strategy is chosen at random.
    """
    if rng is None:
        rng = random.Random()

    strategy_map = {
        "append_clause": _append_clause,
        "prepend_role": _prepend_role,
        "substitute_verb": _substitute_verb,
        "insert_context": _insert_context,
    }

    if strategy is not None:
        fn = strategy_map.get(strategy)
        if fn is None:
            raise ValueError(
                f"Unknown mutation strategy {strategy!r}. "
                f"Choose from: {list(strategy_map)}"
            )
    else:
        fn = rng.choice(_MUTATIONS)

    new_text = fn(prompt.text, rng)
    return Prompt(
        text=new_text,
        generation=prompt.generation + 1,
        parent_ids=[prompt.prompt_id],
    )


# ---------------------------------------------------------------------------
# Crossover helpers
# ---------------------------------------------------------------------------


def _sentence_crossover(text_a: str, text_b: str, rng: random.Random) -> str:
    sents_a = re.split(r"(?<=[.!?])\s+", text_a.strip())
    sents_b = re.split(r"(?<=[.!?])\s+", text_b.strip())
    combined: list[str] = []
    for i, (sa, sb) in enumerate(zip(sents_a, sents_b)):
        combined.append(sa if rng.random() < 0.5 else sb)
    # Append remaining sentences from the longer parent
    extra_a = sents_a[len(sents_b):]
    extra_b = sents_b[len(sents_a):]
    combined.extend(rng.choice([extra_a, extra_b]))
    return " ".join(combined)


def _phrase_splice(text_a: str, text_b: str, rng: random.Random) -> str:
    mid_a = len(text_a) // 2
    mid_b = len(text_b) // 2
    return text_a[:mid_a].rstrip() + " " + text_b[mid_b:].lstrip()


_CROSSOVERS = [_sentence_crossover, _phrase_splice]


def crossover(
    parent_a: Prompt,
    parent_b: Prompt,
    rng: random.Random | None = None,
    strategy: str | None = None,
) -> Prompt:
    """Combine two parent prompts into a single offspring.

    Parameters
    ----------
    parent_a, parent_b:
        The two parent prompts.
    rng:
        Optional :class:`random.Random` instance for reproducibility.
    strategy:
        One of ``"sentence_crossover"`` or ``"phrase_splice"``.
        If ``None``, chosen at random.
    """
    if rng is None:
        rng = random.Random()

    strategy_map = {
        "sentence_crossover": _sentence_crossover,
        "phrase_splice": _phrase_splice,
    }

    if strategy is not None:
        fn = strategy_map.get(strategy)
        if fn is None:
            raise ValueError(
                f"Unknown crossover strategy {strategy!r}. "
                f"Choose from: {list(strategy_map)}"
            )
    else:
        fn = rng.choice(_CROSSOVERS)

    new_text = fn(parent_a.text, parent_b.text, rng)
    generation = max(parent_a.generation, parent_b.generation) + 1
    return Prompt(
        text=new_text,
        generation=generation,
        parent_ids=[parent_a.prompt_id, parent_b.prompt_id],
    )


# ---------------------------------------------------------------------------
# Selection
# ---------------------------------------------------------------------------


def tournament_select(
    candidates: Sequence[Prompt],
    k: int = 3,
    rng: random.Random | None = None,
) -> Prompt:
    """Select the fittest prompt from a random tournament of size *k*.

    All candidates must have been evaluated (``fitness`` is not ``None``).

    Parameters
    ----------
    candidates:
        Pool of evaluated :class:`Prompt` instances to select from.
    k:
        Tournament size.
    rng:
        Optional :class:`random.Random` instance for reproducibility.
    """
    if not candidates:
        raise ValueError("candidates must not be empty")

    if rng is None:
        rng = random.Random()

    k = min(k, len(candidates))
    contestants = rng.sample(list(candidates), k)

    unevaluated = [p for p in contestants if not p.is_evaluated()]
    if unevaluated:
        raise ValueError(
            f"{len(unevaluated)} prompt(s) in the tournament have not been evaluated."
        )

    return max(contestants, key=lambda p: p.fitness)  # type: ignore[return-value]
