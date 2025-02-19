import psutil


def get_total_processes_count() -> int:
    """
    Returns the total number of processes.
    """
    return len(psutil.pids())


def get_total_threads_count() -> int:
    """
    Returns the total number of threads.
    """
    total_threads = 0
    for pid in psutil.pids():
        try:
            proc = psutil.Process(pid)
            total_threads += len(proc.threads())
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            # Skip processes that we don't have permission to inspect or that have ended.
            continue
    return total_threads


def get_total_handles_count() -> int:
    """
    Returns the total number of handles.
    """
    total_handles = 0
    for pid in psutil.pids():
        try:
            proc = psutil.Process(pid)
            total_handles += proc.num_handles()
        except (psutil.AccessDenied, psutil.NoSuchProcess, psutil.ZombieProcess):
            # Skip processes that we can't inspect.
            continue
    return total_handles
