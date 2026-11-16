"""
Modified   BY     Reason
--------   --     -----
27-June-25 CBL    Original, play with the python bluetooth toolkit and
                  learn how to send data between bluetooth devices.

References:
    https://pypi.org/project/bleak/
    https://randomnerdtutorials.com/esp32-ble-server-client/
    https://www.bluetooth.com/specifications/assigned-numbers/
    https://docs.python.org/3/library/asyncio.html
"""
# My standard imports
import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as konst
import math

import asyncio
from bleak import BleakClient

# Going to try and connect to the ESP32 device.
# DF024462-7326-2EB4-7FA7-8730468BF632: Long name works now
# The title is given by me in the XIAO ESP32 program
# 
address = "e4:b3:23:ac:8e:5e"
CHARACTERISTIC_UUID="beb5483e-36e1-4688-b7f5-ea07361b26a8"
DATA_UUID = "f416b7eb-be2f-49f3-aaaf-96150769d25d"

async def main(address):
    async with BleakClient(address) as client:
        print('BleakClient')
        something = await client.read_gatt_char(CHARACTERISTIC_UUID)
        print("something: {0}".format("".join(map(chr, something))))
        data = await client.read_gatt_char(CHARACTERISTIC_UUID)
        print("Data: {0}".format("".join(map(chr, data))))

print(address);
asyncio.run(main(address))
