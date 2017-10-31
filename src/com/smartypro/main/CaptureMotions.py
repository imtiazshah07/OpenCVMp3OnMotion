'''
Created on Oct 31, 2017

@author: SImtiazAli
'''

import logging
import cv2
import imutils
import threading
import os

class CaptureMotions (threading.Thread):
    logging.basicConfig(level=logging.DEBUG,format='%(asctime)s (%(threadName)-10s) %(message)s',)
    
    def run(self):
        self._startProcess()
        
    def __init__(self,mp3FilePath,sensorId,showWindows,contourAreaMin,contourAreaMax,windowsTitle):
        logging.info("SmartyPro- CaptureMotions.Init !")
        threading.Thread.__init__(self)
        self._mp3FilePath = mp3FilePath
        self._sensorId = sensorId
        self._showWindows = showWindows
        self._operationInProgress = False
        self._contourAreaMin = contourAreaMin
        self._contourAreaMax = contourAreaMax
        self._windowsTitle = windowsTitle

    def _handleSound(self):
        self._operationInProgress = True
        
        logging.info("SmartyPro- _handleSound Started ...self._operationInProgress "+str(self._operationInProgress))
        os.system('mpg123 -q '+self._mp3FilePath)
        self._operationInProgress = False
        
        logging.info("SmartyPro- _handleSound Completed ...self._operationInProgress "+str(self._operationInProgress))
        
        
    def _startProcess(self):
        logging.info("SmartyPro- CaptureMotions.StartProcess !")
        
        firstFrame = None
        
        camera = cv2.VideoCapture(self._sensorId)
        while True:
            
            (grabbed, frame) = camera.read()
             
            if not grabbed:
                    break
            
            frame = imutils.resize(frame, width=500)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)
            
            if firstFrame is None:
               firstFrame = gray
               continue

            frameDelta = cv2.absdiff(firstFrame, gray)
            thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
            
            thresh = cv2.dilate(thresh, None, iterations=2)
            (_,cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            
            for c in cnts:
                if cv2.contourArea(c) > self._contourAreaMin and cv2.contourArea(c) < self._contourAreaMax: 
                   if not self._operationInProgress: 
                      workerThread = threading.Thread(name='_handleSound', target=self._handleSound)
                      workerThread.start()
                     
            if self._showWindows :
                cv2.imshow(self._windowsTitle, frame)
            
            key = cv2.waitKey(10)
            if key == 27:
                cv2.destroyWindow(self._windowsTitle)
                break
     
