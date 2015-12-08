#!/usr/bin/env python

"""
@author: Dennis 
"""

import time
import serial
import wave
import struct
from struct import *

import array


# UART settings
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

# Declare audiofiles
sound1='sounds/SineWave_300Hz_samp_2kHz_60s.wav'
sound2='sounds/SineWave_450Hz_samp_2kHz_60s.wav'
sound3='sounds/SineWave_600Hz_samp_2kHz_60s.wav'
sound4='sounds/SineWave_750Hz_samp_2kHz_60s.wav'
sound5='sounds/SineWave_900Hz_samp_2kHz_60s.wav'
sound6='sounds/mario_8kHz_16bit_mono.wav'
sound7='sounds/starwars_8kHz_16bit_mono.wav'


# function that send 2 bytes at a time using a for loop	
def SendStream(songnumber):
    wavefile = wave.open(songnumber,'rb')
    chans = wavefile.getnchannels()
    samps = wavefile.getnframes()
    framerate = wavefile.getframerate()
    comptype = wavefile.getcompname()
    sampwidth = wavefile.getsampwidth()
    frames = wavefile.readframes(samps)

    print "Info about wav-file:"
    # mono returns 1, stereo returns 2
    print "Channel(s): ", chans
    # each frame exist out of 2 bytes (most of the time)
    print "Number of frames: ", samps
    # 16 bit returns 2, 8 bit returns 1
    print "Total length (frames*2) (size of file) : ",len(frames)
    # sample width in bytes
    print "Sample width (bytes): ", sampwidth
    print "Sampling Frequency (Hz): ", framerate
    print "Compression type: ", comptype

    wavefile.close()

    #string of 6 bytes
    unpstr = '<{0}h'.format(samps*chans)
    print "unpstr  ", len(unpstr)

    # NEEDS TO BE SENDED!!!
#    print "amount of frames",calcsize(unpstr)
#    print "amount of frames",len(frames)
    ListOfInts = list(struct.unpack(unpstr, frames))
    print "list length",len(ListOfInts)
    
    start=time.time()    
    # list length = amount of frames 
    for a in range(len(ListOfInts)):
#    for a in range(0, len(ListOfInts), 2):
             
         # length is 8 bytes    

#         char = struct.pack('hh', ListOfInts[a], ListOfInts[a+1])         
         # length char is 2 bytes    
         char = struct.pack('h', ListOfInts[a])         

#         print "char type",type(char)
#         print "char type",len(char)
#         print "-----------------------"


         # length is 4 bytes
#         bytestosend = char.encode('hex')


         
#         print "type bytestosend", type(bytestosend)
#         print "len bytestosend", len(bytestosend)

         # sending 4 bytes         
#         print "sending ",bytestosend                    

#         print "sending ",char                    
#         print len(char)

         #TESTING
#         ser.write(bytestosend)
         ser.write(char)
#         ser.flush()       
#         time.sleep(1)

    end = time.time()
    print "time needed: ", end-start


def GetSoundProperties(songnumber):
   
    # Read in a wavfile
    wavefile = wave.open(songnumber,'rb')
    # Get amount of frames (a frame exists out of 2 bytes) 
    samps = wavefile.getnframes()
    # Get the sample frequency
    framerate = wavefile.getframerate()
    
    #create parameterstring and return it
    soundsettings= str(samps)+ '_' +str(framerate)
    return soundsettings


def AllParams(s, par):
    soundinfo = str(par)+ '_' +GetSoundProperties(s)
    return soundinfo


def StartMenu():
   menu = {}
   menu['']="\n\n----- START MENU -----"
   menu['\033[1;32m \n 1 \033[1;m']="\033[1;32m MENU ROBOT CONTROLS \033[1;m"
   menu['\033[1;32m 2 \033[1;m']="\033[1;32m MENU AUDIO CONTROLS \033[1;m"
   menu['\033[1;32m 3 \033[1;m']="\033[1;32m ROBOT MONITOR\n \033[1;m"
   menu['\033[1;32m 911 \033[1;m']="\033[1;32m Exit program \033[1;m"
 
   while True:
     options=menu.keys()
     options.sort()
     for entry in options:
        print entry, menu[entry]
     print "\n-----------------------"
  
     selection=raw_input("\n\033[1;46m Please select: \033[1;m ")
     if selection =='1':
        RobotMenu()
     elif selection =='2':
        LowPassAmplifyMenu()
     elif selection =='3':
         RobotMonitor()
     elif selection =='911':
        print "Exiting program\n"
        break
     else:
        print "Unknown Option Selected!\n"




