#!/usr/bin/env python3
# SPDX-License-Identifier: MIT

"""Screen capture utility for old Tektronix oscilloscopes

A screenshot is triggered by pressing the HARDCOPY button. The script will then
receive the TIFF data over RS-232 (19200 baud 8N1) and write the image to the
current directory.
This was developed for the TDS 320 but should also work with similar models
that have a serial port.
"""
import sys
from datetime import datetime

from serial import Serial

START = b'MM\0*'
END = b'TIFF Driver 1.0\0'


def configure(serial):
    send_cmd(serial, b"HARDCopy:FORMat TIFf")
    send_cmd(serial, b"HARDCopy:LAYout PORTRait")
    send_cmd(serial, b"HARDCopy:PORT RS232")
    send_cmd(serial, b"RS232:HARDFlagging OFF")
    send_cmd(serial, b"RS232:SOFTFlagging OFF")


def receive_tiffs(serial):
    data = b''

    while True:
        b = serial.read()
        if len(b):
            data += b
            if data.endswith(END):
                ts = datetime.now().strftime("%Y%m%d%H%M%S")
                filename = f"capture_{ts}.tiff"
                print(f"Writing {filename}")
                write_tiff(filename, data)
                data = b''


def write_tiff(filename, data):
    try:
        start = data.index(START)
    except ValueError:
        print("Invalid data")
        return
    with open(filename, 'wb') as f:
        f.write(data[start:])


def send_cmd(serial, cmd):
    serial.write(cmd + b"\r\n")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} /dev/ttyxxx")
        exit(1)
    serial = Serial(sys.argv[1], 19200, timeout=1)
    configure(serial)
    try:
        receive_tiffs(serial)
    except KeyboardInterrupt:
        pass
    finally:
        if serial:
            serial.close()
