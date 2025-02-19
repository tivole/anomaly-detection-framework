import sys
import os

src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))

if src_path not in sys.path:
    sys.path.insert(0, src_path)


from anomaly.methods.zscore import ZScore
from anomaly.methods.gaussian_mixture import (
    GaussianMixtureWithThreshold as GaussianMixture,
)
from anomaly.methods.average_rule import AverageRule
from anomaly.methods.max_rule import MaxRule
from anomaly.methods.one_class_svm import OneClassSVMWrapper as OneClassSVM
from anomaly.module import AnomalyDetectionModule
from anomaly.detector import Detector
from logger import get_logger

logger = get_logger(__name__)


def anomaly_callback(alert: dict) -> None:
    logger.info(f"\n---------------------------------")
    logger.info(f"-                               -")
    logger.info(f"\tAnomaly detected: {alert}")
    logger.info(f"-                               -")
    logger.info(f"---------------------------------\n")


def main():
    anomaly_module = AnomalyDetectionModule(
        use_db=False,
        initial_learning_period_seconds=900,
        retraining_interval_seconds=300,
        alert_callback=anomaly_callback,
        detection_threshold=2,
        monitored_features=[
            "cpu_usage",
            "cpu_speed",
            "cpu_temperature",
            "cpu_fan_speed",
            "ram_usage",
            "vram_usage",
            "gpu_usage",
            "gpu_temperature",
            "gpu_fan_speed",
            "disk_read_bytes",
            "disk_write_bytes",
            "network_bytes_sent",
            "network_bytes_received",
            "network_packets_sent",
            "network_packets_received",
        ],
    )

    # Add Z-Score method to the module
    anomaly_module.add_detector(
        Detector(
            method=ZScore(
                n=3,
                threshold=1.5,
            ),
            features=[
                "cpu_usage",
                "cpu_speed",
                "disk_read_bytes",
                "disk_write_bytes",
                "network_bytes_sent",
                "network_bytes_received",
                "network_packets_sent",
                "network_packets_received",
            ],
        )
    )

    # Add GaussianMixture method to the module
    anomaly_module.add_detector(
        Detector(
            method=GaussianMixture(
                n_components=3,
                covariance_type="full",
                threshold=-2.0,
            ),
            features=[
                "cpu_usage",
                "cpu_speed",
                "disk_read_bytes",
                "disk_write_bytes",
                "network_bytes_sent",
                "network_bytes_received",
                "network_packets_sent",
                "network_packets_received",
            ],
        )
    )

    # Add AverageRule method to the module
    anomaly_module.add_detector(
        Detector(
            method=AverageRule(
                n=4,
                threshold=0.25,
            ),
            features=[
                "cpu_usage",
                "cpu_temperature",
                "cpu_speed",
                "cpu_fan_speed",
            ],
        )
    )

    # Add MaxRule method to the module
    anomaly_module.add_detector(
        Detector(
            method=MaxRule(
                n=2,
                threshold=0.05,
            ),
            features=[
                "cpu_usage",
                "cpu_temperature",
                "cpu_speed",
                "cpu_fan_speed",
                "vram_usage",
                "gpu_temperature",
                "gpu_fan_speed",
            ],
        )
    )

    # Add MaxRule method to the module
    anomaly_module.add_detector(
        Detector(
            method=OneClassSVM(
                kernel="rbf",
                nu=0.001,
                gamma="scale",
            ),
            features=[
                "cpu_usage",
                "cpu_temperature",
                "cpu_speed",
                "cpu_fan_speed",
                "vram_usage",
                "gpu_temperature",
                "gpu_fan_speed",
            ],
        )
    )

    # Start the anomaly detection process
    anomaly_module.process()


if __name__ == "__main__":
    main()
