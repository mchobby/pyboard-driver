""" test_mag.py - read and display magnetometer data by accessing the magnetic vector

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
lsm.mag_gain = MAGGAIN_2  # Magnetometer gauss with high resolution
lsm.mag_rate = MAGRATE_100 # magnetometre data rates

while True:
	# read magnetic and accelerometer
	lsm.read()
	# Access the mangnetic vector.
	print( 'x', lsm.m.x, 'y', lsm.m.y )
	time.sleep( 0.300 )
