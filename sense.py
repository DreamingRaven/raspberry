# @Author: archer
# @Date:   2019-06-03T19:42:17+01:00
# @Last modified by:   archer
# @Last modified time: 2019-06-04T20:03:07+01:00

import os, sys
import time
import picamera
from pathlib import Path

home = str(Path.home())

def main():
    # create camera object and only continue if it is still valid
    with picamera.PiCamera() as cam:
        cam.resolution = (3280, 2464)
        cam.rotation = 180
        cam.start_preview()
        while(True):
            time.sleep(5)
            cam.capture(str(time.strftime("%Y-%m-%d_%H:%M:%S", time.gmtime())), 'png')

if __name__ == "__main__":
    main()
