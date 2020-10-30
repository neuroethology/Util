import os
import cv2
import numpy as np
from util.seqIo import *


class vidReader():
    # a small class that opens, reads from, and closes either seq movies or movies openable by cv2.
    # saves us having to keep checking video extensions in the main code.
    # could be extended with other features as needed....

    def __init__(self,filename):

        _, self.ext = os.path.splitext(filename)
        if self.ext=='seq':
            self._reader = seqIo_reader(filename)
            self.NUM_FRAMES = self._reader.header['numFrames']
            self.IM_H = self._reader.header['height']
            self.IM_W = self._reader.header['width']
            self.fps = self._reader.header['fps']
            self._reader.buildSeekTable()

        else:
            self._reader = cv2.VideoCapture(filename)
            if self._reader.isOpened():
                self.rval = True
            else:
                self.rval = False
                print('video not readable')
            self.fps = self._reader.get(cv2.CAP_PROP_FPS)
            if np.isnan(self.fps): self.fps = 30.
            self.NUM_FRAMES = int(self._reader.get(cv2.CAP_PROP_FRAME_COUNT))
            self.IM_H = self._reader.get(cv2.CAP_PROP_FRAME_HEIGHT)
            self.IM_W = self._reader.get(cv2.CAP_PROP_FRAME_WIDTH)

    def seek(self,f):
        if self.ext=='seq':
            # I'm not sure this is a thing for seq files
            return
        else:
            self.reader.set(cv2.CAP_PROP_POS_FRAMES, f)


    def getFrame(self,f):
        if self.ext == 'seq':
            img = self._reader.getFrame(f)[0]
        else:
            self._reader.set(cv2.CAP_PROP_POS_FRAMES, f)
            _, img = self._reader.read()
            img = img.astype(np.float)
        return img

    def getNext(self):  # I'm not sure that this actually works- do cv2 readers auto-advance?
        if self.ext == 'seq':
            self.f = self.f+1
            img = self._reader.getFrame(self.f)[0]
        else:
            _, img = self._reader.read()
            img = img.astype(np.float)
        return img

    def close(self):
        if self.ext == 'seq':
            self._reader.close()
        else:
            self._reader.release()