def RobotMenu():
   menu2 = {}
   menu2['']="\n\n----- ROBOT CONTROLS -----"  
   menu2['\033[1;32m \n 1 \033[1;m']="\033[1;32m Faster \033[1;m"
   menu2['\033[1;32m 2 \033[1;m']="\033[1;32m Backward \033[1;m"
   menu2['\033[1;32m 3 \033[1;m']="\033[1;32m Slower \033[1;m"
   menu2['\033[1;32m 4 \033[1;m']="\033[1;32m Left \033[1;m"
   menu2['\033[1;32m 5 \033[1;m']="\033[1;32m Drop Dead \033[1;m"
   menu2['\033[1;32m 6 \033[1;m']="\033[1;32m Right \033[1;m"
   menu2['\033[1;32m 8 \033[1;m']="\033[1;32m Forward \033[1;m"
   menu2['\033[1;31m 911 \033[1;m']="\033[1;31m Previous Menu \033[1;m"

   while True:
      options2=menu2.keys()
      options2.sort()
      for entry2 in options2:
         print entry2, menu2[entry2]
      print "\n--------------------------"
  
      selection2=raw_input("\n\033[1;46m Please select: \033[1;m ")
      if selection2 =='1':
         print "Faster\n"
         ser.write("fast")
      elif selection2 =='2':
         print "Backward\n"
         ser.write("back")
      elif selection2 =='3':
         print "Slower\n"
         ser.write("slow")
      elif selection2 =='4':
         print "Left\n"
         ser.write("left")
      elif selection2 =='5':
         print "Drop Dead\n"
         ser.write("dead")
      elif selection2 =='6':
         print "Right\n"
         ser.write("righ")
      elif selection2 =='8':
         print "Forward\n"
         ser.write("forw")
      elif selection2 =='911':
         break
      else:
         print "Unknown Option Selected!\n"



def LowPassAmplifyMenu():
   menu3 = {}
   menu3['']="\n\n----- CUTT-OFF 200Hz -----"
   menu3['\033[1;32m \n 1 \033[1;m']="\033[1;32m +10dB \033[1;m"
   menu3['\033[1;32m \n 2 \033[1;m']="\033[1;32m 0dB \033[1;m"
   menu3['\033[1;32m \n 3 \033[1;m']="\033[1;32m -10dB \033[1;m"
   menu3['\033[1;31m 911 \033[1;m']="\033[1;31m Previous Menu \033[1;m"
   
   paramlow=''
   while True:
      options3=menu3.keys()
      options3.sort()
      for entry3 in options3:
         print entry3, menu3[entry3]
      print "\n--------------------------"
      print "Cut-off low= ",paramlow
      selection3=raw_input("\n\033[1;46m Please select: \033[1;m ")
      if selection3 =='1':
         print "+10dB selected\n"
         paramlow='+10'
         HighPassAmplifyMenu(paramlow)
      elif selection3 =='2':
         print "0dB selected\n"
         paramlow='000'
         HighPassAmplifyMenu(paramlow)
      elif selection3 =='3':
         print "-10dB selected\n"
         paramlow='-10'
         HighPassAmplifyMenu(paramlow)
      elif selection3 =='911':
         break
      else:
         print "Unknown Option Selected!\n"


