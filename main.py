import asyncio
from bleak import BleakClient
from display_protocol import ExtData, build_blk
from temperature_monitor import TemperatureMonitor
from config import DEVICE_ADDRESS, SERVICE_UUID, CHARACTERISTIC_UUID, DEFAULT_DISPLAY_CONFIG
import time

# 要写入的数据 (十六进制字符串转换为字节)
def build_data(cpu, gpu):
    return build_blk(ExtData(
        enable=DEFAULT_DISPLAY_CONFIG.get("enable", True),
        bignumb=cpu if cpu is not None else 0,
        smalnumb=gpu if gpu is not None else 0,
        smiley=DEFAULT_DISPLAY_CONFIG.get("smiley", 1),
        battery=DEFAULT_DISPLAY_CONFIG.get("battery", False),
        percent=DEFAULT_DISPLAY_CONFIG.get("percent", False),
        tmpsmb=DEFAULT_DISPLAY_CONFIG.get("tmpsmb", 4),
        vtimed=DEFAULT_DISPLAY_CONFIG.get("vtimed", 1000),
    ))

async def main():
    # 连接到设备
    print(f"Connecting to {DEVICE_ADDRESS}...")
    try:
        async with BleakClient(DEVICE_ADDRESS, timeout=30, winrt={"address_type": "public"}) as client:
            if not client.is_connected:
                print("Connection failed!")
                return

            print(f"Connected to {DEVICE_ADDRESS}")
            
            # 获取服务和特征
            services = client.services
            service = services.get_service(SERVICE_UUID)
            if not service:
                print(f"Service {SERVICE_UUID} not found")
                return
                
            characteristic = service.get_characteristic(CHARACTERISTIC_UUID)
            if not characteristic:
                print(f"Characteristic {CHARACTERISTIC_UUID} not found in service {SERVICE_UUID}")
                return
                
            print(f"Found service {service.uuid} and characteristic {characteristic.uuid}")
            
            # 创建温度监控器
            with TemperatureMonitor() as monitor:
                while True:
                    try:
                        # 获取温度数据
                        cpu, gpu = monitor.get_cpu_gpu_temperature()
                        
                        # 构建并发送数据
                        data = build_data(cpu, gpu)
                        if data:
                            await client.write_gatt_char(characteristic, data, True)
                            print(f"CPU temp {cpu if cpu is not None else 'N/A'}, GPU temp {gpu if gpu is not None else 'N/A'}")
                            print(f"Successfully wrote data to characteristic {CHARACTERISTIC_UUID}")
                            print(f"Data written: {data.hex()}")
                        else:
                            print("No data to send (extension disabled)")
                        
                        # 等待1秒
                        await asyncio.sleep(3)
                        
                    except Exception as e:
                        print(f"Error during operation: {e}")
                        # 继续循环而不是退出
                        await asyncio.sleep(1)
                        
    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        print("Disconnecting...")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Program interrupted by user")
    except Exception as e:
        print(f"Program error: {e}")