"""Tests for the WearableTechIntegration module."""

import pytest

from encyclopedia.wearable import (
    DeviceType,
    SensorReading,
    SensorType,
    WearableDevice,
    WearableProgrammingExercise,
    WearableTechIntegration,
)


class TestSensorReading:
    def test_str_representation(self):
        reading = SensorReading(
            sensor=SensorType.HEART_RATE,
            value=72,
            unit="bpm",
            timestamp_ms=1000,
        )
        assert "heart_rate" in str(reading)
        assert "72" in str(reading)
        assert "bpm" in str(reading)


class TestWearableDevice:
    def setup_method(self):
        self.device = WearableDevice(
            name="RoboWatch X1",
            device_type=DeviceType.SMARTWATCH,
            sensors=[SensorType.ACCELEROMETER, SensorType.HEART_RATE],
            battery_level_pct=85.0,
        )

    def test_record_and_get_readings(self):
        reading = SensorReading(SensorType.ACCELEROMETER, (0.1, 0.2, 9.8), "m/s²", 0)
        self.device.record_reading(reading)
        all_readings = self.device.get_readings()
        assert len(all_readings) == 1
        assert all_readings[0] is reading

    def test_get_readings_filtered_by_sensor(self):
        accel = SensorReading(SensorType.ACCELEROMETER, (1, 0, 0), "m/s²", 0)
        hr = SensorReading(SensorType.HEART_RATE, 80, "bpm", 0)
        self.device.record_reading(accel)
        self.device.record_reading(hr)

        accel_only = self.device.get_readings(SensorType.ACCELEROMETER)
        assert len(accel_only) == 1
        assert accel_only[0] is accel

    def test_clear_readings(self):
        self.device.record_reading(SensorReading(SensorType.TEMPERATURE, 37.0, "°C", 0))
        self.device.clear_readings()
        assert self.device.get_readings() == []

    def test_status_contains_device_name(self):
        status = self.device.status()
        assert "RoboWatch X1" in status
        assert "85.0" in status


class TestWearableTechIntegration:
    def setup_method(self):
        self.wt = WearableTechIntegration()

    def test_register_and_get_device(self):
        device = WearableDevice("Alien Suit", DeviceType.LIFE_SUPPORT_SUIT)
        self.wt.register_device(device)
        retrieved = self.wt.get_device("Alien Suit")
        assert retrieved is device

    def test_get_device_not_registered(self):
        assert self.wt.get_device("Nonexistent") is None

    def test_list_devices(self):
        d1 = WearableDevice("D1", DeviceType.AR_HEADSET)
        d2 = WearableDevice("D2", DeviceType.BIOSENSOR_PATCH)
        self.wt.register_device(d1)
        self.wt.register_device(d2)
        devices = self.wt.list_devices()
        assert d1 in devices
        assert d2 in devices

    def test_get_exercises_returns_list(self):
        exercises = self.wt.get_exercises()
        assert isinstance(exercises, list)
        assert len(exercises) >= 3  # built-in exercises

    def test_add_exercise(self):
        custom = WearableProgrammingExercise(
            title="Custom Exercise",
            description="desc",
            required_sensors=[SensorType.GPS],
            starter_code="pass",
            expected_outcome="It works.",
        )
        self.wt.add_exercise(custom)
        assert custom in self.wt.get_exercises()

    def test_get_exercises_for_sensors_subset(self):
        available = [SensorType.ACCELEROMETER, SensorType.GYROSCOPE, SensorType.EEG]
        exercises = self.wt.get_exercises_for_sensors(available)
        assert len(exercises) > 0
        for ex in exercises:
            for s in ex.required_sensors:
                assert s in available

    def test_get_exercises_for_sensors_empty_match(self):
        # No built-in exercise requires only GPS
        exercises = self.wt.get_exercises_for_sensors([SensorType.GPS])
        assert exercises == []

    def test_summarize_contains_header(self):
        summary = self.wt.summarize()
        assert "Wearable Tech" in summary