def HighPassAmplifyMenu(paramlow):
   
   paramhigh=''
   menu4 = {}
   print "\n\n----- CUTT-OFF 1000Hz -----"
   menu4['\033[1;32m \n 1 \033[1;m']="\033[1;32m +10dB \033[1;m"
   menu4['\033[1;32m \n 2 \033[1;m']="\033[1;32m 0dB \033[1;m"
   menu4['\033[1;32m \n 3 \033[1;m']="\033[1;32m -10dB \033[1;m"
   menu4['\033[1;31m 911 \033[1;m']="\033[1;31m Previous Menu \033[1;m"

   while True:
      options4=menu4.keys()
      options4.sort()
      for entry4 in options4:
         print entry4, menu4[entry4]
      print "\n--------------------------"
      print "Cut-off low= ",paramlow

      selection4=raw_input("\n\033[1;46m Please select: \033[1;m ")
      if selection4 =='1':
         paramhigh = paramlow+'+10'
         print "+10dB selected\n"
         AudioMenu(paramhigh)   
      elif selection4 =='2':
         paramhigh = paramlow+'000'
         print "0dB selected\n"   
         AudioMenu(paramhigh)     
      elif selection4 =='3':
         paramhigh = paramlow+'-10'
         print "-10dB selected\n"
         AudioMenu(paramhigh)   
      elif selection4 =='911':
         break
      else:
         print "Unknown Option Selected!\n"
 

    
def AudioMenu(param):
   menu5 = {}
   print "\n\n----- AUDIO SETTINGS -----"
   menu5['\033[1;32m \n 1 \033[1;m']="\033[1;32m Sound1 \033[1;m"
   menu5['\033[1;32m 2 \033[1;m']="\033[1;32m Sound2 \033[1;m"
   menu5['\033[1;32m 3 \033[1;m']="\033[1;32m Sound3 \033[1;m"
   menu5['\033[1;32m 4 \033[1;m']="\033[1;32m Sound4 \033[1;m"
   menu5['\033[1;32m 5 \033[1;m']="\033[1;32m Sound5 \033[1;m"
   menu5['\033[1;32m 6 \033[1;m']="\033[1;32m Sound6 \033[1;m"
   menu5['\033[1;32m 7 \033[1;m']="\033[1;32m Sound7 \033[1;m"
   menu5['\033[1;31m 911 \033[1;m']="\033[1;31m Previous Menu \033[1;m"

   while True:
      options5=menu5.keys()
      options5.sort()
      for entry5 in options5:
         print entry5, menu5[entry5]
      print "\n--------------------------"
      print "Param cut-off", param
      selection5=raw_input("\n\033[1;46m Please select: \033[1;m ")
      if selection5 =='1':
         print "Sound1 selected\n"
         print sound1
         ser.write(AllParams(sound1, param))   
         SendStream(sound1)
         StartMenu()

      elif selection5 =='2':
         print "Sound2 selected\n"
         print sound2   
         ser.write(AllParams(sound2, param))   
         SendStream(sound2)
         StartMenu()

      elif selection5 =='3':
         print "Sound3 selected\n"
         print sound3
         ser.write(AllParams(sound3, param))   
         SendStream(sound3)
         StartMenu()

      elif selection5 =='4':
         print "Sound4 selected\n"
         print sound4
         ser.write(AllParams(sound4, param))   
         SendStream(sound4)
         StartMenu()

      elif selection5 =='5':
         print "Sound5 selected\n"
         print sound5
         ser.write(AllParams(sound5, param))   
         SendStream(sound5)
         StartMenu()

      elif selection5 =='6':
         print "Sound6 selected\n"
         print sound6
         ser.write(AllParams(sound6, param))   
         SendStream(sound6)
         StartMenu()

      elif selection5 =='7':
         print "Sound7 selected\n"
         print sound7
         ser.write(AllParams(sound7, param))   
         SendStream(sound7)
         StartMenu()

      elif selection5 =='911':
         break
      else:
         print "Unknown Option Selected!\n"



# draft
def RobotMonitor():
   # send lisn command to trigger robot node
   ser.write("lisn")

   menu6 = {}
   menu6['\033[1;32m \n 1 \033[1;m']="\033[1;32m Start Monitoring \033[1;m"
   menu6['\033[1;32m \n 2 \033[1;m']="\033[1;32m Exit \033[1;m"
   options6=menu6.keys()
   options6.sort()
   for entry6 in options6:
       print entry6, menu6[entry6]

   selection6=raw_input("\n\033[1;46m Please select: \033[1;m ")
   if selection6=="1":
      print "Reading Robotdata:\n"
      while True:
          getinfo = ser.read(4)
          print getinfo
   elif selection6=="2":
      ser.write("exit")   
      return
   else:
      print "Unknown Option Selected!\n"



StartMenu()
