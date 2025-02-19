import psutil


def get_disk_read_bytes() -> int:
    """
    Returns the disk read speed in bytes per second.
    """
    disk_io = psutil.disk_io_counters()
    if disk_io:
        return disk_io.read_bytes
    else:
        return 0


def get_disk_write_bytes() -> int:
    """
    Returns the disk write speed in bytes per second.
    """
    disk_io = psutil.disk_io_counters()
    if disk_io:
        return disk_io.write_bytes
    else:
        return 0
