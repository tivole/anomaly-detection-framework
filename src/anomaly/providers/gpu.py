import os
import sys
import clr
from logger import get_logger

try:
    import GPUtil
except ImportError:
    GPUtil = None

providers_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.append(providers_dir)
clr.AddReference("LibreHardwareMonitor/LibreHardwareMonitorLib")
from LibreHardwareMonitor.Hardware import Computer, HardwareType, SensorType

logger = get_logger(__name__)


def get_vram_usage() -> float:
    """
    Returns the GPU usage value in [0, 1] range.
    """
    if GPUtil is None:
        logger.warn(
            "GPUtil library is not installed. VRAM usage data won't be collected."
        )
        return 0.0

    gpus = GPUtil.getGPUs()
    if not gpus:
        logger.warn("No compatible GPUs found. VRAM usage data won't be collected.")
        return 0.0

    # Calculate average VRAM usage across all available GPUs
    total_vram_percent = sum(gpu.memoryUtil for gpu in gpus)
    avg_vram_usage = total_vram_percent / len(gpus)

    return avg_vram_usage


def get_gpu_temperature() -> float:
    temperature = 0.0

    comp = Computer()
    comp.IsGpuEnabled = True
    comp.Open()

    for hardware in comp.Hardware:
        if hardware.HardwareType == HardwareType.GpuNvidia:
            hardware.Update()
            for sensor in hardware.Sensors:
                if sensor.SensorType == SensorType.Temperature:
                    temperature = sensor.Value
                    if temperature:
                        comp.Close()
                        return temperature

    comp.Close()
    return temperature


def get_gpu_usage():
    gpu_usage = 0.0

    comp = Computer()
    comp.IsGpuEnabled = True
    comp.Open()

    for hardware in comp.Hardware:
        if hardware.HardwareType == HardwareType.GpuNvidia:
            hardware.Update()
            for sensor in hardware.Sensors:
                if sensor.SensorType == SensorType.Load:
                    gpu_usage = sensor.Value
                    if gpu_usage:
                        comp.Close()
                        return gpu_usage

    comp.Close()
    return gpu_usage
