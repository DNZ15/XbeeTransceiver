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
        bus=smbus.SMBus(1)     #Use '1' for newer Pi boards;

		ADDR1   = 0x20         #The I2C address of MCP23017-1
		ADDR2   = 0x24         #The I2C address of MCP23017-2
		DIRA    = 0x00         #PortA I/O direction, by pin. 0=output, 1=input
		DIRB    = 0x01         #PortB I/O direction, by pin. 0=output, 1=input
		BANKA   = 0x12         #Register address for Bank A
		BANKB   = 0x13         #Register address for Bank B

		#Set up the 23017 for 16 output pins
		bus.write_byte_data(ADDR1, DIRA, 0);  #all zeros = all outputs on Bank A
		bus.write_byte_data(ADDR1, DIRB, 0);  #all zeros = all outputs on Bank B
		bus.write_byte_data(ADDR2, DIRA, 0);  #all zeros = all outputs on Bank A
		bus.write_byte_data(ADDR2, DIRB, 0);  #all zeros = all outputs on Bank B
  

	def set_Left():
		bus.write_byte_data(addressU1,0x12,0b10111011)
		bus.write_byte_data(addressU1,0x13,0b10101010)
		bus.write_byte_data(addressU2,0x12,0b01111011)
		bus.write_byte_data(addressU2,0x13,0b11101111)


	def set_Right():
		bus.write_byte_data(addressU1,0x12,0b01111011)
		bus.write_byte_data(addressU1,0x13,0b11101111)
		bus.write_byte_data(addressU2,0x12,0b10101010)
		bus.write_byte_data(addressU2,0x13,0b11101110)

	def set_Min():
		bus.write_byte_data(addressU1,0x12,0b01111011)
		bus.write_byte_data(addressU1,0x13,0b11101111)
		bus.write_byte_data(addressU2,0x12,0b01111011)
		bus.write_byte_data(addressU2,0x13,0b11101111)

	def set_Plus():
		bus.write_byte_data(addressU1,0x12,0b01111011)
		bus.write_byte_data(addressU1,0x13,0b10000011)
		bus.write_byte_data(addressU2,0x12,0b01100000)
		bus.write_byte_data(addressU2,0x13,0b11101111)

	def set_Back():
		bus.write_byte_data(addressU1,0x12,0b11111011)
		bus.write_byte_data(addressU1,0x13,0b10000010)
		bus.write_byte_data(addressU2,0x12,0b11100000)
		bus.write_byte_data(addressU2,0x13,0b11101110)

	def set_Forw():
		bus.write_byte_data(addressU1,0x12,0b10111011)
		bus.write_byte_data(addressU1,0x13,0b10000011)
		bus.write_byte_data(addressU2,0x12,0b10100000)
		bus.write_byte_data(addressU2,0x13,0b11101111)

	def set_Dead():
		bus.write_byte_data(addressU1,0x12,0b11001110)
		bus.write_byte_data(addressU1,0x13,0b11011110)
		bus.write_byte_data(addressU2,0x12,0b11010111)
		bus.write_byte_data(addressU2,0x13,0b10111010)

	def set_Dead2():
		bus.write_byte_data(addressU1,0x12,0b10111010)
		bus.write_byte_data(addressU1,0x13,0b10101001)
		bus.write_byte_data(addressU2,0x12,0b10101010)
		bus.write_byte_data(addressU2,0x13,0b11101001)
