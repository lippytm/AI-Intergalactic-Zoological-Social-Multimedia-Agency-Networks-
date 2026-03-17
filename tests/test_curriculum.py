"""Tests for the Curriculum module."""

import pytest

from encyclopedia.curriculum import (
    Curriculum,
    Lesson,
    LearnerType,
    Module,
    SkillLevel,
)


class TestSkillLevel:
    def test_enum_values(self):
        assert SkillLevel.BEGINNER.value == "beginner"
        assert SkillLevel.MASTER.value == "master"


class TestLearnerType:
    def test_enum_values(self):
        assert LearnerType.HUMAN.value == "human"
        assert LearnerType.ROBOT.value == "robot"
        assert LearnerType.SPACE_ALIEN.value == "space_alien"


class TestLesson:
    def test_summarize_includes_title(self):
        lesson = Lesson(
            title="My Lesson",
            description="A test lesson.",
            skill_level=SkillLevel.BEGINNER,
            topics=["topic1"],
            exercises=["ex1", "ex2"],
        )
        summary = lesson.summarize()
        assert "My Lesson" in summary
        assert "BEGINNER" in summary
        assert "2 exercise(s)" in summary

    def test_summarize_includes_prerequisites(self):
        lesson = Lesson(
            title="Advanced",
            description="An advanced lesson.",
            skill_level=SkillLevel.ADVANCED,
            prerequisites=["Basics"],
        )
        summary = lesson.summarize()
        assert "Prerequisites" in summary
        assert "Basics" in summary

    def test_summarize_no_prerequisites(self):
        lesson = Lesson(
            title="Intro",
            description="An intro lesson.",
            skill_level=SkillLevel.BEGINNER,
        )
        summary = lesson.summarize()
        assert "Prerequisites" not in summary


class TestModule:
    def test_add_lesson(self):
        module = Module(name="Test Module", description="desc")
        lesson = Lesson("L1", "d", SkillLevel.BEGINNER)
        module.add_lesson(lesson)
        assert lesson in module.lessons

    def test_get_lessons_by_level(self):
        module = Module(name="Mix", description="desc")
        beginner_lesson = Lesson("B", "d", SkillLevel.BEGINNER)
        advanced_lesson = Lesson("A", "d", SkillLevel.ADVANCED)
        module.add_lesson(beginner_lesson)
        module.add_lesson(advanced_lesson)
        assert module.get_lessons_by_level(SkillLevel.BEGINNER) == [beginner_lesson]
        assert module.get_lessons_by_level(SkillLevel.ADVANCED) == [advanced_lesson]
        assert module.get_lessons_by_level(SkillLevel.MASTER) == []

    def test_summarize_lists_lesson_titles(self):
        module = Module(name="M", description="desc")
        module.add_lesson(Lesson("Hello Lesson", "d", SkillLevel.BEGINNER))
        summary = module.summarize()
        assert "Hello Lesson" in summary


class TestCurriculum:
    def setup_method(self):
        self.curriculum = Curriculum()

    def test_get_modules_returns_list(self):
        modules = self.curriculum.get_modules()
        assert isinstance(modules, list)
        assert len(modules) >= 2  # programming basics + wearable tech

    def test_add_module(self):
        custom = Module("Custom", "desc")
        self.curriculum.add_module(custom)
        assert custom in self.curriculum.get_modules()

    def test_get_learning_path_beginner(self):
        path = self.curriculum.get_learning_path(LearnerType.HUMAN, SkillLevel.BEGINNER)
        assert len(path) > 0
        levels = {lesson.skill_level for lesson in path}
        # Should not include levels before beginner
        assert SkillLevel.BEGINNER in levels

    def test_get_learning_path_advanced_excludes_beginner(self):
        path_adv = self.curriculum.get_learning_path(LearnerType.ROBOT, SkillLevel.ADVANCED)
        for lesson in path_adv:
            assert lesson.skill_level not in (SkillLevel.BEGINNER, SkillLevel.INTERMEDIATE)

    def test_summarize_contains_curriculum_header(self):
        summary = self.curriculum.summarize()
        assert "Curriculum" in summary
