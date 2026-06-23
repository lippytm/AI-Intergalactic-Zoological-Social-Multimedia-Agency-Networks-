"""PromptEvolver — orchestrates the evolutionary prompt engineering loop.

Algorithm
---------
1.  **Initialise** a seed population of prompts.
2.  **Evaluate** every prompt using the fitness function.
3.  **Select** parents via tournament selection.
4.  **Reproduce** offspring through mutation and crossover.
5.  **Elitism** — carry the top ``elite_size`` prompts into the next generation.
6.  Repeat for ``generations`` iterations.
7.  Return the best prompt found.
"""

from __future__ import annotations

import random
from typing import Callable, Iterable, List, Optional

from .fitness import score_prompt
from .operators import crossover, mutate, tournament_select
from .population import PromptPopulation
from .prompt import Prompt


class PromptEvolver:
    """Evolves a population of prompts over multiple generations.

    Parameters
    ----------
    population_size:
        Number of prompts in each generation.
    generations:
        Number of evolutionary cycles to run.
    mutation_rate:
        Probability (0–1) that an offspring is mutated rather than being a
        pure crossover product.
    elite_size:
        Number of top-scoring prompts that survive unchanged into the next
        generation.
    tournament_k:
        Tournament size for parent selection.
    fitness_fn:
        Callable that accepts a :class:`Prompt` and assigns / returns its
        fitness.  Defaults to the built-in heuristic :func:`score_prompt`.
    seed:
        Optional integer seed for the internal random number generator, for
        reproducibility.
    verbose:
        If ``True``, print progress after each generation.
    """

    def __init__(
        self,
        population_size: int = 10,
        generations: int = 5,
        mutation_rate: float = 0.6,
        elite_size: int = 2,
        tournament_k: int = 3,
        fitness_fn: Optional[Callable[[Prompt], float]] = None,
        seed: Optional[int] = None,
        verbose: bool = False,
    ) -> None:
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.elite_size = elite_size
        self.tournament_k = tournament_k
        self.fitness_fn: Callable[[Prompt], float] = fitness_fn or score_prompt
        self.rng = random.Random(seed)
        self.verbose = verbose

        # History: list of PromptPopulation, one per generation
        self.history: List[PromptPopulation] = []

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def evolve(self, seeds: Iterable[str | Prompt]) -> Prompt:
        """Run the evolutionary loop and return the best prompt found.

        Parameters
        ----------
        seeds:
            Initial prompt texts (``str``) or :class:`Prompt` instances to
            seed generation 0.  If fewer seeds than ``population_size`` are
            provided the seeds are reused (with mutation) to fill the gap.
        """
        seed_list = [
            Prompt(text=s) if isinstance(s, str) else s for s in seeds
        ]

        population = self._seed_population(seed_list)
        self._evaluate_all(population)
        self.history.append(population)

        if self.verbose:
            self._log(population)

        for gen in range(1, self.generations + 1):
            population = self._next_generation(population, gen)
            self._evaluate_all(population)
            self.history.append(population)
            if self.verbose:
                self._log(population)

        overall_best = self._best_across_history()
        return overall_best

    @property
    def best(self) -> Optional[Prompt]:
        """Best prompt found across all generations evaluated so far."""
        return self._best_across_history() if self.history else None

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _seed_population(self, seeds: List[Prompt]) -> PromptPopulation:
        """Build the initial generation, filling up to ``population_size``."""
        pop = PromptPopulation(generation=0)
        if not seeds:
            raise ValueError("At least one seed prompt must be provided.")

        # Fill up to population_size by cycling and mutating seeds
        for i in range(self.population_size):
            base = seeds[i % len(seeds)]
            if i < len(seeds):
                pop.add(base.clone() if base.fitness is not None else base)
            else:
                pop.add(mutate(base, rng=self.rng))
        return pop

    def _evaluate_all(self, population: PromptPopulation) -> None:
        for prompt in population.unevaluated:
            self.fitness_fn(prompt)

    def _next_generation(
        self, current: PromptPopulation, gen: int
    ) -> PromptPopulation:
        next_pop = PromptPopulation(generation=gen)

        # Elitism: carry top prompts forward unchanged
        elites = current.top_k(self.elite_size)
        for elite in elites:
            preserved = elite.clone()
            preserved.fitness = elite.fitness  # keep fitness for display
            next_pop.add(preserved)

        # Fill remainder with offspring
        while len(next_pop) < self.population_size:
            parent_a = tournament_select(
                current.evaluated, k=self.tournament_k, rng=self.rng
            )
            if self.rng.random() < self.mutation_rate:
                child = mutate(parent_a, rng=self.rng)
            else:
                parent_b = tournament_select(
                    current.evaluated, k=self.tournament_k, rng=self.rng
                )
                child = crossover(parent_a, parent_b, rng=self.rng)
            child.generation = gen
            next_pop.add(child)

        return next_pop

    def _best_across_history(self) -> Optional[Prompt]:
        best: Optional[Prompt] = None
        for pop in self.history:
            candidate = pop.best
            if candidate is None:
                continue
            if best is None or candidate.fitness > best.fitness:  # type: ignore[operator]
                best = candidate
        return best

    @staticmethod
    def _log(population: PromptPopulation) -> None:
        best = population.best
        avg = population.average_fitness
        print(
            f"Generation {population.generation:3d} | "
            f"size={len(population):3d} | "
            f"avg_fitness={avg:.4f} | "
            f"best_fitness={best.fitness:.4f}"  # type: ignore[union-attr]
        )
