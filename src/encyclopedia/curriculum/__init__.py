"""
Curriculum Module
=================
Core educational curriculum for teaching programming to all learners:
humans, robots, and space aliens alike.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class SkillLevel(Enum):
    """Learner skill level."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    MASTER = "master"


class LearnerType(Enum):
    """Type of learner in the intergalactic educational system."""
    HUMAN = "human"
    ROBOT = "robot"
    SPACE_ALIEN = "space_alien"
    AI = "artificial_intelligence"
    WEARABLE_DEVICE = "wearable_device"


@dataclass
class Lesson:
    """A single educational lesson."""
    title: str
    description: str
    skill_level: SkillLevel
    topics: List[str] = field(default_factory=list)
    exercises: List[str] = field(default_factory=list)
    prerequisites: List[str] = field(default_factory=list)

    def summarize(self) -> str:
        """Return a human-readable summary of the lesson."""
        prereq_text = (
            f"\n  Prerequisites: {', '.join(self.prerequisites)}"
            if self.prerequisites
            else ""
        )
        return (
            f"[{self.skill_level.value.upper()}] {self.title}\n"
            f"  {self.description}"
            f"{prereq_text}\n"
            f"  Topics: {', '.join(self.topics)}\n"
            f"  Exercises: {len(self.exercises)} exercise(s)"
        )


@dataclass
class Module:
    """A collection of related lessons forming a learning module."""
    name: str
    description: str
    lessons: List[Lesson] = field(default_factory=list)

    def add_lesson(self, lesson: Lesson) -> None:
        """Add a lesson to this module."""
        self.lessons.append(lesson)

    def get_lessons_by_level(self, level: SkillLevel) -> List[Lesson]:
        """Return all lessons at a given skill level."""
        return [l for l in self.lessons if l.skill_level == level]

    def summarize(self) -> str:
        """Return a human-readable summary of the module."""
        lines = [f"Module: {self.name}", f"  {self.description}", "  Lessons:"]
        for lesson in self.lessons:
            lines.append(f"    - [{lesson.skill_level.value}] {lesson.title}")
        return "\n".join(lines)


