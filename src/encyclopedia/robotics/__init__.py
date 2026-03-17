"""
Robotics Training Module
=========================
Teaching and Training Robotics Robots and Space Aliens & People
to Become Better Programmers.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Dict, List, Optional


class RobotType(Enum):
    """Classification of robot learners."""
    HUMANOID = "humanoid"
    WHEELED = "wheeled"
    DRONE = "drone"
    SPACE_EXPLORER = "space_explorer"
    INDUSTRIAL_ARM = "industrial_arm"
    SOFT_ROBOT = "soft_robot"
    ALIEN_ANDROID = "alien_android"


class ProgrammingTask(Enum):
    """High-level programming tasks a robot can learn."""
    SENSOR_READING = "sensor_reading"
    MOTOR_CONTROL = "motor_control"
    PATH_PLANNING = "path_planning"
    OBJECT_DETECTION = "object_detection"
    NATURAL_LANGUAGE = "natural_language_processing"
    BLOCKCHAIN_TX = "blockchain_transaction"
    SELF_IMPROVEMENT = "self_improvement"


@dataclass
class RobotLearner:
    """
    Represents a robot (or alien android) that is enrolled in the
    Encyclopedia of Everything Applied training programme.
    """
    name: str
    robot_type: RobotType
    completed_tasks: List[ProgrammingTask] = field(default_factory=list)
    proficiency_scores: Dict[str, float] = field(default_factory=dict)

    def complete_task(self, task: ProgrammingTask, score: float) -> None:
        """Record a completed programming task with a proficiency score (0–100)."""
        if not 0.0 <= score <= 100.0:
            raise ValueError(f"Score must be in [0, 100], got {score}")
        if task not in self.completed_tasks:
            self.completed_tasks.append(task)
        self.proficiency_scores[task.value] = score

    def overall_score(self) -> float:
        """Return the mean proficiency score across all completed tasks."""
        if not self.proficiency_scores:
            return 0.0
        return sum(self.proficiency_scores.values()) / len(self.proficiency_scores)

    def report_card(self) -> str:
        """Return a formatted progress report."""
        lines = [
            f"Robot Learner: {self.name} ({self.robot_type.value})",
            f"  Tasks completed: {len(self.completed_tasks)}",
            f"  Overall proficiency: {self.overall_score():.1f}/100",
            "  Scores by task:",
        ]
        for task_name, score in sorted(self.proficiency_scores.items()):
            bar = "█" * int(score / 10) + "░" * (10 - int(score / 10))
            lines.append(f"    {task_name:<30} {bar} {score:.1f}")
        return "\n".join(lines)


@dataclass
class TrainingScenario:
    """
    A simulated scenario in which a robot practises a programming task.

    ``evaluator`` is a callable that accepts a robot and the learner's
    solution code (as a string) and returns a score in [0, 100].
    """
    title: str
    task: ProgrammingTask
    description: str
    starter_code: str
    hint: str = ""
    evaluator: Optional[Callable[[RobotLearner, str], float]] = field(
        default=None, repr=False
    )

    def display(self) -> str:
        """Return a formatted description of the scenario."""
        hint_section = f"\nHint: {self.hint}" if self.hint else ""
        return (
            f"=== {self.title} ===\n"
            f"Task type: {self.task.value}\n"
            f"{self.description}{hint_section}\n\n"
            f"Starter code:\n```python\n{self.starter_code}\n```"
        )


# ---------------------------------------------------------------------------
# Built-in training scenarios
# ---------------------------------------------------------------------------

_SCENARIOS: List[TrainingScenario] = [
    TrainingScenario(
        title="Read a Proximity Sensor",
        task=ProgrammingTask.SENSOR_READING,
        description=(
            "Write a function that reads the current distance from an ultrasonic "
            "proximity sensor and returns True if an obstacle is within 30 cm."
        ),
        starter_code="""\
def is_obstacle_close(sensor_reading_cm: float) -> bool:
    \"\"\"Return True if the reading indicates an obstacle within 30 cm.\"\"\"
    # TODO: implement
    return False
""",
        hint="A simple comparison against the threshold is all you need.",
    ),
    TrainingScenario(
        title="Drive in a Square",
        task=ProgrammingTask.MOTOR_CONTROL,
        description=(
            "Command a wheeled robot to drive in a 1-metre square using "
            "the provided motor controller API."
        ),
        starter_code="""\
class MotorController:
    def move_forward(self, distance_m: float) -> None: ...
    def turn_left(self, degrees: float) -> None: ...

def drive_square(motors: MotorController, side_m: float = 1.0) -> None:
    \"\"\"Drive the robot in a square of the given side length.\"\"\"
    # TODO: implement four sides and four 90-degree turns
    pass
""",
        hint="A square has four equal sides and four 90-degree turns.",
    ),
    TrainingScenario(
        title="A* Path Planning",
        task=ProgrammingTask.PATH_PLANNING,
        description=(
            "Implement the A* search algorithm to find the shortest path on a "
            "grid map from a start cell to a goal cell, avoiding obstacles."
        ),
        starter_code="""\
from typing import List, Tuple, Optional
import heapq

