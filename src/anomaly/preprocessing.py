import copy
from typing import Any

from .providers.cpu import get_cpu_min_speed, get_cpu_max_speed
from .collection import MonitoredFeature


class CriticalValue:
    def __init__(self, min: float, max: float) -> None:
        self.min = min
        self.max = max


class DataPreprocessor:
    _monitored_features_critical_values: dict[MonitoredFeature, CriticalValue]

    def __init__(self, monitored_features: list[MonitoredFeature]) -> None:
        self._monitored_features = monitored_features
        self._monitored_features_critical_values = {}

    def normalize(self, telemetry_data: list[dict]) -> list[dict]:
        """
        Normalize the data using min-max normalization.

        Instead of modifying the original telemetry_data, this method creates a deep copy,
        performs normalization on the copy, and returns it.
        """
        # Create a deep copy of the telemetry data so the original is not modified.
        normalized_data = copy.deepcopy(telemetry_data)

        if len(normalized_data) == 0:
            return normalized_data

        # Determine the critical (min, max) values for each monitored feature.
        for feature in self._monitored_features:
            min_value = normalized_data[0][feature]
            max_value = normalized_data[0][feature]
            for telemetry in normalized_data:
                min_value = min(min_value, telemetry[feature])
                max_value = max(max_value, telemetry[feature])
            self._monitored_features_critical_values[feature] = CriticalValue(
                min_value, max_value
            )

        if "cpu_speed" in self._monitored_features:
            cpu_min_speed = get_cpu_min_speed()
            cpu_max_speed = get_cpu_max_speed()
            self._monitored_features_critical_values["cpu_speed"] = CriticalValue(
                cpu_min_speed, cpu_max_speed
            )

        if "cpu_temperature" in self._monitored_features:
            self._monitored_features_critical_values["cpu_temperature"] = CriticalValue(
                25.0, 100.0
            )

        if "gpu_temperature" in self._monitored_features:
            self._monitored_features_critical_values["gpu_temperature"] = CriticalValue(
                25.0, 100.0
            )

        if "cpu_fan_speed" in self._monitored_features:
            self._monitored_features_critical_values["cpu_fan_speed"] = CriticalValue(
                0.0, 7500.0
            )

        if "gpu_fan_speed" in self._monitored_features:
            self._monitored_features_critical_values["gpu_fan_speed"] = CriticalValue(
                0.0, 7500.0
            )

        # Normalize each telemetry record in the copied data.
        for telemetry in normalized_data:
            for feature in self._monitored_features:
                telemetry[feature] = self._normalize_feature(
                    feature, telemetry[feature]
                )

        return normalized_data

    def normalize_single(self, telemetry: dict) -> dict:
        """
        Normalize a single telemetry data point using min-max normalization.

        Instead of modifying the input telemetry, this method creates a deep copy,
        normalizes the copy, and returns it.
        """
        telemetry_copy = copy.deepcopy(telemetry)
        for feature in self._monitored_features:
            telemetry_copy[feature] = self._normalize_feature(
                feature, telemetry_copy[feature]
            )
        return telemetry_copy

    def _normalize_feature(self, feature: MonitoredFeature, value: Any) -> float:
        """
        Normalize the given feature value using min-max normalization.
        """
        if feature in ["cpu_usage", "ram_usage", "vram_usage"]:
            return value

        min_value = self._monitored_features_critical_values[feature].min
        max_value = self._monitored_features_critical_values[feature].max

        # Take 20% of the range as the buffer to avoid normalization errors.
        min_value -= 0.25 * (max_value - min_value)
        max_value += 0.25 * (max_value - min_value)

        # Ensure the value is within the range [min_value, max_value].
        if min_value < 0:
            min_value = 0

        # Avoid division by zero in case min_value == max_value.
        if max_value == min_value:
            return 0.0

        res = (value - min_value) / (max_value - min_value)

        if res < 0:
            return 0.0

        if res > 1:
            return 1.0

        return res
