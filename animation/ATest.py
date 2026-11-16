# 
# Modified    By    Reason
# --------    --    ------
# 16-Feb-25   CBL   Original
#
#
# things that I needed to do!
# 0) make sure that I'm pointing at the correct version of python
#   sudo port select --set python python313
#   sudo port select --set python3 python313
# 1) blow away and recreate the virtual enviroment.
# 2) make a symbolic link in /usr/local as follows:
# ln -s /System/Volumes/Data/opt/local/include include
# 3) reimport everything
# pip install....
#
# References:
#     https://people.csail.mit.edu/hubert/pyaudio/docs/
#     https://stackoverflow.com/questions/40704026/voice-recording-using-pyaudio
#     https://github.com/jleb/pyaudio/blob/master/test/record.py
#
# Required packages
#
# numpy
# matplotlib
# pyaudio
# scipy
# wxwidgets
# scikit-rf
# pandas
# jupyter
#

import numpy as np
import matplotlib as plt
import scipy.constants as konst
import pyaudio
import wave

def RecordInput():
    import wave

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "output.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                          channels=CHANNELS,
                          rate=RATE,
                          input=True,
                          input_device_index=0,
                          frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        #frames.append(data)

        print("* done recording")

        stream.stop_stream()
        stream.close()
        p.terminate()
        
def PlayWav(filename):
    CHUNK = 1024


    with wave.open(filename, 'rb') as wf:
        # Instantiate PyAudio and initialize PortAudio system resources (1)
        p = pyaudio.PyAudio()

        # Open stream (2)
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        # Play samples from the wave file (3)
        while len(data := wf.readframes(CHUNK)):  # Requires Python 3.8+ for :=
            stream.write(data)

        # Close stream (4)
        stream.close()

        # Release PortAudio system resources (5)
        p.terminate()
        
def ShowDevices():
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')

    for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))



# ===================================================================

ShowDevices()
#RecordInput()
