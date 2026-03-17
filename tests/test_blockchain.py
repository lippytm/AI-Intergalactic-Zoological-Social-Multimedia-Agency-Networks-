"""Tests for the BlockchainCurriculum module."""

import pytest

from encyclopedia.blockchain import (
    BlockchainCurriculum,
    BlockchainLesson,
    BlockchainPlatform,
    SmartContractExample,
)


class TestSmartContractExample:
    def test_display_contains_title(self):
        example = SmartContractExample(
            title="My Contract",
            platform=BlockchainPlatform.ETHEREUM,
            language="Solidity",
            code="contract Test {}",
            explanation="A test contract.",
        )
        display = example.display()
        assert "My Contract" in display
        assert "Solidity" in display
        assert "contract Test {}" in display
        assert "A test contract." in display


class TestBlockchainLesson:
    def test_summarize_includes_title(self):
        lesson = BlockchainLesson(
            title="Blockchain Basics",
            description="Learn the basics.",
            key_concepts=["hashing", "blocks"],
            exercises=["Exercise 1"],
        )
        summary = lesson.summarize()
        assert "Blockchain Basics" in summary
        assert "1" in summary  # exercise count


class TestBlockchainCurriculum:
    def setup_method(self):
        self.bc = BlockchainCurriculum()

    def test_get_lessons_returns_list(self):
        lessons = self.bc.get_lessons()
        assert isinstance(lessons, list)
        assert len(lessons) >= 5  # at least the built-in lessons

    def test_add_lesson(self):
        custom = BlockchainLesson(
            title="Custom Lesson",
            description="Custom description.",
        )
        self.bc.add_lesson(custom)
        assert custom in self.bc.get_lessons()

    def test_get_lesson_by_title_found(self):
        lesson = self.bc.get_lesson_by_title("Blockchain Fundamentals")
        assert lesson is not None
        assert lesson.title == "Blockchain Fundamentals"

    def test_get_lesson_by_title_case_insensitive(self):
        lesson = self.bc.get_lesson_by_title("blockchain fundamentals")
        assert lesson is not None

    def test_get_lesson_by_title_not_found(self):
        lesson = self.bc.get_lesson_by_title("Does Not Exist")
        assert lesson is None

    def test_get_lessons_by_platform_ethereum(self):
        lessons = self.bc.get_lessons_by_platform(BlockchainPlatform.ETHEREUM)
        assert len(lessons) > 0
        for lesson in lessons:
            assert any(ex.platform == BlockchainPlatform.ETHEREUM for ex in lesson.examples)

    def test_get_lessons_by_platform_no_results(self):
        # Hyperledger has no built-in examples
        lessons = self.bc.get_lessons_by_platform(BlockchainPlatform.HYPERLEDGER)
        assert lessons == []

    def test_summarize_contains_header(self):
        summary = self.bc.summarize()
        assert "Blockchain Curriculum" in summary

    def test_summarize_contains_lesson_titles(self):
        summary = self.bc.summarize()
        assert "Blockchain Fundamentals" in summary
        assert "Smart Contracts 101" in summary
