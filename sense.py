# @Author: archer
# @Date:   2019-06-03T19:42:17+01:00
# @Last modified by:   archer
# @Last modified time: 2019-06-03T19:45:32+01:00

import os, sys
import time
import picamera
from pathlib import Path


home = str(Path.home())


with picamera.PiCamera() as camera:
    camera.resolution = (3280, 2464)
    camera.rotation = 180
    camera.start_preview()
    time.sleep(2)
    camera.capture(str(time.strftime("%Y-%m-%d_%H:%M:%S", time.gmtime())), 'yuv')
