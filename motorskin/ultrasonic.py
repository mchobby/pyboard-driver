##
# Ultrasonic library for MicroPython's pyboard.
# Compatible with HC-SR04 and SRF04.
#
# Copyright 2014 - Sergio Conde Gómez <skgsergio@gmail.com>
# Improved by Mithru Vigneshwara
# Improved by Meurisse Dominique (timeout handling instead of infinite loop)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Source: https://github.com/skgsergio/MicropythonLibs/blob/master/Ultrasonic/module/ultrasonic.py
# Special thanks to Sergio Conde Gómez
##

import pyb


class Ultrasonic:
    def __init__(self, tPin, ePin):
        # WARNING: Don't use PA4-X5 or PA5-X6 as echo pin without a 1k resistor
        self.triggerPin = tPin
        self.echoPin = ePin

        # Init trigger pin (out)
        self.trigger = pyb.Pin(self.triggerPin)
        self.trigger.init(pyb.Pin.OUT_PP, pyb.Pin.PULL_NONE)
        self.trigger.low()

        # Init echo pin (in)
        self.echo = pyb.Pin(self.echoPin)
        self.echo.init(pyb.Pin.IN, pyb.Pin.PULL_NONE)

    def distance_in_inches(self):
        return (self.distance_in_cm() * 0.3937)

    def distance_in_cm(self, timeout_value = 10000, timeout_us=330000):
        """ Return value in cm. Otherwise timeout_value in case of sensor timeout (0.33s = 100m = 10000cm) instead of infinite looping"""
        start = 0
        end = 0
        watch = 0 # Check if we are not over a timeout

        # Create a microseconds counter.
        micros = pyb.Timer(2, prescaler=83, period=0x3fffffff)
        micros.counter(0)

        # Send a 10us pulse.
        self.trigger.high()
        pyb.udelay(10)
        self.trigger.low()

        
        watch = micros.counter()

        # Wait 'till whe pulse starts.
        while self.echo.value() == 0:
            if micros.counter()-watch > timeout_us:
                return timeout_value 
            start = micros.counter()

        watch = micros.counter()

        # Wait 'till the pulse is gone.
        while self.echo.value() == 1:
            if micros.counter()-watch > timeout_us:
                return timeout_value             
            end = micros.counter()

        # Deinit the microseconds counter
        micros.deinit()

        # Calc the duration of the recieved pulse, divide the result by
        # 2 (round-trip) and divide it by 29 (the speed of sound is
        # 340 m/s and that is 29 us/cm).
        dist_in_cm = ((end - start) / 2) / 29

        return dist_in_cm
