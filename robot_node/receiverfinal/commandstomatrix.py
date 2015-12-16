import alsaaudio as aa
from struct import unpack
import numpy as np
import wave
import threading
import sys
import time
import copy
import smbus

class ComToMatrix():

    def __init__(self):
        self.bus=smbus.SMBus(1)     #Use '1' for newer Pi boards;

        self.addressU1=0x20         #The I2C address of MCP23017-1
        self.addressU2=0x24         #The I2C address of MCP23017-2
        self.DIRA=0x00         #PortA I/O direction, by pin. 0=output, 1=input
        self.DIRB=0x01         #PortB I/O direction, by pin. 0=output, 1=input
        self.BANKA=0x12         #Register address for Bank A
        self.BANKB=0x13         #Register address for Bank B
        #Set up the 23017 for 16 output pins
        self.bus.write_byte_data(self.addressU1, self.DIRA, 0);  #all zeros = all outputs on Bank A
        self.bus.write_byte_data(self.addressU1, self.DIRB, 0);  #all zeros = all outputs on Bank B
        self.bus.write_byte_data(self.addressU2, self.DIRA, 0);  #all zeros = all outputs on Bank A
        self.bus.write_byte_data(self.addressU2, self.DIRB, 0);  #all zeros = all outputs on Bank B

        self.data12A1 = 0xFF
        self.data12A2 = 0xFF
        self.data13A1 = 0xFF
        self.data13A2 = 0xFF

    def set_Reset(self):
		self.bus.write_byte_data(self.addressU1,0x12,0xFF)
		self.bus.write_byte_data(self.addressU1,0x13,0xFF)
		self.bus.write_byte_data(self.addressU2,0x12,0xFF)
		self.bus.write_byte_data(self.addressU2,0x13,0xFF)

    def set_Left(self):
		self.bus.write_byte_data(self.addressU1,0x12,0b10111011)
		self.bus.write_byte_data(self.addressU1,0x13,0b10101010)
		self.bus.write_byte_data(self.addressU2,0x12,0b01111011)
		self.bus.write_byte_data(self.addressU2,0x13,0b11101111)


    def set_Right(self):
		self.bus.write_byte_data(self.addressU1,0x12,0b01111011)
		self.bus.write_byte_data(self.addressU1,0x13,0b11101111)
		self.bus.write_byte_data(self.addressU2,0x12,0b10101010)
		self.bus.write_byte_data(self.addressU2,0x13,0b11101110)

    def set_Min(self):
		self.bus.write_byte_data(self.addressU1,0x12,0b01111011)
		self.bus.write_byte_data(self.addressU1,0x13,0b11101111)
		self.bus.write_byte_data(self.addressU2,0x12,0b01111011)
		self.bus.write_byte_data(self.addressU2,0x13,0b11101111)

    def set_Plus(self):
		self.bus.write_byte_data(self.addressU1,0x12,0b01111011)
		self.bus.write_byte_data(self.addressU1,0x13,0b10000011)
		self.bus.write_byte_data(self.addressU2,0x12,0b01100000)
		self.bus.write_byte_data(self.addressU2,0x13,0b11101111)

    def set_Back(self):
		self.bus.write_byte_data(self.addressU1,0x12,0b11111011)
		self.bus.write_byte_data(self.addressU1,0x13,0b10000010)
		self.bus.write_byte_data(self.addressU2,0x12,0b11100000)
		self.bus.write_byte_data(self.addressU2,0x13,0b11101110)

    def set_Forw(self):
		self.bus.write_byte_data(self.addressU1,0x12,0b10111011)
		self.bus.write_byte_data(self.addressU1,0x13,0b10000011)
		self.bus.write_byte_data(self.addressU2,0x12,0b10100000)
		self.bus.write_byte_data(self.addressU2,0x13,0b11101111)

    def set_Dead(self):
		self.bus.write_byte_data(self.addressU1,0x12,0b11001110)
		self.bus.write_byte_data(self.addressU1,0x13,0b11011110)
		self.bus.write_byte_data(self.addressU2,0x12,0b11010111)
		self.bus.write_byte_data(self.addressU2,0x13,0b10111010)

    def set_Dead2(self):
		self.bus.write_byte_data(self.addressU1,0x12,0b10111010)
		self.bus.write_byte_data(self.addressU1,0x13,0b10101001)
		self.bus.write_byte_data(self.addressU2,0x12,0b10101010)
		self.bus.write_byte_data(self.addressU2,0x13,0b11101001)



