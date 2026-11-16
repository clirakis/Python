"""
 ####################################################################
  BlochWIT.py

  Using UDP/OSC send data from the WIT 9DOF sensor and pass it
  along to Touch designer for rendering.


  Modified   By   Reason
  --------   --   ------
  15-Nov-26  CBL  Original

  References:
  OSC/UDP interface 
     https://docs.cycling74.com/legacy/max5/refpages/max-ref/udpreceive.html
     https://python-osc.readthedocs.io/en/latest/"
     https://python-osc.readthedocs.io/en/latest/client.html#module-pythonosc.udp_client"

  Make sure you have the python interface

     pip install python_osc  
  
  Notes:
      https://python-osc.readthedocs.io/en/stable/server.html
      may want to use asyncio example
  ####################################################################
"""
# imports
import numpy as np
from pythonosc import dispatcher, osc_server
from pythonosc.udp_client import SimpleUDPClient
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
import time
import threading
from bleak import BleakScanner, BleakClient
import asyncio

# Local includes
from TxOSC import TxOSC
from WT901 import WT901

# Global variable. May not need. 
ThreadRun = True
iFreq = 110.0

def Halt(address, *args):
    """
    Shutdown this server
    """
    print('HALT!')
    global server
    ThreadRun = False
    threading.Thread(target=server.shutdown, daemon=True).start()

def Gimme(address, *args):
    """
    example of a general request. 
    """
    global Tx
    global iFreq
    Tx.FreqPhase(iFreq, 0.0)
    iFreq = iFreq * 2
    
def EventHandler(address, *args):
    """
    This is the callback function for the dispatcher.
    For each UDP packet received, it will be called.
    My intent here is that this looks for the /COMMAND prefix to
    tell this program something to do. EG if it is qiskit
    give me some more samples.
    @param address - the address prefix from the OSC message
    @param *args   - this may be a list of arguments of any type. 
    """
    global Tx
    print(f"Received: {address}, Arguments: {args}")

async def BT_GetData():
    """
    a thread to recieve bluetooth data from the WT901 sensor.
    """
    global Tx
    
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
            # debug below
            #print(WIT)
            """
            Use acceleration. But lets change this into angles.
            Rotation about X is theta
            Rotation about Y is phi
            Normalize by total vector
            """
            #Tx.Tuple(WIT.acc[0], WIT.acc[1], WIT.acc[2])
            x = WIT.acc[0]
            y = WIT.acc[1]
            z = WIT.acc[2]
            norm = np.sqrt(x*x + y*y + z*z)
            
            theta = 360.0/3.141526 * np.arccos(y/norm)
            phi   = 360.0/3.141526 * np.arccos(x/norm)
            Tx.Theta(theta)
            Tx.Phi(phi)
            
        await client.start_notify(
            "0000ffe4-0000-1000-8000-00805f9a34fb",
            notification_handler
            )
        print("Listening for sensor data...")
        # This code says go to sleep for 15 seconds
        await asyncio.sleep(30)
        #await asyncio.sleep() # wait indefinitely
        
        await client.stop_notify(
            "0000ffe4-0000-1000-8000-00805f9a34fb"
            )

#def BT_Main():
#    asyncio.run(BT_GetData())
    
def Initialize():
    """
    Initialize any other stuff here. predominatly setup the
    UDP socket for sending the data to MAX or Touch Designer.
    """
    global Tx
    # setup a client for sending messages to port 9001
    Tx = TxOSC()
    print ('Initialize')
    
def Finalize():
    """
    do any necessary cleanup on exit. 
    """
    global Tx
    del Tx
    print('Finalize')
    
def BlockingServer():
    """
    This is kind of the main call for this example. It sets up the
    Dispather and then tells it that EventHandler method from above
    is to as it says handle all the inbound events.
    
    """
    global server
    dispatcher = Dispatcher()
    dispatcher.map("/Halt", Halt)
    dispatcher.map("/Gimme", Gimme)
    dispatcher.set_default_handler(EventHandler)
    # lisetn on local host. The receive port for this process
    # is 9002. 
    server = BlockingOSCUDPServer(("127.0.0.1", 9002), dispatcher)
    print("Listening on port 9002")
    threading.Thread(target=server.serve_forever, daemon=True).start()

    #server.serve_forever()
    asyncio.run(BT_GetData())        
    
    
if __name__ == '__main__':
    Initialize()
    #threading.Thread(target=
    BlockingServer()
    print('program ends')
    Finalize()
