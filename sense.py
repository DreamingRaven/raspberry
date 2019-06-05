# @Author: archer
# @Date:   2019-06-03T19:42:17+01:00
# @Last modified by:   archer
# @Last modified time: 2019-06-04T20:58:46+01:00

import os, sys
import time
import argparse

from pathlib import Path

home = str(Path.home())

def main():
    description = "Short script file to convert one delimited file type to another"
    args = argz(sys.argv[1:], description=description)
    print(args)
    print(args["resolution"], type(args["resolution"]))
    # create camera object and only continue if it is still valid
    try:
        import picamera
        with picamera.PiCamera() as cam:
            cam.resolution = (3280, 2464)
            cam.rotation = 180
            cam.start_preview()
            while(True):
                time.sleep(5)
                cam.capture(str(time.strftime("%Y-%m-%d_%H:%M:%S", time.gmtime())), 'png')
    except:
        print("failed")

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
    pathArgNames = ["data"]

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
