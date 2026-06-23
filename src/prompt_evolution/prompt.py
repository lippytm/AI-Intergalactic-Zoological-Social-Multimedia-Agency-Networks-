"""Core Prompt data class."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Prompt:
    """Represents a single prompt candidate in the evolutionary population.

    Attributes:
        text: The raw prompt text.
        fitness: Numeric fitness score (higher is better). ``None`` means
            the prompt has not yet been evaluated.
        generation: The evolutionary generation this prompt was created in.
        parent_ids: IDs of the parent prompts (empty for seed prompts).
        prompt_id: Unique identifier for this prompt instance.
    """

    text: str
    fitness: Optional[float] = None
    generation: int = 0
    parent_ids: list[str] = field(default_factory=list)
    prompt_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    # ------------------------------------------------------------------
    # Convenience helpers
    # ------------------------------------------------------------------

    def clone(self) -> "Prompt":
        """Return a shallow copy of this prompt with a new unique ID."""
        return Prompt(
            text=self.text,
            fitness=None,
            generation=self.generation,
            parent_ids=list(self.parent_ids),
        )

    def is_evaluated(self) -> bool:
        """Return ``True`` if a fitness score has been assigned."""
        return self.fitness is not None

    def __repr__(self) -> str:
        score = f"{self.fitness:.4f}" if self.fitness is not None else "unevaluated"
        short = self.text[:60].replace("\n", " ")
        return f"Prompt(gen={self.generation}, fitness={score}, text={short!r})"
