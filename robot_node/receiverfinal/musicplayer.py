import sounddevice as sd
from threading import Thread
from multiprocessing import Queue
import time

class MusicPlayer(Thread):
    i = 0
    
    def __init__(self, q, Fs, minimumblocks=10, sleeptime=0.2):
        self.q = q
        self.Fs = Fs
        self.sleeptime = sleeptime
        self.minblocks = minimumblocks
        
        Thread.__init__(self)
        
    def run(self):
        while self.i < 10000:
            # qsize() is unreliable
            if len(self.q)!=0 and len(self.q) > self.minblocks:
                # Get all values from all chunks and put in a list
                data = []
                n = 0
                for n in range(self.minblocks):
                    # get minblocks amount of chunks
                    tmp2 = self.q.pop()
                    print "tmp2 ",tmp2
#                    print "type ",len(tmp)
		    tmp = float(tmp2)
                    n = n + 1

                    m = 0
                    for m in range(len(tmp)):
                        # append all values in chunk to data list
                        data.append(tmp[m])
                        m = m + 1

                    self.i = self.i + 1

                print("Musicplayer: Playing data with length: ", len(data))
                sd.play(data)

            time.sleep(self.sleeptime)
