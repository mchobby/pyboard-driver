# Test the OLED FeatherWing with the PYBStick-Feather-Face
#
# See Project: https://github.com/mchobby/pyboard-driver/tree/master/PYBStick-feather-face
#
# Rely on the adfmotors library for MicroPython available at
#     https://github.com/mchobby/esp8266-upy/tree/master/adfmotors
#
from motorwing import MotorWing
import time
from machine import I2C
i2c = I2C(1)
m = MotorWing( i2c, address=0x60 )

from motorbase import FORWARD, BACKWARD, BRAKE, RELEASE
from time import sleep

def test_motor( motor_obj ):
	""" Test the various DCMotor functionnalities """
	motor_obj.speed( 128 ) # Initial speed configuration
	print( "Foward")
	motor_obj.run( FORWARD )
	sleep( 3 )
	print( "Backward")
	motor_obj.run( BACKWARD )
	sleep( 3 )
	print( "Brake")
	motor_obj.run( BRAKE )
	sleep( 3 )
	print( "Accelerate" )
	# Warning: Setting speed to 0 will stop motor! New speed() followed by run()
	#          are required to restart motor rotation.
	motor_obj.speed( 1 )
	motor_obj.run( FORWARD )
	for speed in range( 1, 256 ): # 1 to 255
		motor_obj.speed( speed )
		sleep( 0.050 )
	print( "Decelerate" )
	for speed in range( 255, 0, -1 ): # 255 to 1
		motor_obj.speed( speed )
		sleep( 0.050 )
	print( "Speed 128")
	motor_obj.speed( 128 )
	sleep(2)
	print( "RELEASE" )
	motor_obj.run( RELEASE )

# Test the various motors on the MotorWing
for motor_nr in (1,2,3,4):
	print( "Motor M%s" % motor_nr )
	motor = m.get_motor(motor_nr)
	test_motor( motor )