class Curriculum:
    """
    Master curriculum for the Encyclopedia of Everything Applied.

    Provides structured learning paths for programming and blockchain
    development tailored to different learner types and skill levels.
    """

    PROGRAMMING_BASICS_MODULE = Module(
        name="Programming Fundamentals",
        description="Core programming concepts for all learner types",
        lessons=[
            Lesson(
                title="Introduction to Variables and Data Types",
                description="Learn how to store and manipulate information.",
                skill_level=SkillLevel.BEGINNER,
                topics=["variables", "integers", "strings", "booleans", "lists"],
                exercises=[
                    "Create a variable storing your home planet name",
                    "Build a list of the top 5 programming languages",
                ],
            ),
            Lesson(
                title="Control Flow: Conditions and Loops",
                description="Direct the flow of a program using logic.",
                skill_level=SkillLevel.BEGINNER,
                topics=["if/else", "for loops", "while loops", "break/continue"],
                exercises=[
                    "Write a loop that counts from 1 to 100",
                    "Create a condition that responds to different learner types",
                ],
                prerequisites=["Introduction to Variables and Data Types"],
            ),
            Lesson(
                title="Functions and Modular Programming",
                description="Break programs into reusable, composable units.",
                skill_level=SkillLevel.INTERMEDIATE,
                topics=["functions", "parameters", "return values", "scope", "modules"],
                exercises=[
                    "Write a function that converts Celsius to Kelvin",
                    "Create a module for common intergalactic unit conversions",
                ],
                prerequisites=["Control Flow: Conditions and Loops"],
            ),
            Lesson(
                title="Object-Oriented Programming",
                description="Model the world using classes, objects, and inheritance.",
                skill_level=SkillLevel.INTERMEDIATE,
                topics=["classes", "objects", "inheritance", "polymorphism", "encapsulation"],
                exercises=[
                    "Design a SpaceAlien class with attributes and behaviors",
                    "Extend the SpaceAlien class to model different alien species",
                ],
                prerequisites=["Functions and Modular Programming"],
            ),
            Lesson(
                title="Algorithms and Data Structures",
                description="Solve complex problems efficiently.",
                skill_level=SkillLevel.ADVANCED,
                topics=["sorting", "searching", "trees", "graphs", "hash maps", "complexity"],
                exercises=[
                    "Implement a binary search on a sorted list of star systems",
                    "Build a graph representing intergalactic travel routes",
                ],
                prerequisites=["Object-Oriented Programming"],
            ),
            Lesson(
                title="Distributed Systems and Consensus Algorithms",
                description="Build systems that work across multiple nodes in a network.",
                skill_level=SkillLevel.MASTER,
                topics=[
                    "distributed consensus", "Raft", "Paxos", "Byzantine fault tolerance",
                    "eventual consistency", "CAP theorem",
                ],
                exercises=[
                    "Implement a basic leader election algorithm",
                    "Simulate a Byzantine fault-tolerant network with 7 nodes",
                ],
                prerequisites=["Algorithms and Data Structures"],
            ),
        ],
    )

    WEARABLE_TECH_MODULE = Module(
        name="Wearable Technology Development",
        description="Create software for wearable devices used by robots and space aliens",
        lessons=[
            Lesson(
                title="Introduction to Wearable Computing",
                description="Understand the unique constraints and capabilities of wearable devices.",
                skill_level=SkillLevel.BEGINNER,
                topics=["sensors", "actuators", "low-power computing", "embedded systems"],
                exercises=[
                    "Design a wearable health monitor for a humanoid robot",
                    "List 5 sensors useful for a space-alien life-support suit",
                ],
            ),
            Lesson(
                title="Sensor Data Processing",
                description="Collect, filter, and interpret data from physical sensors.",
                skill_level=SkillLevel.INTERMEDIATE,
                topics=["ADC", "signal filtering", "FFT", "threshold detection", "streaming data"],
                exercises=[
                    "Implement a moving-average filter for accelerometer data",
                    "Detect gestures from raw IMU sensor readings",
                ],
                prerequisites=["Introduction to Wearable Computing"],
            ),
            Lesson(
                title="Edge AI on Wearable Devices",
                description="Run machine learning inference directly on wearable hardware.",
                skill_level=SkillLevel.ADVANCED,
                topics=["TensorFlow Lite", "model quantization", "on-device inference", "TinyML"],
                exercises=[
                    "Deploy a keyword-spotting model to a microcontroller",
                    "Quantize a neural network to run within a 256 KB memory budget",
                ],
                prerequisites=["Sensor Data Processing"],
            ),
        ],
    )

    def __init__(self) -> None:
        self._modules: List[Module] = [
            self.PROGRAMMING_BASICS_MODULE,
            self.WEARABLE_TECH_MODULE,
        ]

    def get_modules(self) -> List[Module]:
        """Return all curriculum modules."""
        return list(self._modules)

    def add_module(self, module: Module) -> None:
        """Add a custom module to the curriculum."""
        self._modules.append(module)

    def get_learning_path(
        self,
        learner_type: LearnerType,
        starting_level: SkillLevel = SkillLevel.BEGINNER,
    ) -> List[Lesson]:
        """
        Return an ordered list of lessons suitable for a given learner type
        starting from the specified skill level.
        """
        level_order = [
            SkillLevel.BEGINNER,
            SkillLevel.INTERMEDIATE,
            SkillLevel.ADVANCED,
            SkillLevel.MASTER,
        ]
        start_idx = level_order.index(starting_level)
        relevant_levels = set(level_order[start_idx:])

        path: List[Lesson] = []
        for module in self._modules:
            for lesson in module.lessons:
                if lesson.skill_level in relevant_levels:
                    path.append(lesson)
        return path

    def summarize(self) -> str:
        """Return a human-readable overview of the entire curriculum."""
        lines = ["=== Encyclopedia of Everything Applied — Curriculum ===", ""]
        for module in self._modules:
            lines.append(module.summarize())
            lines.append("")
        return "\n".join(lines)
