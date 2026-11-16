import numpy as np
import struct
import asyncio
from bleak import BleakScanner, BleakClient
from WT901 import WT901

async def main():
    device = await BleakScanner.find_device_by_name("WT901BLE68", timeout=15)
    WIT = WT901()
    
    if device is None:
        print("Sensor not found")
        return
 
    async with BleakClient(device) as client:
        print("Connected:", client.is_connected)
        def notification_handler(sender,data):
            #print(f"Received {len(data)} bytes: {data.hex(' ')}")
            WIT.DoIt(data)
            print(WIT)
            
        await client.start_notify(
            "0000ffe4-0000-1000-8000-00805f9a34fb",
            notification_handler
            )
        print("Listening for sensor data...")
        await asyncio.sleep(15)
        await client.stop_notify(
            "0000ffe4-0000-1000-8000-00805f9a34fb"
            )

asyncio.run(main())
