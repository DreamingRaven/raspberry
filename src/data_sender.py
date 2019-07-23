# @Author: George Onoufriou <archer>
# @Date:   2019-07-23
# @Email:  george raven community at pm dot me
# @Filename: data_sender.py
# @Last modified by:   archer
# @Last modified time: 2019-07-23
# @License: Please see LICENSE in project root


from __future__ import absolute_import, division, print_function
from SimpleDataTransport import DataReceiver


def respond_to_weather_request(request):
    """Get weather data."""
    return {
        "temperature": 0.0,
        "pressure": 0.0,
        "humidity": 0.0,
        "air_quality": 0.0,
    }


if __name__ == '__main__':
    receiver = DataReceiver(host="0.0.0.0", port=5000,
                            callback=respond_to_weather_request,
                            endpoint="/api/weather")
    receiver.run()
