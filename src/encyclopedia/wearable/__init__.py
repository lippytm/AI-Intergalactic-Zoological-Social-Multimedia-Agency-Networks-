"""
Wearable Technology Integration Module
=======================================
Using Wearable Technologies for Robotics Robots, Space Aliens and People
to Make and Create Technologies for Teaching and Training Machines to
Become Better Programmers and Blockchain Developers.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class DeviceType(Enum):
    """Categories of wearable device."""
    SMARTWATCH = "smartwatch"
    AR_HEADSET = "augmented_reality_headset"
    EXOSKELETON = "exoskeleton"
    BIOSENSOR_PATCH = "biosensor_patch"
    NEURAL_INTERFACE = "neural_interface"
    LIFE_SUPPORT_SUIT = "life_support_suit"  # for space aliens
    ROBOT_CHASSIS_WEARABLE = "robot_chassis_wearable"


class SensorType(Enum):
    """Types of sensors commonly embedded in wearables."""
    ACCELEROMETER = "accelerometer"
    GYROSCOPE = "gyroscope"
    HEART_RATE = "heart_rate"
    TEMPERATURE = "temperature"
    EEG = "electroencephalogram"
    EMG = "electromyogram"
    GPS = "gps"
    ENVIRONMENTAL = "environmental"
    PROXIMITY = "proximity"
    CAMERA = "camera"


@dataclass
class SensorReading:
    """A timestamped reading from a wearable sensor."""
    sensor: SensorType
    value: Any
    unit: str
    timestamp_ms: int  # milliseconds since epoch

    def __str__(self) -> str:
        return f"[{self.sensor.value}] {self.value} {self.unit} @ t={self.timestamp_ms}ms"


@dataclass
class WearableDevice:
    """
    Represents a wearable device worn by a robot, space alien, or human learner.
    """
    name: str
    device_type: DeviceType
    sensors: List[SensorType] = field(default_factory=list)
    firmware_version: str = "1.0.0"
    battery_level_pct: float = 100.0
    _readings: List[SensorReading] = field(default_factory=list, init=False, repr=False)

    def record_reading(self, reading: SensorReading) -> None:
        """Store a sensor reading from this device."""
        self._readings.append(reading)

    def get_readings(self, sensor: Optional[SensorType] = None) -> List[SensorReading]:
        """Return all stored readings, optionally filtered by sensor type."""
        if sensor is None:
            return list(self._readings)
        return [r for r in self._readings if r.sensor == sensor]

    def clear_readings(self) -> None:
        """Discard all stored readings."""
        self._readings.clear()

    def status(self) -> str:
        """Return a human-readable device status."""
        return (
            f"Device: {self.name} ({self.device_type.value})\n"
            f"  Firmware: {self.firmware_version}\n"
            f"  Battery: {self.battery_level_pct:.1f}%\n"
            f"  Sensors: {', '.join(s.value for s in self.sensors)}\n"
            f"  Stored readings: {len(self._readings)}"
        )


@dataclass
class WearableProgrammingExercise:
    """
    An exercise that uses wearable sensor data as input for a programming task.

    By coupling physical feedback with code exercises, learners experience an
    immediate, embodied connection between their code and the real world.
    """
    title: str
    description: str
    required_sensors: List[SensorType]
    starter_code: str
    expected_outcome: str

    def display(self) -> str:
        """Return a formatted exercise description."""
        sensors = ", ".join(s.value for s in self.required_sensors)
        return (
            f"=== {self.title} ===\n"
            f"{self.description}\n\n"
            f"Required sensors: {sensors}\n\n"
            f"Starter code:\n```python\n{self.starter_code}\n```\n\n"
            f"Expected outcome:\n{self.expected_outcome}"
        )


# ---------------------------------------------------------------------------
# Built-in wearable programming exercises
# ---------------------------------------------------------------------------

_EXERCISES: List[WearableProgrammingExercise] = [
    WearableProgrammingExercise(
        title="Step Counter",
        description=(
            "Use accelerometer data from a wearable to count the number of steps "
            "taken by a human, robot, or alien learner."
        ),
        required_sensors=[SensorType.ACCELEROMETER],
        starter_code="""\
def count_steps(accel_readings):
    \"\"\"
    Count steps from a list of (x, y, z) accelerometer readings.

    :param accel_readings: list of (float, float, float) tuples in m/s²
    :returns: estimated step count (int)
    \"\"\"
    # TODO: implement a peak-detection algorithm
    step_count = 0
    return step_count
