import multiprocessing
import time
import math
import random
import os
import socket


def cpu_stressor():
    """
    A CPU-bound task that continuously performs floating-point computations.
    """
    x = 1.0
    while True:
        # Perform heavy computations in a tight loop.
        for _ in range(10**6):
            x = math.sin(x) * math.cos(x) + math.tan(x)
        # Prevent the value from getting too big or optimized away.
        if x == 0:
            print(x)


def ram_stressor():
    """
    A memory-bound task that continuously allocates large blocks of memory.
    """
    blocks = []
    while True:
        try:
            # Allocate a block of 1 million floats (~8MB if each float is 8 bytes)
            block = [random.random() for _ in range(10**6)]
            blocks.append(block)
            # Sleep briefly to allow the process to allocate memory steadily.
            time.sleep(0.05)
        except MemoryError:
            # Once memory is exhausted, clear some of it to continue the cycle.
            blocks.clear()


def disk_stressor():
    """
    A disk-bound task that continuously writes to a file.
    """
    filename = os.path.join(os.getcwd(), "disk_stressor.log")
    while True:
        try:
            with open(filename, "a") as f:
                f.write(f"Disk I/O stress test at {time.time()}\n")
        except Exception:
            pass
        time.sleep(0.001)


def network_stressor():
    """
    A network-bound task that continuously sends UDP packets to localhost.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    target = ("127.0.0.1", 9999)  # Use a port that is safe on your system.
    message = b"Network stress test"
    while True:
        try:
            sock.sendto(message, target)
        except Exception:
            pass
        time.sleep(0.0001)


def main():
    print(
        "WARNING: This program will use a huge amount of CPU, RAM, disk, and network resources!"
    )
    print("Run only in a controlled environment (e.g., a virtual machine).")

    processes = []

    # Determine the number of CPU cores and spawn more processes to stress the CPU.
    cpu_count = os.cpu_count() or 4
    num_cpu_processes = (
        cpu_count * 3
    )  # Adjust multiplier as needed for higher CPU load.

    print(f"Spawning {num_cpu_processes} CPU stress processes.")
    for _ in range(num_cpu_processes):
        p = multiprocessing.Process(target=cpu_stressor)
        p.start()
        processes.append(p)

    # Spawn several processes to aggressively consume memory.
    num_ram_processes = 4  # Adjust number of RAM stressors as needed.
    print(f"Spawning {num_ram_processes} RAM stress processes.")
    for _ in range(num_ram_processes):
        p = multiprocessing.Process(target=ram_stressor)
        p.start()
        processes.append(p)

    # Optionally, spawn disk and network stress processes.
    p_disk = multiprocessing.Process(target=disk_stressor)
    p_disk.start()
    processes.append(p_disk)

    p_network = multiprocessing.Process(target=network_stressor)
    p_network.start()
    processes.append(p_network)

    print("High resource usage simulation started. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Terminating stress test...")
        for p in processes:
            p.terminate()
        for p in processes:
            p.join()
        print("Stress test terminated.")


if __name__ == "__main__":
    main()
