# ####################################################################
# Server.py
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

    # 2. Bind the socket to the target port
    sock.bind((UDP_IP, UDP_PORT))

    print(f"Listening for UDP packets on {UDP_IP}:{UDP_PORT}...")

    while True:
        # 3. Buffer size is 1024 bytes. 
        # recvfrom() blocks until data arrives and returns (bytes_data, sender_address_tuple)
        data, addr = sock.recvfrom(1024)
    
        # 4. Decode the raw bytes into a readable string
        decoded_message = data.decode('utf-8')
        print(f"Received message from {addr}: {decoded_message}")


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
