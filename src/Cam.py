# @Author: archer
# @Date:   2019-06-10T10:52:23+01:00
# @Last modified by:   archer
# @Last modified time: 2019-06-13T13:35:03+01:00

import sys, os, time, io

class Cam():
    """
    Raspberry pi Camera V2 abstraction library

    This Class fascilitates high level control of the camera module so that the
    minor points can just be abstracted away and kept cleanly in a class
    """
    import picamera
    from PIL import Image, ImageChops, ImageStat

    def __init__(self, args={}):
        """
        __init__ can take an argument dict with state overides.
        The defaults that can be overridden (others will have no affect) are:

        args = {
            "rotation": 0,
            "resolution": (1280, 720),
            "framerate": 30,
            "brightness": 50,
            "image_effect": "none",
        }
        """
        self.args = None
        self.cam = None
        self.prior_image = None
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
        # check what locals and globals are availiable
        print("globals:", locals())
        print("locals:",  globals())

    def record(self, args={}):
        with self.picamera.PiCamera() as self.cam:
            # set camera settings + update class state
            self.settings(args)
            self.cam.start_preview()
            time.sleep(2)
            frames=100

            start = time.time()
            while True:
                timer = time.time()
                self.detect_motion()
                print("^ time taken: ", time.time() - timer)
            self.cam.capture_sequence([
                str(time.strftime("%Y-%m-%d_%H:%M:%S", time.gmtime())) +
                '_%02d.jpg' % i
                for i in range(frames)
                ], use_video_port=True)

            finish = time.time()
            print('Captured %d frames at %.2ffps' % (
            frames,
            frames / (finish - start)))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def detect_motion(self):
        stream = io.BytesIO()
        self.cam.capture(stream, format='jpeg', use_video_port=True)
        stream.seek(0)
        if self.prior_image is None:
            self.prior_image = self.Image.open(stream)
            return False
        else:
            current_image = self.Image.open(stream)

            diff = self.ImageChops.difference(current_image, self.prior_image)
            print("difference: ", self.ImageStat.sum(diff))

            # Compare current_image to prior_image to detect motion. This is
            # left as an exercise for the reader!
            result = False
            # Once motion detection is done, make the prior image the current
            self.prior_image = current_image
            return result

if(__name__ == "__main__"):
    with Cam({"framerate":30}) as cam_test:
        cam_test.debug()
        cam_test.record()

    # cam = Cam()
    # cam.debug()
    # cam.record()
