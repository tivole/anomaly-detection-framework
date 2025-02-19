import psutil


def get_network_bytes_sent() -> int:
    """
    Returns the number of bytes sent over the network.
    """
    return psutil.net_io_counters().bytes_sent


def get_network_bytes_received() -> int:
    """
    Returns the number of bytes received over the network.
    """
    return psutil.net_io_counters().bytes_recv


def get_network_packets_sent() -> int:
    """
    Returns the number of packets sent over the network.
    """
    return psutil.net_io_counters().packets_sent


def get_network_packets_received() -> int:
    """
    Returns the number of packets received over the network.
    """
    return psutil.net_io_counters().packets_recv


def get_network_total_active_connections() -> int:
    """
    Returns the total number of active network connections.
    """
    return len(psutil.net_connections())
