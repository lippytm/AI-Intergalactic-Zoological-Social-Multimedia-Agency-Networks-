"""Tests for the Prompt data class."""

import pytest
from prompt_evolution.prompt import Prompt


def test_prompt_default_fields():
    p = Prompt(text="Describe an alien ecosystem.")
    assert p.text == "Describe an alien ecosystem."
    assert p.fitness is None
    assert p.generation == 0
    assert p.parent_ids == []
    assert len(p.prompt_id) == 36  # UUID format


def test_prompt_is_evaluated():
    p = Prompt(text="Hello.")
    assert not p.is_evaluated()
    p.fitness = 0.75
    assert p.is_evaluated()


def test_prompt_clone():
    p = Prompt(text="Original prompt.", fitness=0.8, generation=2, parent_ids=["abc"])
    clone = p.clone()
    assert clone.text == p.text
    assert clone.fitness is None  # fitness is reset on clone
    assert clone.generation == p.generation
    assert clone.parent_ids == p.parent_ids
    assert clone.prompt_id != p.prompt_id  # new unique ID


def test_prompt_repr_unevaluated():
    p = Prompt(text="Short.")
    rep = repr(p)
    assert "unevaluated" in rep


def test_prompt_repr_evaluated():
    p = Prompt(text="Short.", fitness=0.5)
    rep = repr(p)
    assert "0.5000" in rep


def test_prompt_unique_ids():
    ids = {Prompt(text="x").prompt_id for _ in range(100)}
    assert len(ids) == 100
