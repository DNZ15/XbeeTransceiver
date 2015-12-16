import alsaaudio as aa
from struct import unpack
import numpy as np
import wave
import threading
import sys
import time
import copy
import smbus

music = "received.wav"

def set_row1(data, data12A1):
    data = int(data)
    if data == 1:
        data12A1 = (~16 & data12A1 & 0xFF)
    elif data == 2:
        data12A1 = (~24 & data12A1 & 0xFF)
    elif data == 3 :
        data12A1 = (~28 & data12A1 & 0xFF)
    elif data == 4 :
        data12A1 = (~30 & data12A1 & 0xFF)
    elif data >= 5 :
        data12A1 = (~31 & data12A1 & 0xFF)
    return (data12A1)

def set_row2(data, data12A1, data13A1):
    data = int(data)
    if data == 1:
        data13A1 = (~2 & data13A1 & 0xFF)
    elif data == 2 :
        data13A1 = (~3 & data13A1 & 0xFF)
    elif data == 3 :
        data12A1 = (~128 & data12A1 & 0xFF)
        data13A1 = (~3 & data13A1 & 0xFF)
    elif data == 4 :
        data13A1 = (~3 & data13A1 & 0xFF)
        data12A1 = (~192 & data12A1 & 0xFF)
    elif data >= 5 :
        data13A1 = (~3 & data13A1 & 0xFF)
        data12A1 = (~224 & data12A1 & 0xFF)
    return (data12A1, data13A1)

def set_row3(data, data13A1):
    data = int(data)
    if data == 1:
        data13A1 = (~192 & data13A1 & 0xFF)
    elif data == 2 :
        data13A1 = (~224 & data13A1 & 0xFF)
    elif data == 3 :
        data13A1 = (~240 & data13A1 & 0xFF)
    elif data == 4 :
        data13A1 = (~248 & data13A1 & 0xFF)
    elif data >= 5 :
        data13A1 = (~252 & data13A1 & 0xFF)
    return (data13A1)

def set_row4(data, data12A2):
    data = int(data)
    if data == 1:
        data12A2 = (~16 & data12A2 & 0xFF)
    elif data == 2 :
        data12A2 = (~24 & data12A2 & 0xFF)
    elif data == 3 :
        data12A2 = (~28 & data12A2 & 0xFF)
    elif data == 4 :
        data12A2 = (~30 & data12A2 & 0xFF)
    elif data >= 5 :
        data12A2 = (~31 & data12A2 & 0xFF)
    return (data12A2)

def set_row5(data, data12A2, data13A2):
    data = int(data)
    if data == 1:
        data13A2 = (~2 & data13A2 & 0xFF)
    elif data == 2 :
        data13A2 = (~3 & data13A2 & 0xFF)
    elif data == 3 :
        data12A2 = (~128 & data12A2 & 0xFF)
        data13A2 = (~3 & data13A2 & 0xFF)
    elif data == 4 :
        data13A2 = (~3 & data13A2 & 0xFF)
        data12A2 = (~192 & data12A2 & 0xFF)
    elif data >= 5 :
        data13A2 = (~3 & data13A2 & 0xFF)
        data12A2 = (~224 & data12A2 & 0xFF)
    return (data12A2, data13A2)

def set_row6(data, data13A2):
    data = int(data)
    if data == 1:
        data13A2 = (~192 & data13A2 & 0xFF)
    elif data == 2 :
        data13A2 = (~224 & data13A2 & 0xFF)
    elif data == 3 :
        data13A2 = (~240 & data13A2 & 0xFF)
    elif data == 4 :
        data13A2 = (~248 & data13A2 & 0xFF)
    elif data >= 5 :
        data13A2 = (~252 & data13A2 & 0xFF)
    return (data13A2)

def TurnOffLEDS ():
    bus.write_byte_data(ADDR1, BANKA, 0xFF)  #set all columns high
    bus.write_byte_data(ADDR1, BANKB, 0xFF)  #set all rows low
    bus.write_byte_data(ADDR2, BANKA, 0xFF)  #set all columns high
    bus.write_byte_data(ADDR2, BANKB, 0xFF)  #set all rows low

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


# Initialise matrix
matrix    = np.array([0,0,0,0,0,0])
power     = []
weighting = [2,8,8,16,32,64] # Change these according to taste

# Set up audio
wavfile = wave.open(music,"r")
sample_rate = wavfile.getframerate()
no_channels = wavfile.getnchannels()


