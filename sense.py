# @Author: archer
# @Date:   2019-06-03T19:42:17+01:00
# @Last modified by:   archer
# @Last modified time: 2019-06-04T20:58:46+01:00

import os, sys
import time
import argparse

from pathlib import Path
import io
import random
import picamera
from PIL import Image

prior_image = None

home = str(Path.home())

def main():
    description = "Short script file to convert one delimited file type to another"
    args = argz(sys.argv[1:], description=description)
    print(args)
    print(args["resolution"], type(args["resolution"]))

    main_loop(args)
    # create camera object and only continue if it is still valid
    # try:
    #     import picamera
    #     with picamera.PiCamera() as cam:
    #         cam.resolution = (3280, 2464)
    #         cam.rotation = 180
    #         cam.start_preview()
    #         while(True):
    #             time.sleep(5)
    #             cam.capture(str(time.strftime("%Y-%m-%d_%H:%M:%S", time.gmtime())), 'png')
    # except:
    #     print("failed")

def main_loop(args):

    def detect_motion(camera):
        global prior_image
        stream = io.BytesIO()
        camera.capture(stream, format='jpeg', use_video_port=True)
        stream.seek(0)
        if prior_image is None:
            prior_image = Image.open(stream)
            return False
        else:
            current_image = Image.open(stream)
            # Compare current_image to prior_image to detect motion. This is
            # left as an exercise for the reader!
            result = random.randint(0, 10) == 0
            # Once motion detection is done, make the prior image the current
            prior_image = current_image
            return result

    with picamera.PiCamera() as camera:
        camera.resolution = (1280, 720)
        camera.rotation = 180
        stream = picamera.PiCameraCircularIO(camera, seconds=20)
        camera.start_recording(stream, format='h264')
        try:
            while True:
                camera.wait_recording(1)
                if detect_motion(camera):
                    print('Motion detected!')
                    # As soon as we detect motion, split the recording to
                    # record the frames "after" motion
                    camera.split_recording('after.h264')
                    # Write the 10 seconds "before" motion to disk as well
                    stream.copy_to('before.h264', seconds=10)
                    stream.clear()
                    # Wait until motion is no longer detected, then split
                    # recording back to the in-memory circular buffer
                    while detect_motion(camera):
                        camera.wait_recording(1)
                    print('Motion stopped!')
                    camera.split_recording(stream)
        finally:
            camera.stop_recording()

def resolution(s):
    try:
        x, y = map(int, s.split(','))
        return x, y
    except TypeError:
        raise argparse.ArgumentTypeError("Resolution must be x,y")

def argz(argv, description=None):
    """
    Argumet parser for command line args TODO: include config files
    """
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("-o", "--out-folder",
                        default=str(home),
                        help="set the output directory to dump images")
    parser.add_argument("-t", "--out-type",
                        default=str("png"),
                        help="set the output file suffix/ extension to attempt to write to")
    parser.add_argument("-r", "--resolution",
                        default=(3280, 2464),
                        type=resolution,
                        nargs=2,
                        help="set the output file suffix/ extension to attempt to write to")
    # parser.add_argument("-d", "--data", nargs='+',
    #                     default=[],
    #                     help="path to each file desired to be converted")

    # parse the initial args which have only been slightly sanitised
    args = vars(parser.parse_args(argv))

    # list args which are paths to be made cross platform
    pathArgNames = ["out_folder"]

    # return normalised args with cross platform paths
    return normArgs(args=args, pathArgs=pathArgNames)


def normArgs(args, pathArgs):
    """
    Argument normaliser to convert paths or lists of paths to cross platform
    """
    for argName in pathArgs:
        if(type(args[argName]) != list):
            args[argName] = str(os.path.abspath(args[argName]))
        else:
            tempList = list()
            for listItem in args[argName]:
                tempList.append(str(os.path.abspath(listItem)))
            args[argName] = tempList
    return args


if __name__ == "__main__":
    main()
