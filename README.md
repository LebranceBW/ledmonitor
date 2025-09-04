# LED Monitor for CPU and GPU

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Modified Xiaomi Smart Clock 3 mini to display CPU and GPU temperatures. You can also use it to display other data such as CPU usage, time, weather, or even the inventory of cola in your home.

![Example Image](./assest/example.jpg)

## Features

- Real-time monitoring and display of CPU and GPU temperatures
- Bluetooth connection to Xiaomi Smart Clock 3 mini
- Custom firmware flashing support
- Configurable sensor identifiers
- Supports Windows and other platforms

## Hardware Requirements

1. Xiaomi Smart Clock 3 mini (or other temperature/humidity meters that can flash ATC_MiThermometer firmware)
2. Computer with Bluetooth capability (Windows/Linux/MacOS)

## Software Dependencies

- Python 3.13+
- ATC_MiThermometer firmware (https://github.com/pvvx/ATC_MiThermometer)
- Related Python libraries (see [pyproject.toml](pyproject.toml))

## Installation Steps

### 1. Flash Firmware

Use the [ATC_MiThermometer](https://github.com/pvvx/ATC_MiThermometer) project to flash custom firmware to your Xiaomi Smart Clock 3 mini.

### 2. Clone Project

```bash
git clone <repository-url>
cd ledmonitor
```

### 3. Install Dependencies

It is recommended to use the `uv` tool to manage project dependencies and virtual environments:

```bash
# Use uv to install dependencies
uv sync
```

Or use pip:

```bash
pip install -r requirements.txt
```

### 4. Configure Device

Modify the [config/config.toml](config/config.toml) file:

```toml
# Update interval (seconds)
interval = 1
# Bluetooth connection timeout (seconds)
timeout = 30

[bluetooth]
# Your device's Bluetooth address (replace with your device's MAC address)
device_address = "XX:XX:XX:XX:XX:XX"
# Service UUID
service_uuid = "00001f10-0000-1000-8000-00805f9b34fb"
# Characteristic UUID
characteristic_uuid = "00001f1f-0000-1000-8000-00805f9b34fb"

[sensors]
# CPU temperature sensor identifier
cpu_temp_sensor_id = "/amdcpu/0/temperature/2"
# GPU temperature sensor identifier
gpu_temp_sensor_id = "/gpu-nvidia/0/temperature/0"
```

### 5. Run Program

```bash
# Run with uv
uv run ledmonitor.py

# Or run directly
python ledmonitor.py
```

## How It Works

1. Use the [bleak](https://github.com/hbldh/bleak) library to connect to the device via Bluetooth
2. Get system temperature data through [HardwareMonitor](https://github.com/LibreHardwareMonitor/LibreHardwareMonitor)
3. Encode temperature data into LCD display commands
4. Send commands to the temperature/humidity meter via Bluetooth for display

## Project Structure

```
ledmonitor/
├── config/              # Configuration directory
│   └── config.toml      # Main configuration file
├── config.py            # Configuration loading module
├── display_protocol.py  # LCD display protocol encoding
├── ledmonitor.py        # Main program
├── logger_config.py     # Logging configuration
├── temperature_monitor.py # Temperature monitoring module
└── pyproject.toml       # Project dependency configuration
```

## Troubleshooting

- Make sure the Bluetooth device is properly paired and discoverable
- Check that the device address is correctly configured
- Confirm that the ATC_MiThermometer firmware has been successfully flashed
- Check the log file `logs/ledmonitor.log` for more information

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.