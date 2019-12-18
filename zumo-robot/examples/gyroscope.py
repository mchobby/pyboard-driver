"""
gyroscope.py - easy gyroscope Example for Pyboard Original.

* Author(s):    Braccio M.  from MCHobby (shop.mchobby.be).
                Meurisse D. from MCHobby (shop.mchobby.be).

See project source @ https://github.com/mchobby/pyboard-driver/tree/master/zumo-robot
REQUIRES library L3G.py in the project source
"""
#
# The MIT License (MIT)
#
# Copyright (c) 2019 Meurisse D. for MC Hobby
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR INfrom zumoshield import ZumoMotor
from accel import L3GD20, L3GD20_I2C
from machine import I2C
from pyb import Timer
import pyb
import time
import struct
#Speed of the zumo motors
SPEED = 150

"""Starting with the configuration of the I2C communication"""
i2c = I2C(2)
i2c.scan()
print("I2C devices: %s" %i2c.scan())
gyro= L3GD20_I2C(i2c)
motors = ZumoMotor()

while(True):

    gyro_values = gyro.read()
    print(gyro_values)
    time.sleep(2)

    """Turning around the Z-axis clockwise. Z-value should increase in the positive values """
    #motors.setSpeeds(SPEED,-SPEED)

    """Turning around the Z-axis counter-clockwise. Z-axis should increase in the negative values"""
    #motors.setSpeeds(-SPEED,SPEED)