""",
        expected_outcome=(
            "The function returns a step count within ±5% of the ground-truth "
            "value on a dataset of 1,000 simulated walking steps."
        ),
    ),
    WearableProgrammingExercise(
        title="Focus Score from Brainwaves",
        description=(
            "Process raw EEG data from a neural-interface headset to produce a "
            "0–100 focus score that can be used to adapt the difficulty of coding "
            "exercises in real time."
        ),
        required_sensors=[SensorType.EEG],
        starter_code="""\
def compute_focus_score(eeg_samples, sampling_rate_hz=256):
    \"\"\"
    Derive a focus score from EEG samples using the beta/alpha power ratio.

    :param eeg_samples: list of float voltage readings (µV)
    :param sampling_rate_hz: number of samples per second
    :returns: focus score in [0, 100]
    \"\"\"
    # TODO: apply FFT, extract alpha (8-12 Hz) and beta (13-30 Hz) band power,
    #       compute ratio, and normalise to [0, 100]
    focus_score = 0.0
    return focus_score
""",
        expected_outcome=(
            "The function returns a score that correlates positively with "
            "self-reported concentration levels across a diverse set of learners."
        ),
    ),
    WearableProgrammingExercise(
        title="Gesture-to-Blockchain-Command",
        description=(
            "Map hand gestures detected via an IMU wristband to blockchain "
            "operations (e.g., fist = sign transaction, open palm = query balance)."
        ),
        required_sensors=[SensorType.ACCELEROMETER, SensorType.GYROSCOPE],
        starter_code="""\
GESTURE_MAP = {
    "fist":       "sign_transaction",
    "open_palm":  "query_balance",
    "swipe_left": "view_block_history",
    "swipe_right":"deploy_contract",
}

def classify_gesture(accel, gyro):
    \"\"\"
    Classify a gesture from a window of IMU data.

    :param accel: list of (x, y, z) accelerometer readings
    :param gyro:  list of (x, y, z) gyroscope readings
    :returns: gesture label string, or 'unknown'
    \"\"\"
    # TODO: train or implement a gesture classifier
    return "unknown"

def gesture_to_blockchain_command(accel, gyro):
    \"\"\"Map a detected gesture to a blockchain command.\"\"\"
    gesture = classify_gesture(accel, gyro)
    return GESTURE_MAP.get(gesture, "no_op")
""",
        expected_outcome=(
            "The pipeline achieves ≥90% accuracy on five pre-defined gestures "
            "in a controlled environment, and triggers the correct blockchain "
            "operation for each."
        ),
    ),
]


class WearableTechIntegration:
    """
    Wearable technology integration hub for the Encyclopedia of Everything Applied.

    Manages registered wearable devices and provides embodied programming
    exercises that bridge physical sensor data with software development skills.
    """

    def __init__(self) -> None:
        self._devices: Dict[str, WearableDevice] = {}
        self._exercises: List[WearableProgrammingExercise] = list(_EXERCISES)

    # ------------------------------------------------------------------
    # Device registry
    # ------------------------------------------------------------------

    def register_device(self, device: WearableDevice) -> None:
        """Register a new wearable device."""
        self._devices[device.name] = device

    def get_device(self, name: str) -> Optional[WearableDevice]:
        """Return a registered device by name."""
        return self._devices.get(name)

    def list_devices(self) -> List[WearableDevice]:
        """Return all registered devices."""
        return list(self._devices.values())

    # ------------------------------------------------------------------
    # Exercises
    # ------------------------------------------------------------------

    def get_exercises(self) -> List[WearableProgrammingExercise]:
        """Return all wearable programming exercises."""
        return list(self._exercises)

    def add_exercise(self, exercise: WearableProgrammingExercise) -> None:
        """Add a custom exercise."""
        self._exercises.append(exercise)

    def get_exercises_for_sensors(
        self, sensors: List[SensorType]
    ) -> List[WearableProgrammingExercise]:
        """Return exercises whose required sensors are a subset of the provided list."""
        sensor_set = set(sensors)
        return [
            ex
            for ex in self._exercises
            if set(ex.required_sensors).issubset(sensor_set)
        ]

    def summarize(self) -> str:
        """Return a human-readable summary."""
        lines = [
            "=== Encyclopedia of Everything Applied — Wearable Tech Integration ===",
            f"Registered devices: {len(self._devices)}",
            f"Exercises available: {len(self._exercises)}",
            "",
            "Exercises:",
        ]
        for ex in self._exercises:
            sensors = ", ".join(s.value for s in ex.required_sensors)
            lines.append(f"  - {ex.title} [sensors: {sensors}]")
        return "\n".join(lines)
