# ####################################################################
# Client.py
#
# Fooling around to learn how UDP works with Python.
#
# Modified  By   Reason
# --------  --   ------
# 01-Nov-26 CBL  Original
#
# References:
#
# Notes:
#
# ####################################################################
import sys
import argparse
import socket


# basic test parameters
UDP_IP   = "127.0.0.1"
UDP_PORT = 9002


def Test():
    # 1. Create the UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    MESSAGE = "The quick red fox jumped over the lazy brown dog."
    # 2. Convert string payload into raw bytes 
    bytes_to_send = MESSAGE.encode('utf-8')

    # 3. Send data directly to target address
    sock.sendto(bytes_to_send, (UDP_IP, UDP_PORT))
    print(f"Sent message to {UDP_IP}:{UDP_PORT}")

if __name__ == '__main__':

    # default number of samples
    N = 10
    # default elapsed time, hard coded to 1/sec so this ends up
    # being the number of samples.

    # Default gain
    Gain = 4

    parser = argparse.ArgumentParser("Incident UV tool.")
    parser.add_argument("-n", "--number", help="Number samples")
    parser.add_argument("-g", "--gain",   help="ADC amplifier gain.")

    args = parser.parse_args()

    Test()
