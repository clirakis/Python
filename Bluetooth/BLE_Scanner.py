"""
BLE_Scanner.py

Modified   BY     Reason
--------   --     -----
27-June-25 CBL    Original, play with the python bluetooth toolkit and
                  learn how to send data between bluetooth devices.

References:
    https://pypi.org/project/bleak/
    https://randomnerdtutorials.com/esp32-ble-server-client/
    https://www.bluetooth.com/specifications/assigned-numbers/
    https://docs.python.org/3/library/asyncio.html
    https://bleak.readthedocs.io/en/latest/api/scanner.html


"""
# My standard imports
import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as konst
import math

import asyncio
from bleak import BleakScanner

async def main():
    devices = await BleakScanner.discover()
    for d in devices:
        #print(dir(d))
        # on MacOS the address is not the MAC address!!!
        print("MAC: ", d.address)
        print(d.details)

asyncio.run(main())
