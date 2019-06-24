# @Author: archer
# @Date:   2019-06-24T11:38:32+01:00
# @Last modified by:   archer
# @Last modified time: 2019-06-24T12:05:30+01:00

# this file is a test file to check if example code can run on any given
# hardware as existing Cam.py struggles to run longer than 7 minutes on pi0w


import datetime

import time





import picamera




with picamera.PiCamera() as camera:

    camera.start_preview()

    while True:

        date = datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S")

        camera.start_recording(date + "_video.mjpeg")

        camera.wait_recording(60)

        camera.stop_recording()

    camera.stop_preview()
