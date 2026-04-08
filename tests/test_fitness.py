"""Tests for the fitness scoring module."""

import pytest
from prompt_evolution.prompt import Prompt
from prompt_evolution.fitness import score_prompt


def _scored(text: str) -> float:
    p = Prompt(text=text)
    return score_prompt(p)


def test_score_range():
    for text in [
        "",
        "Hi",
        "Explain quantum entanglement to a space alien step by step.",
        "You are an expert. Describe the biodiversity of the galaxy. "
        "Provide examples and compare ecosystems. Use clear language.",
    ]:
        score = _scored(text)
        assert 0.0 <= score <= 1.0, f"Score {score} out of range for: {text!r}"


def test_empty_prompt_low_score():
    score = _scored("")
    assert score < 0.3


def test_well_formed_prompt_higher_than_trivial():
    simple = _scored("tell me stuff")
    good = _scored(
        "You are an expert AI tutor. Explain the fundamentals of evolutionary "
        "algorithms step by step. Provide concrete examples and compare "
        "different selection strategies."
    )
    assert good > simple


def test_score_written_to_prompt():
    p = Prompt(text="Describe alien biology in detail.")
    assert p.fitness is None
    score_prompt(p)
    assert p.fitness is not None
    assert 0.0 <= p.fitness <= 1.0


def test_role_framing_boosts_score():
    without_role = _scored("Describe alien biology.")
    with_role = _scored("You are an expert biologist. Describe alien biology.")
    assert with_role >= without_role


def test_very_long_prompt_penalised():
    long_text = "word " * 1000
    score = _scored(long_text)
    medium_text = "You are an expert. Explain alien taxonomy clearly and concisely."
    assert _scored(medium_text) > score
