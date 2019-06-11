# @Author: archer
# @Date:   2019-06-10T10:52:23+01:00
# @Last modified by:   archer
# @Last modified time: 2019-06-11T12:29:31+01:00

import sys, os, time

class Cam():
    """
    Raspberry pi Camera V2 abstraction library

    This Class fascilitates high level control of the camera module so that the
    minor points can just be abstracted away and kept cleanly in a class
    """
    import picamera

    def __init__(self, args={}):
        """
        __init__ can take an argument dict with state overides.
        The defaults that can be overridden (others will have no affect) are:

        args = {
            "rotation": 0,
            "resolution": (1280, 720),
            "framerate": 30,
        }
        """
        self.args = None
        self.cam = None
        self.args = self._processArgs(args)
        # self.cam = self.picamera.PiCamera()
        # self.settings(args)

    def settings(self, args={}):
        self.args = self._processArgs(args)
        self._setCameraState(self.args)

    def _processArgs(self, args={}):
        """
        Process the input args to ensure each one exists using fallbacks
        """
        # check what locals and globals are availiable
        print("globals:", locals())
        print("locals:",  globals())
        # fallback dict containing default values
        if(self.args is None):
            fallback = {
                "rotation": 0,
                "resolution": (1280, 720),
                "framerate": 30,
                "brightness": 50,
                "image_effect": "none",
            }
        else:
            fallback = self.args
        # creating a new dict from previous dicts combined overriding fallbacks
        try:
            return {**fallback, **args}
        except TypeError:
            etype, value, traceback = sys.exc_info()
            print(etype, value)
            raise TypeError(
                "The argument passed in to Cam() is not of type dict")

    def _setCameraState(self, args):
        """
        Private function to set the camera state from processed args
        """
        self.cam.rotation = args["rotation"]
        self.cam.resolution = args["resolution"]
        self.cam.framerate = args["framerate"]
        self.cam.brightness = args["brightness"]
        self.cam.image_effect = args["image_effect"]

    def debug(self):
        """
        debug function to display the internal state of the class and args

        uses yaml.dump to print nicer or fallback print if unavailiable
        """
        try:
            import yaml
            print("\nCam(args):\n\n",yaml.dump(self.args, allow_unicode=True,
                default_flow_style=False))
        except ModuleNotFoundError:
            print("\nCam(args):\n", self.args, "\n")

    def record(self, args={}):
        with self.picamera.PiCamera() as self.cam:
            # set camera settings + update class state
            self.settings(args)
            self.cam.start_preview()
            time.sleep(2)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

if(__name__ == "__main__"):
    arg_d = {}
    cam = Cam(arg_d)
    cam.debug()
    cam.record()
