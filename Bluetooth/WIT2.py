import numpy as np
import struct
import asyncio
from bleak import BleakScanner, BleakClient

class WT901:
    """
    @brief class container for WT901 interface,
    input agnostic. 
    """
    def __init__(self):
        """
        @brief constructor for class.
        """
        # allocate arrays for the return values
        self.acc = np.zeros(3)
        self.rph = np.zeros(3)
        self.mag = np.zeros(3)

    def __del__(self):
        """
        @brief - destructor, clean up at the end
        nothing at this time. 
        """

    def __str__(self):
        """
        @brief - format data into a string 
        """
        rv = f'{self.acc[0]:.1f}, {self.acc[1]:.1f}, {self.acc[2]:.1f}, {self.rph[0]:.1f}, {self.rph[1]:.1f}, {self.rph[2]:.1f}, {self.mag[0]:.4f}, {self.mag[1]:.4f}, {self.mag[2]:.4f}'
        return rv
   
    def DumpHex(self,data):
        """
        @brief - dump the data in hexadecimal format for debugging
        @param data - data acquired.
        """
        for val in data:
            print(f'{val:X} ', end=' ')
            if (val == 0x55):
                print('BOL! ', end = ' ')
                
    def Decode(self, data):
        """
        @brief - decode a string of data
        @param - data stream to decode
        @return int16 values in (X,Y,Z) triples. acceleration, rph, mag field

        The input data stream from the bluetooth system is 20 hex numbers
        there are 2 bytes of prefix followed by 18 bytes
        """
        prefix = data[0]
        # use the struct.unpack function to get 9 shorts (int 16)
        (vals) = struct.unpack('9h', data[2:])
        return vals

    def ScaleData(self,values):
        """
        @brief - Scale the data to appropriate floating values
        assume a specific order
        @param - values from decoding

        values are in 16 bit bipolar words. 
        """

        # leave in units of g, +/- 2g unless super big
        for i in range(3):
            self.acc[i] = values[i]/32768.0 * 16
            self.rph[i] = values[i+3]/32768.0 * 2000  # degrees/s
            self.mag[i] = values[i+6]/32768.0         # mg

    def DoIt(self, data):
        """
        pass in bytes of data. 
        """
        vals = self.Decode(data)
        self.ScaleData(vals)

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
