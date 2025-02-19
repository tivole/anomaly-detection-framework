import psutil


def get_ram_usage() -> float:
    """
    Returns the CPU usage value in [0, 1] range.
    """
    return psutil.virtual_memory().percent / 100.0
