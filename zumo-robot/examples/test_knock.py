""" test_knock.py - detect when the Zumo is knocked on the front/read/left/right
    by analysing the accelerator vector.

	Note: it should be possible to write a better detection based on test_acc2.py

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

class MeanEval:
	""" Mean & Thresold calculator """

	def __init__( self, th_x = 20, th_y = 20 ):
		# Store the last 10 readings
		# th_x, th_y: Thresold of detection in X and Y position
		self.pos = 0
		self.x_val = [0,0,0,0,0,0,0,0,0,0]
		self.y_val = [0,0,0,0,0,0,0,0,0,0]
		self.th_x = th_x
		self.th_y = th_y

	def push( self, x, y ):
		self.x_val[self.pos] = x
		self.y_val[self.pos] = x
		self.pos += 1
		if self.pos > 0:
			self.pos = 0

	def mean( self ):
		# calculate the mean X,Y position
		return ( sum(self.x_val)/10, sum(self.y_val)/10 )

	def is_knock( self, x, y ):
		# check if the values is a knocking <0,0,>0 for each axis
		x_mean, y_mean = self.mean()
		x_delta, y_delta = 0, 0
		if abs( x-x_mean )>self.th_x:
			x_delta = x - x_mean
		if abs( y-y_mean )>self.th_y:
			y_delta = y - y_mean
		return x_delta, y_delta



print( 'Don t move... we calibrate')
mean_eval = MeanEval( th_x=1000, th_y=1000 ) # With threasold
for i in range(10):
	lsm.read()
	mean_eval.push( lsm.a.x, lsm.a.y )

print( 'Knock it' )
while True:
	# read magnetic and accelerometer
	lsm.read()
	# Access the accelerometer vector
	x,y = lsm.a.x, lsm.a.y

	xdelta,ydelta = mean_eval.is_knock(x,y)
	if (xdelta==0) & (ydelta==0): # No knocking detected
		mean_eval.push( x,y )
		continue

	print( '-----------------' )
	if xdelta < 0:
		print( "FRONT knock" )
	elif xdelta > 0:
		print( "BACK knock" )

	if ydelta < 0:
		print( "LEFT knock" )
	elif ydelta > 0:
		print( "RIGHT knock" )

	time.sleep( 0.100 )
