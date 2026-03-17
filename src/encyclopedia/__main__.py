"""
Command-line interface for the Encyclopedia of Everything Applied.

Usage
-----
    python -m encyclopedia                     # interactive menu
    python -m encyclopedia curriculum          # show curriculum
    python -m encyclopedia blockchain          # show blockchain curriculum
    python -m encyclopedia knowledge           # show knowledge base
    python -m encyclopedia wearable            # show wearable tech exercises
    python -m encyclopedia robotics            # show robotics scenarios
    python -m encyclopedia prompt <topic>      # generate a learning prompt
"""

from __future__ import annotations

import sys
import textwrap
from typing import List, Optional

from encyclopedia import (
    BlockchainCurriculum,
    Curriculum,
    KnowledgeBase,
    PromptEngineer,
    RoboticsTrainer,
    WearableTechIntegration,
)
from encyclopedia.curriculum import LearnerType, SkillLevel
from encyclopedia.prompts import PromptCategory


def _banner() -> str:
    return textwrap.dedent("""
    ╔══════════════════════════════════════════════════════════════════════╗
    ║       Encyclopedia of Everything Applied  •  v1.0.0                 ║
    ║  Teaching Robots, Space Aliens & People to Become Better            ║
    ║  Programmers and Blockchain Developers!                             ║
    ╚══════════════════════════════════════════════════════════════════════╝
    """)


def cmd_curriculum(_args: List[str]) -> None:
    """Print the full programming curriculum."""
    c = Curriculum()
    print(c.summarize())
    print("\nLearning path for a beginner human:")
    path = c.get_learning_path(LearnerType.HUMAN, SkillLevel.BEGINNER)
    for lesson in path:
        print(f"  • {lesson.title}")


def cmd_blockchain(_args: List[str]) -> None:
    """Print the blockchain development curriculum."""
    bc = BlockchainCurriculum()
    print(bc.summarize())

    print("First lesson in detail:\n")
    lesson = bc.get_lessons()[0]
    print(lesson.summarize())
    if lesson.examples:
        print()
        print(lesson.examples[0].display())


def cmd_knowledge(_args: List[str]) -> None:
    """Print the knowledge base overview."""
    kb = KnowledgeBase()
    print(kb.summarize())

    print("Sample entry — 'Encyclopedia of Everything Applied':\n")
    entry = kb.get_entry("Encyclopedia of Everything Applied")
    if entry:
        print(entry.display(full=True))


def cmd_wearable(_args: List[str]) -> None:
    """Print wearable tech exercises."""
    wt = WearableTechIntegration()
    print(wt.summarize())

    print("\nFirst exercise in detail:\n")
    print(wt.get_exercises()[0].display())


def cmd_robotics(_args: List[str]) -> None:
    """Print robotics training scenarios."""
    trainer = RoboticsTrainer()
    print("=== Encyclopedia of Everything Applied — Robotics Training ===\n")
    for scenario in trainer.get_scenarios():
        print(scenario.display())
        print()


def cmd_prompt(args: List[str]) -> None:
    """Generate and improve a learning prompt for a given topic."""
    topic = " ".join(args) if args else "Python programming"
    engineer = PromptEngineer()

    print(f"Generating learning prompt for topic: '{topic}'\n")

    # Create base prompt
    base = engineer.create_from_template(
        PromptCategory.EDUCATIONAL,
        topic=topic,
        learner_type="robot or human",
        skill_level="beginner",
        concept=topic,
    )
    print(f"Base prompt (v{base.version}):")
    print(textwrap.indent(base.text, "  "))

    # Improve it
    improved = engineer.improve(base, strategies=["chain_of_thought", "add_examples", "specify_format"])
    print(f"\nImproved prompt (v{improved.version}):")
    print(textwrap.indent(improved.text, "  "))

    print(f"\nPrompt lineage: {len(engineer.get_lineage(improved))} version(s)")


_COMMANDS = {
    "curriculum": cmd_curriculum,
    "blockchain": cmd_blockchain,
    "knowledge": cmd_knowledge,
    "wearable": cmd_wearable,
    "robotics": cmd_robotics,
    "prompt": cmd_prompt,
}


def _interactive_menu() -> None:
    print(_banner())
    print("Available commands:")
    for name in _COMMANDS:
        print(f"  {name}")
    print("\nRun with a command argument, e.g.:")
    print("  python -m encyclopedia curriculum")


def main(argv: Optional[List[str]] = None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    if not argv:
        _interactive_menu()
        return 0

    command = argv[0].lower()
    rest = argv[1:]

    if command in _COMMANDS:
        print(_banner())
        _COMMANDS[command](rest)
        return 0

    print(f"Unknown command: {command!r}", file=sys.stderr)
    print(f"Available: {', '.join(_COMMANDS)}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
