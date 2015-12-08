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

#           break
           #received=0;
#read()




#simplereceive()

#t1 = threading.Thread(target=ListenForCommands, args=[])
#t2 = threading.Thread(target=simplereceive, args=[ListenForCommands()])
#t1.start()
#t2.start()


def ReadParameters():
    paramlist=[]
    wavparams = ''
    print len(wavparams)
    while (len(wavparams) != 18):
        wavparams = ser.read(18)
#        print len(wavparams)

    print wavparams
    paramlist = wavparams.split('_')
    
    print "filter settings:",paramlist[0]
    filtersettings = str(paramlist[0])
    lowpsetting = filtersettings[0:3]
    print lowpsetting
    highpsetting = filtersettings[3:6]
    print highpsetting

    print "framesize ", paramlist[1]
    print "sampfreq to use ",paramlist[2]


def ReceiveAndSaveWav():
    #check if file exists -> remove
    if os.path.isfile("received.wav"):
        os.remove("received.wav")

    wavie = wave.open('received.wav','w')
    #1 channel, 2 bytes, sampfreq, aantal frames
    wavie.setparams((1,2,2000,0,'NONE','not compressed'))


    #15000 = length meegeven!
    #1 min = 240000 sinussen
    #for i in range(0, 120000):
    #range 0 to max frame (size/2)

    for i in range(0, 120000):

        char = ser.read(2)
    #    a = char.decode('hex')
        wavie.writeframes(char)

    #    print "i",i
        print "char",char
    #    ser.flush()
    #    print "char type",type(char)
    #    print "char len",len(char)
#    time.sleep(1)
     
    print "ok"
    wavie.close()


ReadParameters()






