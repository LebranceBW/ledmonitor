# Configuration file for LED Monitor

# Bluetooth device configuration
DEVICE_ADDRESS = "a4:c1:38:1b:1b:27"
SERVICE_UUID = "00001f10-0000-1000-8000-00805f9b34fb"
CHARACTERISTIC_UUID = "00001f1f-0000-1000-8000-00805f9b34fb"

# Sensor IDs
CPU_TEMP_SENSOR_ID = "/amdcpu/0/temperature/2"  # Core (Tctl/Tdie)
GPU_TEMP_SENSOR_ID = "/gpu-nvidia/0/temperature/0"  # GPU Core

# Default display configuration
DEFAULT_DISPLAY_CONFIG = {
    "smiley": 1,      # (^_^)
    "battery": False,
    "percent": False,
    "tmpsmb": 4,      # _
    "vtimed": 5000,
    "hwver_id": 10
}