from datetime import datetime, timezone
from enum import Enum
import time
import json
from typing import get_args, Callable, Optional

from . import database
from .preprocessing import DataPreprocessor
from .detector import Detector
from .collection import MonitoredFeature, MonitoredFeatureCollector
from logger import get_logger

logger = get_logger(__name__)


class DetectionState(Enum):
    LEARNING = 0
    DETECTING = 1
    TRAINING = 2


class AnomalyDetectionModule:
    _DEFAULT_FEATURES_LIST: list[MonitoredFeature] = list(get_args(MonitoredFeature))
    _MIN_COLLECTION_INTERVAL_SECONDS: int = 3

    _detectors: list[Detector] = []
    _detection_state: DetectionState = DetectionState.LEARNING
    _initial_learning_start_time: datetime
    _last_training_time: datetime
    _telemetry_data: list[dict] = []

    def __init__(
        self,
        initial_learning_period_seconds: int = 3600,
        retraining_interval_seconds: int = 900,
        collection_interval_seconds: int = 5,
        detection_threshold: int = 1,
        monitored_features: list[MonitoredFeature] = _DEFAULT_FEATURES_LIST,
        use_db: bool = False,
        db_url: str = "sqlite:///telemetry.db",
        alert_callback: Optional[Callable[[dict], None]] = None,
    ) -> None:
        if collection_interval_seconds < self._MIN_COLLECTION_INTERVAL_SECONDS:
            raise ValueError(
                f"Collection interval must be at least {self._MIN_COLLECTION_INTERVAL_SECONDS} seconds."
            )

        self._initial_learning_period_seconds = initial_learning_period_seconds
        self._retraining_interval_seconds = retraining_interval_seconds
        self._collection_interval_seconds = collection_interval_seconds
        self._detection_threshold = detection_threshold
        self._monitored_features = monitored_features
        self._preprocessor = DataPreprocessor(monitored_features)
        self._alert_callback = alert_callback

        self._use_db = use_db
        if self._use_db:
            self._db_session_factory = database.init_db(db_url)
            logger.info("Database enabled. Using DB URL:", db_url)

    def add_detector(self, detector: Detector) -> None:
        self._detectors.append(detector)

    def process(self) -> None:
        self._start_initial_learning()

        while True:
            current_time = datetime.now(timezone.utc)
            elapsed_time = current_time - self._initial_learning_start_time
            elapsed_time_seconds = elapsed_time.total_seconds()

            if elapsed_time_seconds >= self._collection_interval_seconds:
                telemetry = self._collect_telemetry()

                # LEARNING state
                if self._detection_state == DetectionState.LEARNING:
                    learning_time = current_time - self._initial_learning_start_time
                    learning_time_seconds = learning_time.total_seconds()

                    if learning_time_seconds >= self._initial_learning_period_seconds:
                        self._detection_state = DetectionState.TRAINING

                    self._telemetry_data.append(telemetry)
                    if self._use_db:
                        self._write_to_db(telemetry)

                # TRAINING state
                elif self._detection_state == DetectionState.TRAINING:
                    self._train()
                    logger.info(
                        f"Initial learning completed at {current_time}. Starting detection."
                    )
                    self._detection_state = DetectionState.DETECTING

                # DETECTION state
                elif self._detection_state == DetectionState.DETECTING:
                    retraining_time = current_time - self._last_training_time
                    retraining_time_seconds = retraining_time.total_seconds()

                    if retraining_time_seconds >= self._retraining_interval_seconds:
                        self._detection_state = DetectionState.TRAINING

                    is_anomaly = self._predict(telemetry)
                    if is_anomaly:
                        logger.info(f"Anomaly detected at {current_time}.")
                        if self._alert_callback:
                            self._alert_callback(telemetry)
                    else:
                        self._telemetry_data.pop(0)
                        self._telemetry_data.append(telemetry)
                        if self._use_db:
                            self._write_to_db(telemetry)

            time.sleep(0.5)

    def _collect_telemetry(self) -> dict:
        """
        Collects telemetry data of monitored features and returns it.
        """
        telemetry_data = {}
        telemetry_data["timestamp"] = datetime.now(timezone.utc)
        for monitored_feature in self._monitored_features:
            telemetry_data[monitored_feature] = MonitoredFeatureCollector[
                monitored_feature
            ]()
        logger.info(f"Collected Data - {telemetry_data}")
        return telemetry_data

    def _train(self) -> None:
        """
        Trains the detectors with the telemetry data.
        """
        normalized_telemetry_data = self._preprocessor.normalize(self._telemetry_data)
        for detector in self._detectors:
            detector.fit(normalized_telemetry_data)
        self._last_training_time = datetime.now(timezone.utc)

    def _predict(self, telemetry: dict) -> bool:
        normalized_telemetry = self._preprocessor.normalize_single(telemetry)
        predictions_sum = 0
        for detector in self._detectors:
            prediction = detector.predict(normalized_telemetry)
            predictions_sum += prediction
            logger.info(f"Prediction of {detector.get_name()} - {prediction}")
        is_anomaly = predictions_sum >= self._detection_threshold
        logger.info(f"Anomaly: {is_anomaly}")
        return is_anomaly

    def _write_to_db(self, telemetry_data: dict) -> None:
        """
        Writes telemetry data into the database as a new record.
        """
        from .database import TelemetryData

        session = self._db_session_factory()
        try:
            record = TelemetryData(
                timestamp=telemetry_data["timestamp"],
                data=json.dumps(
                    telemetry_data,
                    default=lambda o: o.isoformat() if hasattr(o, "isoformat") else o,
                ),
            )
            session.add(record)
            session.commit()
            logger.info("Telemetry data written to database.")
        except Exception as e:
            session.rollback()
            logger.info("Error writing telemetry data to database:", e)
        finally:
            session.close()

    def _start_initial_learning(self) -> None:
        if self._detection_state != DetectionState.LEARNING:
            raise Exception("Initial learning can only be started in LEARNING state.")
        self._initial_learning_start_time = datetime.now(timezone.utc)
        logger.info(f"Initial learning started at {self._initial_learning_start_time}")
