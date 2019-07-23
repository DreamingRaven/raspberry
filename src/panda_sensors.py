# @Author: archer
# @Date:   2019-07-21T21:14:14+01:00
# @Last modified by:   archer
# @Last modified time: 2019-07-23


from __future__ import print_function, absolute_import   # python 2-3 compat
import os
import time
import datetime


class Sense(object):
    """Raspberry Pi specific class to put sensor data into pandas files."""

    def __init__(self, args=None, logger=None):
        """Create object and test what is availiable."""
        args = args if args is not None else dict()
        self.home = os.path.expanduser("~")
        defaults = {
            "cam": None,
            "bme680": None,
            "cam_wanted": True,
            "bme680_wanted": True,
            "cam_import_attempts": 2,
            "cam_resolution": (1920, 1080),
            "pylog": logger if logger is not None else print,
        }
        self.args = self._merge_dicts(defaults, args)

    __init__.__annotations__ = {"args": dict, "return": None}

    def debug(self):
        """Log function to help track the internal state of the class."""
        self.args["pylog"](self.args)

    debug.__annotations__ = {"return": None}

    def _merge_dicts(self, *dicts):
        """Given multiple dictionaries, merge together in order."""
        result = {}
        for dictionary in dicts:
            result.update(dictionary)  # merge each dictionary in order
        return result

    _merge_dicts.__annotations__ = {"dicts": dict, "return": None}

    def _init_camera(self):
        """Check that camera library and camera can be used."""
        # a quick note the camera may fail the first time around
        # so we need to init it twice thanks to poor lower level code
        try:  # try to import camera
            import picamera
            for _ in range(self.args["cam_import_attempts"]):
                try:  # try to init camera _ times
                    self.args["cam"] = picamera.PiCamera()
                    self.args["cam"].start_preview()
                    return True
                except picamera.exc.PiCameraMMALError:
                    self.args["pylog"]("warning: unable to start camera")
        except ImportError:
            self.args["pylog"]("warning: unable to import picamera")
        self.args["pylog"]("warning: skipping camera")
        return False

    _init_camera.__annotations__ = {"return": bool}

    def _init_bme680(self):
        """Check that bme680 library and bme680 can be used."""
        try:
            import bme680
            sensor = bme680.BME680()
            sensor.set_humidity_oversample(bme680.OS_2X)
            sensor.set_pressure_oversample(bme680.OS_4X)
            sensor.set_temperature_oversample(bme680.OS_8X)
            sensor.set_filter(bme680.FILTER_SIZE_3)
            sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
            sensor.set_gas_heater_temperature(320)
            sensor.set_gas_heater_duration(150)
            sensor.select_gas_heater_profile(0)
            self.args["bme680"] = sensor
            return True
        except ImportError:
            self.args["pylog"]("warning: unable to import bme680")
        except NameError:
            self.args["pylog"]("warning unable to use bme680")
        self.args["pylog"]("warning: skipping bme680")
        return False

    _init_bme680.__annotations__ = {"return": bool}

    def getWeatherData(self, requests=None):
        """Record weather and camera data if availiable and return dict."""
        # while(self.args["cam"] is not None)or(self.args["bme680"] is not None):
        sensor_data = {
            "datetime_utc_now": datetime.datetime.utcnow().isoformat(),
        }
        if(self.args["cam"] is not None):
            pass
        if(self.args["bme680"] is not None):
            sensor_data["temperature"] = \
                self.args["bme680"].data.temperature
            sensor_data["pressure"] = \
                self.args["bme680"].data.pressure
            sensor_data["humidity"] = \
                self.args["bme680"].data.humidity
            sensor_data["air_quality"] = \
                self.args["bme680"].data.gas_resistance
        return sensor_data


def test():
    sensors = Sense()
    sensors._init_camera()
    sensors._init_bme680()
    sensors.debug()
    print(sensors.getWeatherData())
    time.sleep(1)
    print(sensors.getWeatherData())
    time.sleep(1)
    print(sensors.getWeatherData())
    time.sleep(1)
    print(sensors.getWeatherData())
    time.sleep(1)

    def getWeatherData(request):
        return {"hi": "Raymond"}
        # for data in sensors:
        #     yield data

    from SimpleDataTransport import DataReceiver
    receiver = DataReceiver(host="0.0.0.0", port=5000,
                            callback=sensors.getWeatherData,
                            endpoint="/api/weather")
    receiver.run()


if(__name__ == "__main__"):
    test()