def astar(
    grid: List[List[int]],
    start: Tuple[int, int],
    goal: Tuple[int, int],
) -> Optional[List[Tuple[int, int]]]:
    \"\"\"
    Find the shortest path on a 2-D grid using A*.

    :param grid: 2-D list where 0 = free, 1 = obstacle
    :param start: (row, col) of the start cell
    :param goal:  (row, col) of the goal cell
    :returns: list of (row, col) cells from start to goal, or None if no path
    \"\"\"
    # TODO: implement A*
    return None
""",
        hint="Use a min-heap with (f_score, cell) entries and a Manhattan distance heuristic.",
    ),
    TrainingScenario(
        title="Sign a Blockchain Transaction",
        task=ProgrammingTask.BLOCKCHAIN_TX,
        description=(
            "Write a function that constructs and signs an Ethereum-style transaction "
            "from a robot's private key (provided as a hex string)."
        ),
        starter_code="""\
def sign_transaction(
    private_key_hex: str,
    to_address: str,
    value_wei: int,
    nonce: int,
    gas_price_gwei: int = 20,
    gas_limit: int = 21000,
) -> str:
    \"\"\"
    Build and sign a basic Ether transfer transaction.

    :returns: signed transaction hex string (0x-prefixed)
    \"\"\"
    # TODO: use eth_account or a compatible library
    return ""
""",
        hint="The eth_account library's sign_transaction helper handles the RLP encoding.",
    ),
    TrainingScenario(
        title="Generate an Improved Training Prompt",
        task=ProgrammingTask.SELF_IMPROVEMENT,
        description=(
            "Use the PromptEngineer module to create a prompt for an AI model that "
            "will help this robot learn a new skill faster. Then apply at least two "
            "improvement strategies and return the final prompt text."
        ),
        starter_code="""\
from encyclopedia.prompts import PromptEngineer, PromptCategory

def build_learning_prompt(skill: str) -> str:
    \"\"\"
    Return an optimised prompt for learning 'skill'.

    :param skill: the skill or concept to learn (e.g. 'recursion')
    :returns: improved prompt text string
    \"\"\"
    engineer = PromptEngineer()
    # TODO: create a prompt, then improve it
    return ""
""",
        hint="Use create_from_template() then call improve() with specific strategies.",
    ),
]


class RoboticsTrainer:
    """
    Robotics training system for the Encyclopedia of Everything Applied.

    Enrolls robot (and alien android) learners, assigns training scenarios,
    and tracks their programming proficiency over time.
    """

    def __init__(self) -> None:
        self._learners: Dict[str, RobotLearner] = {}
        self._scenarios: List[TrainingScenario] = list(_SCENARIOS)

    # ------------------------------------------------------------------
    # Learner management
    # ------------------------------------------------------------------

    def enroll(self, learner: RobotLearner) -> None:
        """Enroll a robot learner in the training programme."""
        self._learners[learner.name] = learner

    def get_learner(self, name: str) -> Optional[RobotLearner]:
        """Return an enrolled learner by name."""
        return self._learners.get(name)

    def list_learners(self) -> List[RobotLearner]:
        """Return all enrolled learners."""
        return list(self._learners.values())

    # ------------------------------------------------------------------
    # Scenarios
    # ------------------------------------------------------------------

    def get_scenarios(self) -> List[TrainingScenario]:
        """Return all training scenarios."""
        return list(self._scenarios)

    def get_scenarios_by_task(self, task: ProgrammingTask) -> List[TrainingScenario]:
        """Return scenarios for a specific task type."""
        return [s for s in self._scenarios if s.task == task]

    def add_scenario(self, scenario: TrainingScenario) -> None:
        """Add a custom training scenario."""
        self._scenarios.append(scenario)

    # ------------------------------------------------------------------
    # Training flow
    # ------------------------------------------------------------------

    def run_scenario(
        self,
        learner: RobotLearner,
        scenario: TrainingScenario,
        solution_code: str,
    ) -> float:
        """
        Evaluate a learner's solution to a scenario.

        If the scenario has a custom evaluator, it is invoked. Otherwise
        a default heuristic scores based on whether the solution is non-empty
        and contains a return statement.
        """
        if scenario.evaluator is not None:
            score = scenario.evaluator(learner, solution_code)
        else:
            score = self._default_evaluator(solution_code)

        learner.complete_task(scenario.task, score)
        return score

    @staticmethod
    def _default_evaluator(solution_code: str) -> float:
        """
        Simple heuristic evaluator used when no custom evaluator is provided.

        Awards points for non-empty solutions that contain meaningful code.
        """
        code = solution_code.strip()
        if not code:
            return 0.0
        score = 50.0  # base for a non-empty attempt
        if "return" in code:
            score += 20.0
        if len(code.splitlines()) > 3:
            score += 15.0
        if any(kw in code for kw in ("for", "while", "if")):
            score += 15.0
        return min(score, 100.0)

    def leaderboard(self) -> str:
        """Return a leaderboard of all enrolled learners ranked by overall score."""
        if not self._learners:
            return "No learners enrolled yet."
        ranked = sorted(
            self._learners.values(),
            key=lambda lr: lr.overall_score(),
            reverse=True,
        )
        lines = ["=== Robotics Training Leaderboard ==="]
        for rank, learner in enumerate(ranked, 1):
            lines.append(
                f"  {rank}. {learner.name:<25} "
                f"{learner.overall_score():.1f}/100  "
                f"({len(learner.completed_tasks)} task(s) completed)"
            )
        return "\n".join(lines)
