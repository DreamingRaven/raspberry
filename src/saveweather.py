import time
import datetime

cam = None
try:
    import picamera
    try:
        cam = picamera.PiCamera()
    except picamera.exc.PiCameraMMALError:  # a hack
        cam = picamera.PiCamera()
except ImportError:
    print("warning: unable to use camera, picmera does not exist")

try:
    import bme680
except ImportError:
    print("warning: unable to use bme680, import bme680 failed")

sensor = bme680.BME680()
sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)
sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)

# print("UTC,C,hPa,%RH,Ohms")
while True:
    if sensor.get_sensor_data():

        output = "{3},{0:.2f},{1:.2f},{2:.2f}".format(
            sensor.data.temperature,
            sensor.data.pressure,
            sensor.data.humidity,
            datetime.datetime.utcnow().isoformat())

        if sensor.data.heat_stable:
            print("{0},{1}".format(output, sensor.data.gas_resistance))
        else:
            print(output)

    time.sleep(1)
