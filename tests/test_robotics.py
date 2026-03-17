"""Tests for the RoboticsTrainer module."""

import pytest

from encyclopedia.robotics import (
    ProgrammingTask,
    RoboticsTrainer,
    RobotLearner,
    RobotType,
    TrainingScenario,
)


class TestRobotLearner:
    def setup_method(self):
        self.learner = RobotLearner(name="R2-Teach", robot_type=RobotType.HUMANOID)

    def test_initial_state(self):
        assert self.learner.completed_tasks == []
        assert self.learner.overall_score() == 0.0

    def test_complete_task(self):
        self.learner.complete_task(ProgrammingTask.SENSOR_READING, 80.0)
        assert ProgrammingTask.SENSOR_READING in self.learner.completed_tasks
        assert self.learner.proficiency_scores[ProgrammingTask.SENSOR_READING.value] == 80.0

    def test_complete_task_updates_score(self):
        self.learner.complete_task(ProgrammingTask.MOTOR_CONTROL, 50.0)
        self.learner.complete_task(ProgrammingTask.MOTOR_CONTROL, 75.0)
        # Only one entry per task
        assert self.learner.completed_tasks.count(ProgrammingTask.MOTOR_CONTROL) == 1
        assert self.learner.proficiency_scores[ProgrammingTask.MOTOR_CONTROL.value] == 75.0

    def test_overall_score_average(self):
        self.learner.complete_task(ProgrammingTask.SENSOR_READING, 60.0)
        self.learner.complete_task(ProgrammingTask.MOTOR_CONTROL, 80.0)
        assert self.learner.overall_score() == pytest.approx(70.0)

    def test_invalid_score_raises(self):
        with pytest.raises(ValueError):
            self.learner.complete_task(ProgrammingTask.SENSOR_READING, 150.0)
        with pytest.raises(ValueError):
            self.learner.complete_task(ProgrammingTask.SENSOR_READING, -1.0)

    def test_report_card_contains_name(self):
        self.learner.complete_task(ProgrammingTask.PATH_PLANNING, 90.0)
        card = self.learner.report_card()
        assert "R2-Teach" in card
        assert "90" in card


class TestRoboticsTrainer:
    def setup_method(self):
        self.trainer = RoboticsTrainer()
        self.learner = RobotLearner("TestBot", RobotType.WHEELED)

    def test_enroll_and_get_learner(self):
        self.trainer.enroll(self.learner)
        retrieved = self.trainer.get_learner("TestBot")
        assert retrieved is self.learner

    def test_get_learner_not_enrolled(self):
        assert self.trainer.get_learner("Ghost") is None

    def test_list_learners(self):
        other = RobotLearner("OtherBot", RobotType.DRONE)
        self.trainer.enroll(self.learner)
        self.trainer.enroll(other)
        learners = self.trainer.list_learners()
        assert self.learner in learners
        assert other in learners

    def test_get_scenarios_returns_built_in(self):
        scenarios = self.trainer.get_scenarios()
        assert len(scenarios) >= 5

    def test_get_scenarios_by_task(self):
        scenarios = self.trainer.get_scenarios_by_task(ProgrammingTask.SENSOR_READING)
        assert len(scenarios) >= 1
        for s in scenarios:
            assert s.task == ProgrammingTask.SENSOR_READING

    def test_add_scenario(self):
        custom = TrainingScenario(
            title="Custom",
            task=ProgrammingTask.OBJECT_DETECTION,
            description="detect things",
            starter_code="pass",
        )
        self.trainer.add_scenario(custom)
        assert custom in self.trainer.get_scenarios()

    def test_run_scenario_default_evaluator_empty(self):
        scenario = self.trainer.get_scenarios_by_task(ProgrammingTask.SENSOR_READING)[0]
        self.trainer.enroll(self.learner)
        score = self.trainer.run_scenario(self.learner, scenario, "")
        assert score == 0.0

    def test_run_scenario_default_evaluator_with_code(self):
        scenario = self.trainer.get_scenarios_by_task(ProgrammingTask.SENSOR_READING)[0]
        self.trainer.enroll(self.learner)
        code = "def is_obstacle_close(reading):\n    return reading < 30\n"
        score = self.trainer.run_scenario(self.learner, scenario, code)
        assert score > 0.0

    def test_run_scenario_custom_evaluator(self):
        def always_100(learner, code):
            return 100.0

        scenario = TrainingScenario(
            title="Perfect",
            task=ProgrammingTask.MOTOR_CONTROL,
            description="always perfect",
            starter_code="pass",
            evaluator=always_100,
        )
        self.trainer.enroll(self.learner)
        score = self.trainer.run_scenario(self.learner, scenario, "anything")
        assert score == 100.0

    def test_leaderboard_no_learners(self):
        output = self.trainer.leaderboard()
        assert "No learners enrolled" in output

    def test_leaderboard_ranks_by_score(self):
        high_scorer = RobotLearner("High", RobotType.HUMANOID)
        low_scorer = RobotLearner("Low", RobotType.WHEELED)
        high_scorer.complete_task(ProgrammingTask.SENSOR_READING, 90.0)
        low_scorer.complete_task(ProgrammingTask.SENSOR_READING, 40.0)
        self.trainer.enroll(high_scorer)
        self.trainer.enroll(low_scorer)
        board = self.trainer.leaderboard()
        assert board.index("High") < board.index("Low")
