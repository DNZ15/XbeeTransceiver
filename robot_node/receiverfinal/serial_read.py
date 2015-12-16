#!/usr/bin/env python

"""
@author: Dennis 
"""

import time
import serial

ser = serial.Serial(
    port='/dev/ttyAMA0', 
    baudrate=57600, 
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)
ser.flushInput()
ser.flushOutput()

while 1:
    print ser.read(4)
#  time.sleep(0.5)