#chunk's zijn afhankelijk van de sample_rate
#chunk       = 2400
#chunk       = 600
#chunk       = 120
#chunk       = 60
chunk       = 600
#chunk       = 240
#chunk       = 8192
#chunk       = 16384 #use this value if running it all on one Pi

output = aa.PCM(aa.PCM_PLAYBACK, aa.PCM_NORMAL)
output.setchannels(no_channels)
output.setrate(sample_rate)
output.setformat(aa.PCM_FORMAT_S16_LE)
output.setperiodsize(chunk)

# Return power array index corresponding to a particular frequency
def piff(val):
    return int((2*chunk*val)/sample_rate)

def calculate_levels(data, chunk,sample_rate,matrix):
    #    global matrix
    # Convert raw data (ASCII string) to numpy array
    data = unpack("%dh"%(len(data)/2),data)
    data = np.array(data, dtype='h')
    # Apply FFT - real data
    fourier=np.fft.rfft(data)
    # Remove last element in array to make it the same size as chunk
    fourier=np.delete(fourier,len(fourier)-1)
    # Find average 'amplitude' for specific frequency ranges in Hz
    power = np.abs(fourier)
    #power = power*2
    
    #matrix[0]= int(power(piff(450)))
    #matrix[1]= int(power[600])
    #print power
    #print (np.mean(power[piff(600) :piff(750):1]))
    matrix[0]= int(np.mean(power[piff(156)  :piff(313):1]))
    matrix[1]= int(np.mean(power[piff(313)  :piff(600):1]))
    matrix[2]= int(np.mean(power[piff(600)  :piff(900):1]))
    matrix[3]= int(np.mean(power[piff(900)  :piff(1200):1]))
    matrix[4]= int(np.mean(power[piff(1200) :piff(1500):1]))
    matrix[5]= int(np.mean(power[piff(1500) :piff(1800):1]))
    
    """
        matrix[0]= int(np.mean(power[piff(0)    :piff(156):1]))
        matrix[1]= int(np.mean(power[piff(156)  :piff(313):1]))
        matrix[2]= int(np.mean(power[piff(313)  :piff(450):1]))
        matrix[3]= int(np.mean(power[piff(450)  :piff(600):1]))
        matrix[4]= int(np.mean(power[piff(600) :piff(750):1]))
        matrix[5]= int(np.mean(power[piff(750) :piff(1050):1]))
        """
    #matrix[5]= int(np.mean(power[piff(5000) :piff(10000):1]))
    #matrix[7]= int(np.mean(power[piff(10000):piff(20000):1]))
    # Tidy up column values for the LED matrix
    matrix=np.divide(np.multiply(matrix,weighting),1000000)#hier stond 1000000
    # Set floor at 0 and ceiling at 8 for LED matrix
    matrix=matrix.clip(0,5)
    return matrix

data12A1 = 0xFF
data12A2 = 0xFF
data13A1 = 0xFF
data13A2 = 0xFF

try:
    # Process audio file
    print "Processing....."
    data = wavfile.readframes(chunk)
    while data!='':
        output.write(data)
        matrix=calculate_levels(data, chunk,sample_rate,matrix)
        for i in range (0,6):
            #print i
            row = matrix[i] #(1<<matrix[i])-1
            
            #print matrix[1]
            
            if i == 0:
                data12A1 = set_row1(row, data12A1)
            elif i == 1:
                data12A1, data13A1 = set_row2(row, data12A1, data13A1)
            elif i == 2:
                data13A1 = set_row3(row, data13A1)
            elif i == 3:
                data12A2 = set_row4(row, data12A2)
            elif i == 4:
                data12A2, data13A2 = set_row5(row, data12A2, data13A2)
            elif i == 5:
                data13A2 = set_row6(row, data13A2)


        bus.write_byte_data(ADDR1,0x12,data12A1)
        bus.write_byte_data(ADDR2,0x12,data12A2)
        bus.write_byte_data(ADDR1,0x13,data13A1)
        bus.write_byte_data(ADDR2,0x13,data13A2)
        
        data12A1 = 0xFF
        data12A2 = 0xFF
        data13A1 = 0xFF
        data13A2 = 0xFF
        
        
        data = wavfile.readframes(chunk)

except KeyboardInterrupt:
    print "User Cancelled (Ctrl C)"
    TurnOffLEDS()
except:
    print "Unexpected error - ", sys.exc_info()[0], sys.exc_info()[1]
    TurnOffLEDS()
    raise

TurnOffLEDS()


