#!/usr/bin/env python

import time
import serial
import threading
import wave

#exp
import os

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


def ListenForCommands():
   while 1:
      x = ser.readline(4)
      return x

def simplereceive():
#    received=1
#    while receive != 0:
     while 1:
        x = ser.readline(4) 
        if x == 'forw':
           print 'Moving forward'        
        elif x == 'back':
           print 'Moving backwards'
        elif x == 'left':
           print 'Moving left'
        elif x == 'righ':
           print 'Moving right'
        elif x == 'fast':
           print 'Moving faster'
        elif x == 'slow':
           print 'Moving slower'
        elif x == 'dead':
           print 'Drop dead'




def ReadParameters():
    paramlist=[]
    wavparams = ''
    print len(wavparams)
    while (len(wavparams) != 18):
        wavparams = ser.read(18)
        # print len(wavparams)

    print wavparams
    paramlist = wavparams.split('_')
    
    print "filter settings:",paramlist[0]
    filtersettings = str(paramlist[0])
    lowpsetting = filtersettings[0:3]
    highpsetting = filtersettings[3:6]
    framesize = int(paramlist[1])
    sampfreq = int(paramlist[2])

    print lowpsetting
    print highpsetting
    print "framesize ", paramlist[1]
    print "sampfreq to use ",paramlist[2]
    ReceiveAndSaveWav(framesize, sampfreq)

#def ReceiveAndSaveWav():
def ReceiveAndSaveWav(totframes, fs):
    #check if file exists -> remove
    if os.path.isfile("received.wav"):
        os.remove("received.wav")

    wavie = wave.open('received.wav','w')
    #1 channel, 2 bytes, sampfreq, amount of frames
#    wavie.setparams((1,2,2000,0,'NONE','not compressed'))
    wavie.setparams((1,2,fs,0,'NONE','not compressed'))


#    for i in range(0, 120000):
    for i in range(0, totframes):

        char = ser.read(2)
    #    a = char.decode('hex')
        wavie.writeframes(char)

    #    print "i",i
        print "char",char
    #    ser.flush()
    #    print "char type",type(char)
    #    print "char len",len(char)
     
    print "ok"
    wavie.close()

#simplereceive()

ReadParameters()






