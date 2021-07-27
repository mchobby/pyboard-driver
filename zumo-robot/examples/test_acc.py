""" test_acc.py - read and display accelerometer data by accessing the accelerator vector

See project source @ https://github.com/mchobby/pyboard-driver/tree/master/zumo-robot

23 jul 2021 - domeu - initial writing
"""
from zumoshield import ZumoShield
from machine import I2C
from lsm303 import LSM303
import time

zumo = ZumoShield() # Will stop motors
i2c = I2C(2)

lsm = LSM303(i2c)
lsm.enableDefault()

while True:
	# read magnetic and accelerometer
	lsm.read()
	# Access the accelerometer vector.
	print( 'x', lsm.a.x, 'y', lsm.a.y )
	time.sleep( 0.300 )
