from typing import Literal, Callable, Any

from .providers.cpu import get_cpu_usage, get_cpu_speed, get_cpu_temperature
from .providers.gpu import get_gpu_usage, get_gpu_temperature, get_vram_usage
from .providers.fan import get_cpu_fan_speed, get_gpu_fan_speed
from .providers.memory import get_ram_usage
from .providers.disk import get_disk_read_bytes, get_disk_write_bytes
from .providers.network import (
    get_network_bytes_received,
    get_network_bytes_sent,
    get_network_packets_received,
    get_network_packets_sent,
    get_network_total_active_connections,
)
from .providers.process import (
    get_total_processes_count,
    get_total_threads_count,
    get_total_handles_count,
)

MonitoredFeature = Literal[
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
    "network_total_active_connections",
    "total_processes_count",
    "total_threads_count",
    "total_handles_count",
]

MonitoredFeatureCollector: dict[MonitoredFeature, Callable[[], Any]] = {
    "cpu_usage": get_cpu_usage,
    "cpu_speed": get_cpu_speed,
    "cpu_fan_speed": get_cpu_fan_speed,
    "cpu_temperature": get_cpu_temperature,
    "ram_usage": get_ram_usage,
    "vram_usage": get_vram_usage,
    "gpu_usage": get_gpu_usage,
    "gpu_temperature": get_gpu_temperature,
    "gpu_fan_speed": get_gpu_fan_speed,
    "disk_read_bytes": get_disk_read_bytes,
    "disk_write_bytes": get_disk_write_bytes,
    "network_bytes_sent": get_network_bytes_sent,
    "network_bytes_received": get_network_bytes_received,
    "network_packets_sent": get_network_packets_sent,
    "network_packets_received": get_network_packets_received,
    "network_total_active_connections": get_network_total_active_connections,
    "total_processes_count": get_total_processes_count,
    "total_threads_count": get_total_threads_count,
    "total_handles_count": get_total_handles_count,
}
