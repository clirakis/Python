"""
 ####################################################################
  WT901.py

  Class for unpacking WIT 901 9DOF sensor
  for rendering.

  Modified   By   Reason
  --------   --   ------
  15-Nov-26  CBL  Original

  References:
  
  Notes:
  Commands for future reference, page 19 in manual
  FF AA 27 40 00 - Read Temperature
  FF AA 01 01 00 - Accelerometer calibration
  FF AA 01 07 00 - Magnetic Calibration
  FF AA 01 00 00 - Quit calibration
  FF AA 00 xx 00 - Save or restore  xx = 0 Save config, xx = 1 restore default
  FF AA 03 RR 00 - Set rate, default is 10 Hz


  ####################################################################
"""
# IMPORTS
import numpy as np
import struct
import asyncio

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
        self.acc = np.zeros(3)  # acceleration
        self.w   = np.zeros(3)  # rate of rotation around various axis
        self.rpy = np.zeros(3)  # sensor fused data. RPY

    def __del__(self):
        """
        @brief - destructor, clean up at the end
        nothing at this time. 
        """

    def __str__(self):
        """
        @brief - format data into a string 
        """
        rv = f'{self.acc[0]:.1f}, {self.acc[1]:.1f}, {self.acc[2]:.1f}, {self.w[0]:.1f}, {self.w[1]:.1f}, {self.w[2]:.1f}, {self.rpy[0]:.4f}, {self.rpy[1]:.4f}, {self.rpy[2]:.4f}'
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
            self.w[i]   = values[i+3]/32768.0 * 2000.  # degrees/s
            self.rpy[i] = values[i+6]/32768.0 * 180.0  # rpy

    def DoIt(self, data):
        """
        pass in bytes of data. 
        """
        vals = self.Decode(data)
        self.ScaleData(vals)
