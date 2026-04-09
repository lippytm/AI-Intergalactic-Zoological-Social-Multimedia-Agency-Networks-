"""Tests for the PromptEngineer module."""

import pytest

from encyclopedia.prompts import Prompt, PromptCategory, PromptEngineer


class TestPromptEngineer:
    def setup_method(self):
        self.engineer = PromptEngineer()

    def test_create_from_template_educational(self):
        prompt = self.engineer.create_from_template(
            PromptCategory.EDUCATIONAL,
            topic="Python",
            learner_type="robot",
            skill_level="beginner",
            concept="for loops",
        )
        assert isinstance(prompt, Prompt)
        assert "Python" in prompt.text
        assert prompt.version == 1
        assert prompt.category == PromptCategory.EDUCATIONAL

    def test_create_from_template_missing_placeholder(self):
        with pytest.raises(ValueError, match="topic"):
            self.engineer.create_from_template(
                PromptCategory.EDUCATIONAL,
                # missing: topic, learner_type, skill_level, concept
            )

    def test_create_custom(self):
        prompt = self.engineer.create_custom(
            "Tell me about space travel",
            PromptCategory.GENERAL,
            tags=["space", "travel"],
        )
        assert prompt.text == "Tell me about space travel"
        assert prompt.category == PromptCategory.GENERAL
        assert "space" in prompt.tags

    def test_improve_increments_version(self):
        base = self.engineer.create_custom("Base prompt", PromptCategory.GENERAL)
        improved = self.engineer.improve(base, strategies=["add_context"])
        assert improved.version == 2
        assert improved.parent_prompt is base

    def test_improve_unknown_strategy_raises(self):
        base = self.engineer.create_custom("Base", PromptCategory.GENERAL)
        with pytest.raises(ValueError, match="Unknown strategy"):
            self.engineer.improve(base, strategies=["nonexistent_strategy"])

    def test_improve_all_strategies_by_default(self):
        base = self.engineer.create_custom("Base", PromptCategory.GENERAL)
        improved = self.engineer.improve(base)
        assert improved.version == 2
        assert len(self.engineer.list_strategies()) > 0

    def test_add_chain_of_thought(self):
        base = self.engineer.create_custom("Original prompt.", PromptCategory.TECHNICAL)
        cot = self.engineer.add_chain_of_thought(base)
        assert "step-by-step" in cot.text
        assert "chain_of_thought" in cot.tags
        assert cot.version == 2

    def test_add_few_shot_examples(self):
        base = self.engineer.create_custom("Prompt.", PromptCategory.TECHNICAL)
        examples = [
            {"input": "What is 2+2?", "output": "4"},
            {"input": "What is 3*3?", "output": "9"},
        ]
        few_shot = self.engineer.add_few_shot_examples(base, examples)
        assert "Example 1" in few_shot.text
        assert "Example 2" in few_shot.text
        assert "few_shot" in few_shot.tags

    def test_get_lineage(self):
        p1 = self.engineer.create_custom("v1", PromptCategory.GENERAL)
        p2 = self.engineer.improve(p1, strategies=["add_context"])
        p3 = self.engineer.add_chain_of_thought(p2)
        lineage = self.engineer.get_lineage(p3)
        assert lineage[0] is p1
        assert lineage[1] is p2
        assert lineage[2] is p3

    def test_get_history_grows(self):
        initial_count = len(self.engineer.get_history())
        self.engineer.create_custom("A", PromptCategory.GENERAL)
        self.engineer.create_custom("B", PromptCategory.EDUCATIONAL)
        assert len(self.engineer.get_history()) == initial_count + 2

    def test_list_templates_returns_strings(self):
        templates = self.engineer.list_templates()
        assert isinstance(templates, list)
        assert len(templates) > 0
        assert all(isinstance(t, str) for t in templates)

    def test_list_strategies_structure(self):
        strategies = self.engineer.list_strategies()
        assert isinstance(strategies, list)
        for item in strategies:
            assert "name" in item
            assert "description" in item

    def test_prompt_summarize(self):
        prompt = Prompt(text="Hello world", category=PromptCategory.GENERAL, version=3)
        summary = prompt.summarize()
        assert "v3" in summary
        assert "general" in summary


class TestPromptStr:
    def test_str_returns_text(self):
        p = Prompt(text="my prompt", category=PromptCategory.CREATIVE)
        assert str(p) == "my prompt"
