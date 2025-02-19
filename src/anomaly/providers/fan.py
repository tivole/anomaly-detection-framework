import os
import ctypes

current_dir = os.path.abspath(os.path.dirname(__file__))
dll_path = os.path.join(current_dir, "AsusWinIO/AsusWinIO64.dll")

try:
    asus_winio = ctypes.WinDLL(dll_path)
except Exception as e:
    raise RuntimeError(f"Failed to load AsusWinIO64.dll: {e}")


def get_cpu_fan_speed():
    asus_winio.InitializeWinIo()
    asus_winio.HealthyTable_SetFanIndex(0)
    fan_speed = asus_winio.HealthyTable_FanRPM()
    asus_winio.ShutdownWinIo()
    return fan_speed


def get_gpu_fan_speed():
    asus_winio.InitializeWinIo()
    asus_winio.HealthyTable_SetFanIndex(1)
    fan_speed = asus_winio.HealthyTable_FanRPM()
    asus_winio.ShutdownWinIo()
    return fan_speed
