import asyncio
from bleak import BleakScanner, BleakClient


async def main():
    device = await BleakScanner.find_device_by_name("WT901BLE68", timeout=15)
    if device is None:
        print("Sensor not found")
        return
 
    async with BleakClient(device) as client:
        print("Connected:", client.is_connected)
 
        for service in client.services:
            print("Service:", service.uuid)
 
            for char in service.characteristics:
                print("  Characteristic:", char.uuid)
                print("  Properties:", char.properties)

asyncio.run(main())
