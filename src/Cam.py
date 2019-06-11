# @Author: archer
# @Date:   2019-06-10T10:52:23+01:00
# @Last modified by:   archer
# @Last modified time: 2019-06-11T11:28:42+01:00

import sys, os

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
        self.cam = self.picamera.PiCamera()
        self.settings(args)

    def settings(self, args={}):
        self._processArgs(args)
        self._setCameraState()

    def _processArgs(self, args={}):
        """
        Process the input args to ensure each one exists using fallbacks
        """
        # fallback dict containing default values
        fallback = {
            "rotation": 0,
            "resolution": (1280, 720),
            "framerate": 30,
            "brightness": 50,
            "image_effect": "none",
        }
        # creating a new dict from previous dicts combined overriding fallbacks
        try:
            self.args = {**fallback, **args}
        except TypeError:
            etype, value, traceback = sys.exc_info()
            print(etype, value)
            raise TypeError(
                "The argument passed in to Cam() is not of type dict")

    def _setCameraState(self):
        """
        Private function to set the camera state from processed args
        """
        self.cam.rotation = self.args["rotation"]
        self.cam.resolution = self.args["resolution"]
        self.cam.framerate = self.args["framerate"]
        self.cam.brightness = self.args["brightness"]
        self.cam.image_effect = self.args["image_effect"]

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

    def record():
        pass

if(__name__ == "__main__"):
    arg_d = {}
    cam = Cam(arg_d)
    cam.debug()
