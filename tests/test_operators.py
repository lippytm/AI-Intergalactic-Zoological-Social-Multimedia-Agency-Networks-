"""Tests for evolutionary operators: mutate, crossover, tournament_select."""

import random
import pytest
from prompt_evolution.prompt import Prompt
from prompt_evolution.operators import mutate, crossover, tournament_select
from prompt_evolution.fitness import score_prompt


def _evaluated(text: str) -> Prompt:
    p = Prompt(text=text)
    score_prompt(p)
    return p


# ---------------------------------------------------------------------------
# mutate
# ---------------------------------------------------------------------------

class TestMutate:
    def test_returns_new_prompt(self):
        p = Prompt(text="Describe alien life.")
        child = mutate(p, rng=random.Random(0))
        assert isinstance(child, Prompt)
        assert child.prompt_id != p.prompt_id

    def test_parent_id_recorded(self):
        p = Prompt(text="Describe alien life.")
        child = mutate(p, rng=random.Random(0))
        assert p.prompt_id in child.parent_ids

    def test_generation_incremented(self):
        p = Prompt(text="Describe alien life.", generation=3)
        child = mutate(p, rng=random.Random(0))
        assert child.generation == 4

    def test_text_changed(self):
        p = Prompt(text="Describe alien life forms in detail.")
        child = mutate(p, rng=random.Random(42))
        assert child.text != p.text

    def test_invalid_strategy_raises(self):
        with pytest.raises(ValueError, match="Unknown mutation strategy"):
            mutate(Prompt(text="Hello."), strategy="nonexistent")

    @pytest.mark.parametrize("strategy", [
        "append_clause", "prepend_role", "substitute_verb", "insert_context"
    ])
    def test_all_strategies_produce_non_empty_text(self, strategy):
        p = Prompt(text="Tell me about alien species. Create a list.")
        child = mutate(p, rng=random.Random(1), strategy=strategy)
        assert child.text.strip() != ""


# ---------------------------------------------------------------------------
# crossover
# ---------------------------------------------------------------------------

class TestCrossover:
    def test_returns_new_prompt(self):
        a = Prompt(text="Explain quantum tunnelling. Use analogies.")
        b = Prompt(text="You are a physicist. Describe wave functions clearly.")
        child = crossover(a, b, rng=random.Random(0))
        assert isinstance(child, Prompt)

    def test_both_parent_ids_recorded(self):
        a = Prompt(text="Explain quantum tunnelling.")
        b = Prompt(text="Describe wave functions.")
        child = crossover(a, b, rng=random.Random(0))
        assert a.prompt_id in child.parent_ids
        assert b.prompt_id in child.parent_ids

    def test_generation_from_max_parent(self):
        a = Prompt(text="A prompt.", generation=2)
        b = Prompt(text="Another prompt.", generation=5)
        child = crossover(a, b, rng=random.Random(0))
        assert child.generation == 6

    def test_invalid_strategy_raises(self):
        a = Prompt(text="A.")
        b = Prompt(text="B.")
        with pytest.raises(ValueError, match="Unknown crossover strategy"):
            crossover(a, b, strategy="bad_strategy")

    @pytest.mark.parametrize("strategy", ["sentence_crossover", "phrase_splice"])
    def test_all_strategies_produce_non_empty_text(self, strategy):
        a = Prompt(text="You are an expert. Explain alien zoology in detail.")
        b = Prompt(text="Act as a teacher. Describe extraterrestrial flora.")
        child = crossover(a, b, rng=random.Random(7), strategy=strategy)
        assert child.text.strip() != ""


# ---------------------------------------------------------------------------
# tournament_select
# ---------------------------------------------------------------------------

class TestTournamentSelect:
    def test_returns_prompt(self):
        pool = [_evaluated("prompt " + str(i)) for i in range(5)]
        winner = tournament_select(pool, k=3, rng=random.Random(0))
        assert isinstance(winner, Prompt)

    def test_winner_in_pool(self):
        pool = [_evaluated("prompt " + str(i)) for i in range(5)]
        winner = tournament_select(pool, k=3, rng=random.Random(0))
        assert winner in pool

    def test_empty_raises(self):
        with pytest.raises(ValueError, match="candidates must not be empty"):
            tournament_select([], k=3)

    def test_unevaluated_raises(self):
        pool = [Prompt(text="unevaluated")]
        with pytest.raises(ValueError, match="have not been evaluated"):
            tournament_select(pool, k=1)

    def test_k_larger_than_pool_allowed(self):
        pool = [_evaluated("p" + str(i)) for i in range(2)]
        winner = tournament_select(pool, k=10, rng=random.Random(0))
        assert winner in pool
