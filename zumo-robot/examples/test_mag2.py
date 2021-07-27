""" test_mag2.py - read and display magnetometer data using the properties

See project source @ https://github.com/mchobby/pyboard-driver/tree/master/zumo-robot

23 jul 2021 - domeu - initial writing
"""
from zumoshield import ZumoShield
from machine import I2C
from lsm303 import LSM303, MAGGAIN_2, MAGRATE_100
import time

zumo = ZumoShield() # Will stop motors
i2c = I2C(2)

lsm = LSM303(i2c)
lsm.enableDefault()
lsm.mag_gain = MAGGAIN_2  # Magnetometer gauss avec high resolution
lsm.mag_rate = MAGRATE_100 # magnetometre data rates

while True:
	# Magnetometer values as (X, Y, Z) in microteslas (as )signed floats) """
	print( 'x: %f, y: %f, z: %f in MicroTesla' % lsm.magnetic )
	time.sleep( 0.300 )
