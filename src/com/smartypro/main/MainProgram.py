'''
Created on Oct 31, 2017

@author: SImtiazAli
'''
import logging

from src.com.smartypro.main.CaptureMotions import CaptureMotions

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s (%(threadName)-10s) %(message)s',)

_mp3FilePath = "10Seconds.mp3"
_sensorId = 0
_showWindows = True
_contourAreaMin=10000
_contourAreaMax = 184900
_windowsTitle='SmartyPro Player'

if __name__ == '__main__':
    logging.info("SmartyPro Client Starting!")
    
    _CaptureMotions = CaptureMotions(_mp3FilePath,_sensorId,_showWindows,_contourAreaMin,_contourAreaMax,_windowsTitle)
    _CaptureMotions.start()

    logging.info("SmartyPro Client Terminated!")