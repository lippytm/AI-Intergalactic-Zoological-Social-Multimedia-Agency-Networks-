"""Tests for PromptEvolver end-to-end."""

import pytest
from prompt_evolution.evolver import PromptEvolver
from prompt_evolution.prompt import Prompt


class TestPromptEvolver:
    def test_returns_prompt(self):
        evolver = PromptEvolver(population_size=4, generations=2, seed=0)
        best = evolver.evolve(["Describe alien life."])
        assert isinstance(best, Prompt)

    def test_best_has_fitness(self):
        evolver = PromptEvolver(population_size=4, generations=2, seed=1)
        best = evolver.evolve(["Tell me about the galaxy."])
        assert best.fitness is not None
        assert 0.0 <= best.fitness <= 1.0

    def test_history_length(self):
        evolver = PromptEvolver(population_size=4, generations=3, seed=2)
        evolver.evolve(["Write about space aliens."])
        # history = generation 0 + 3 evolution steps
        assert len(evolver.history) == 4

    def test_population_size_maintained(self):
        evolver = PromptEvolver(population_size=6, generations=2, seed=3)
        evolver.evolve(["Explain quantum entanglement."])
        for pop in evolver.history:
            assert len(pop) == 6

    def test_multiple_seeds(self):
        seeds = [
            "Describe alien flora.",
            "You are an expert biologist. Explain xenobotany.",
            "Create a catalog of alien species.",
        ]
        evolver = PromptEvolver(population_size=5, generations=2, seed=4)
        best = evolver.evolve(seeds)
        assert isinstance(best, Prompt)

    def test_no_seeds_raises(self):
        evolver = PromptEvolver(population_size=4, generations=1, seed=5)
        with pytest.raises(ValueError, match="At least one seed"):
            evolver.evolve([])

    def test_best_property_before_evolve(self):
        evolver = PromptEvolver()
        assert evolver.best is None

    def test_best_property_after_evolve(self):
        evolver = PromptEvolver(population_size=4, generations=2, seed=6)
        evolver.evolve(["Teach robots to code."])
        assert evolver.best is not None

    def test_reproducibility(self):
        seeds = ["Describe the intergalactic zoo."]
        e1 = PromptEvolver(population_size=5, generations=3, seed=99)
        e2 = PromptEvolver(population_size=5, generations=3, seed=99)
        b1 = e1.evolve(seeds)
        b2 = e2.evolve(seeds)
        assert b1.fitness == b2.fitness
        assert b1.text == b2.text

    def test_custom_fitness_fn(self):
        def always_one(p: Prompt) -> float:
            p.fitness = 1.0
            return 1.0

        evolver = PromptEvolver(
            population_size=4, generations=2, seed=7, fitness_fn=always_one
        )
        best = evolver.evolve(["Any prompt."])
        assert best.fitness == 1.0

    def test_verbose_does_not_raise(self, capsys):
        evolver = PromptEvolver(
            population_size=4, generations=2, seed=8, verbose=True
        )
        evolver.evolve(["Test verbose output."])
        captured = capsys.readouterr()
        assert "Generation" in captured.out
