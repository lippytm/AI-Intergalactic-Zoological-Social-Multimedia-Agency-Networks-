"""PromptPopulation — manages a generation of prompt candidates."""

from __future__ import annotations

from typing import Iterable, Iterator, List, Optional

from .prompt import Prompt


class PromptPopulation:
    """An ordered collection of :class:`Prompt` instances representing one
    evolutionary generation.

    Parameters
    ----------
    prompts:
        Initial seed prompts.  May be empty; use :meth:`add` to populate.
    generation:
        Generation index for this population.
    """

    def __init__(
        self,
        prompts: Iterable[Prompt] = (),
        generation: int = 0,
    ) -> None:
        self._prompts: List[Prompt] = list(prompts)
        self.generation = generation

    # ------------------------------------------------------------------
    # Collection interface
    # ------------------------------------------------------------------

    def add(self, prompt: Prompt) -> None:
        """Append *prompt* to this population."""
        self._prompts.append(prompt)

    def extend(self, prompts: Iterable[Prompt]) -> None:
        """Append multiple prompts."""
        self._prompts.extend(prompts)

    def __len__(self) -> int:
        return len(self._prompts)

    def __iter__(self) -> Iterator[Prompt]:
        return iter(self._prompts)

    def __getitem__(self, index: int) -> Prompt:
        return self._prompts[index]

    # ------------------------------------------------------------------
    # Evaluation helpers
    # ------------------------------------------------------------------

    @property
    def evaluated(self) -> List[Prompt]:
        """All prompts that have a fitness score."""
        return [p for p in self._prompts if p.is_evaluated()]

    @property
    def unevaluated(self) -> List[Prompt]:
        """All prompts that have not yet been scored."""
        return [p for p in self._prompts if not p.is_evaluated()]

    @property
    def best(self) -> Optional[Prompt]:
        """The prompt with the highest fitness, or ``None`` if empty."""
        evaled = self.evaluated
        if not evaled:
            return None
        return max(evaled, key=lambda p: p.fitness)  # type: ignore[return-value]

    @property
    def average_fitness(self) -> Optional[float]:
        """Mean fitness across evaluated prompts, or ``None`` if none evaluated."""
        evaled = self.evaluated
        if not evaled:
            return None
        return sum(p.fitness for p in evaled) / len(evaled)  # type: ignore[misc]

    # ------------------------------------------------------------------
    # Sorting / filtering
    # ------------------------------------------------------------------

    def top_k(self, k: int) -> List[Prompt]:
        """Return the top *k* evaluated prompts sorted by fitness descending."""
        return sorted(self.evaluated, key=lambda p: p.fitness, reverse=True)[:k]  # type: ignore[return-value]

    def bottom_k(self, k: int) -> List[Prompt]:
        """Return the bottom *k* evaluated prompts sorted by fitness ascending."""
        return sorted(self.evaluated, key=lambda p: p.fitness)[:k]  # type: ignore[return-value]

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        avg = self.average_fitness
        avg_str = f"{avg:.4f}" if avg is not None else "n/a"
        return (
            f"PromptPopulation(generation={self.generation}, "
            f"size={len(self)}, avg_fitness={avg_str})"
        )

    def summary(self) -> str:
        """Return a human-readable summary of the population."""
        lines = [repr(self)]
        for i, p in enumerate(self._prompts):
            lines.append(f"  [{i}] {p}")
        return "\n".join(lines)
