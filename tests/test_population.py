"""Tests for PromptPopulation."""

import pytest
from prompt_evolution.prompt import Prompt
from prompt_evolution.population import PromptPopulation
from prompt_evolution.fitness import score_prompt


def _p(text: str, fitness: float | None = None) -> Prompt:
    p = Prompt(text=text)
    if fitness is not None:
        p.fitness = fitness
    return p


class TestPromptPopulation:
    def test_empty_population(self):
        pop = PromptPopulation()
        assert len(pop) == 0
        assert pop.best is None
        assert pop.average_fitness is None

    def test_add_and_len(self):
        pop = PromptPopulation()
        pop.add(_p("Hello."))
        pop.add(_p("World."))
        assert len(pop) == 2

    def test_extend(self):
        pop = PromptPopulation()
        pop.extend([_p("A"), _p("B"), _p("C")])
        assert len(pop) == 3

    def test_iter(self):
        prompts = [_p("A"), _p("B")]
        pop = PromptPopulation(prompts)
        assert list(pop) == prompts

    def test_getitem(self):
        prompts = [_p("X"), _p("Y")]
        pop = PromptPopulation(prompts)
        assert pop[0] is prompts[0]

    def test_evaluated_and_unevaluated(self):
        pop = PromptPopulation([_p("A", 0.5), _p("B"), _p("C", 0.8)])
        assert len(pop.evaluated) == 2
        assert len(pop.unevaluated) == 1

    def test_best(self):
        pop = PromptPopulation([_p("A", 0.3), _p("B", 0.9), _p("C", 0.1)])
        assert pop.best.fitness == 0.9  # type: ignore[union-attr]

    def test_average_fitness(self):
        pop = PromptPopulation([_p("A", 0.4), _p("B", 0.6)])
        assert abs(pop.average_fitness - 0.5) < 1e-9  # type: ignore[operator]

    def test_top_k(self):
        pop = PromptPopulation([_p("A", 0.1), _p("B", 0.9), _p("C", 0.5)])
        top = pop.top_k(2)
        assert top[0].fitness == 0.9
        assert top[1].fitness == 0.5

    def test_bottom_k(self):
        pop = PromptPopulation([_p("A", 0.1), _p("B", 0.9), _p("C", 0.5)])
        bottom = pop.bottom_k(2)
        assert bottom[0].fitness == 0.1
        assert bottom[1].fitness == 0.5

    def test_repr(self):
        pop = PromptPopulation([_p("A", 0.6)], generation=3)
        r = repr(pop)
        assert "generation=3" in r
        assert "avg_fitness=0.6000" in r

    def test_summary(self):
        pop = PromptPopulation([_p("My prompt.", 0.7)])
        s = pop.summary()
        assert "My prompt." in s
