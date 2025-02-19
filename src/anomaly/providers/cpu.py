import os
import sys
import psutil
import clr

providers_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.append(providers_dir)
clr.AddReference("LibreHardwareMonitor/LibreHardwareMonitorLib")
from LibreHardwareMonitor.Hardware import Computer, HardwareType, SensorType


def get_cpu_usage(interval: int = 1) -> float:
    """
    Returns the CPU usage value in [0, 1] range.
    """
    return psutil.cpu_percent(interval=interval) / 100.0


def get_cpu_max_speed() -> float:
    """
    Returns the maximum CPU speed in MHz using psutil.
    """
    freq = psutil.cpu_freq()
    return freq.max if freq and freq.max else 0.0


def get_cpu_min_speed() -> float:
    """
    Returns the minimum CPU speed in MHz using psutil.
    """
    freq = psutil.cpu_freq()
    return freq.min if freq and freq.min else 0.0


def get_cpu_temperature() -> float:
    temperature = 0.0

    comp = Computer()
    comp.IsCpuEnabled = True
    comp.Open()

    for hardware in comp.Hardware:
        if hardware.HardwareType == HardwareType.Cpu:
            hardware.Update()
            for sensor in hardware.Sensors:
                if sensor.SensorType == SensorType.Temperature:
                    temperature = sensor.Value
                    if temperature:
                        comp.Close()
                        return temperature

    comp.Close()
    return temperature


def get_cpu_speed() -> float:
    cpu_speed = 0.0

    comp = Computer()
    comp.IsCpuEnabled = True
    comp.Open()

    for hardware in comp.Hardware:
        if hardware.HardwareType == HardwareType.Cpu:
            hardware.Update()
            for sensor in hardware.Sensors:
                if sensor.SensorType == SensorType.Clock:
                    cpu_speed = sensor.Value
                    if cpu_speed:
                        comp.Close()
                        return cpu_speed

    comp.Close()
    return cpu_speed
