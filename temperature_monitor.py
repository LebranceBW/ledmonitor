# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "HardwareMonitor",
# ]
# ///

from HardwareMonitor.Util import OpenComputer


class TemperatureMonitor:
    def __init__(self, sensors_config=None):
        self.computer = OpenComputer(cpu=True, gpu=True)
        if sensors_config:
            self.cpu_temp_sensor_id = sensors_config.get(
                "cpu_temp_sensor_id", "/amdcpu/0/temperature/2"
            )
            self.gpu_temp_sensor_id = sensors_config.get(
                "gpu_temp_sensor_id", "/gpu-nvidia/0/temperature/0"
            )
        else:
            raise RuntimeError("sensors_config is required")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def get_cpu_gpu_temperature(self):
        if not self.computer:
            raise RuntimeError("Computer not initialized")
        self.computer.Update()
        cpu_temp, gpu_temp = None, None
        for hardware in self.computer.Hardware:
            for sensor in hardware.Sensors:
                identifier = sensor.Identifier.ToString()
                if identifier == self.cpu_temp_sensor_id:
                    cpu_temp = sensor.Value
                elif identifier == self.gpu_temp_sensor_id:
                    gpu_temp = sensor.Value

                # 如果都找到了就提前返回
                if cpu_temp is not None and gpu_temp is not None:
                    return cpu_temp, gpu_temp

        return cpu_temp, gpu_temp

    def close(self):
        self.computer.Close()


if __name__ == "__main__":
    import time

    try:
        with TemperatureMonitor() as monitor:
            while True:
                cpu_temp, gpu_temp = monitor.get_cpu_gpu_temperature()
                if cpu_temp is not None:
                    print(f"CPU Temperature: {cpu_temp:.1f}°C")
                else:
                    print("CPU Temperature: Not available")
                if gpu_temp is not None:
                    print(f"GPU Temperature: {gpu_temp:.1f}°C")
                else:
                    print("GPU Temperature: Not available")
                time.sleep(1)
    except KeyboardInterrupt:
        print("Monitoring stopped by user")
    except Exception as e:
        print(f"Error: {e}")
