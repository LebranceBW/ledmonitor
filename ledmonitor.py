import asyncio
import sys
from bleak import BleakClient
from config import settings
from display_protocol import encode_lcd_display
from logger_config import logger
from temperature_monitor import TemperatureMonitor


async def main():
    device_address = settings.bluetooth.device_address
    service_uuid = settings.bluetooth.service_uuid
    characteristic_uuid = settings.bluetooth.characteristic_uuid
    timeout = settings.timeout
    sensors_config = settings.sensors
    interval = settings.interval
    logger.info(f"Using sensors configuration: {sensors_config}")

    # 连接到设备
    logger.info(f"Connecting to {device_address}...")
    async with BleakClient(device_address, timeout=timeout) as client:
        if not client.is_connected:
            logger.error("Connection failed!")
            return

        logger.info(f"Connected to {device_address}")

        # 获取服务和特征
        service = client.services.get_service(service_uuid)
        if not service:
            logger.error(f"Service {service_uuid} not found")
            return

        characteristic = service.get_characteristic(characteristic_uuid)
        if not characteristic:
            logger.error(
                f"Characteristic {characteristic_uuid} not found in service {service_uuid}"
            )
            return

        logger.info(
            f"Found service {service.uuid} and characteristic {characteristic.uuid}"
        )

        # 创建温度监控器，传递 sensors 配置
        with TemperatureMonitor(sensors_config) as monitor:
            flash = True
            logger.info(
                f"Starting temperature monitoring loop with {interval}s interval"
            )
            while True:
                try:
                    # 获取温度数据
                    cpu, gpu = monitor.get_cpu_gpu_temperature()
                    logger.debug(f"Retrieved temperatures - CPU: {cpu}, GPU: {gpu}")

                    # 构建并发送数据
                    data = encode_lcd_display(cpu, gpu, flash)
                    flash = not flash

                    if data:
                        await client.write_gatt_char(characteristic, data, True)
                        logger.info(f"Data sent to device - CPU: {cpu}°C, GPU: {gpu}°C")
                    else:
                        logger.warning("No data to send to device")

                    # 等待指定的时间间隔
                    await asyncio.sleep(interval)

                except KeyboardInterrupt:
                    logger.info("Interrupted by user")
                    break
                except Exception as e:
                    logger.error(f"Error during monitoring loop: {e}", exc_info=True)
                    # 出错后等待一段时间再继续
                    await asyncio.sleep(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
    except Exception as e:
        logger.error(f"Unhandled error: {e}", exc_info=True)
        sys.exit(1)
