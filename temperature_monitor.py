# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "HardwareMonitor",
# ]
# ///

import time
from HardwareMonitor.Util import OpenComputer
from config import CPU_TEMP_SENSOR_ID, GPU_TEMP_SENSOR_ID

class TemperatureMonitor:
    def __init__(self):
        self.computer = OpenComputer(cpu=True, gpu=True)
        self.cpu_temp_sensor_id = CPU_TEMP_SENSOR_ID
        self.gpu_temp_sensor_id = GPU_TEMP_SENSOR_ID
        
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def get_cpu_gpu_temperature(self):
        """获取CPU和GPU温度"""
        if not self.computer:
            return None, None
            
        try:
            self.computer.Update()
        except Exception:
            # If update fails, return None values
            return None, None
            
        cpu_temp, gpu_temp = None, None
        
        try:
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
        except Exception:
            # If there's an error accessing sensors, return what we have
            pass
        
        return cpu_temp, gpu_temp

    def close(self):
        """手动关闭资源"""
        if self.computer:
            try:
                self.computer.Close()
            except Exception:
                # Ignore errors when closing
                pass
            finally:
                self.computer = None

if __name__ == "__main__":
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