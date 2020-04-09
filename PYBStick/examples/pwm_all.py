"""
pwm_all.py - Test each PWM output, once every-time.
Press the user Switch (A) button to move the PWM test to the NEXT PIN.

WARNING: ALL PINS WILL BE SET AS PWM OUTPUT with duty cycle from 0 to 100%

* Author(s): Meurisse D. from MCHobby (shop.mchobby.be).

See project source @ https://github.com/mchobby/pyboard-driver/tree/master/PYBStick
"""
from pyb import Switch
from time import sleep_ms, sleep
from pwm  import *

import micropython
micropython.alloc_emergency_exception_buf(100)

# List of pin to test
PINS = [ "S3", "S5", "S7", "S11", "S13", "S19", "S21", "S23", "S8",
		 "S10", "S12", "S16", "S18", "S22", "S24" ]

PIN_NAMES = PINS

__idx = -1

sw = Switch()
def setup_next_pin():
	global sw
	sw.callback( None )
	global __idx
	if __idx+1 >= len(PINS):
		__idx = 0
	else:
		__idx += 1
	sleep( 0.5 )
	sw.callback(setup_next_pin)

sw.callback( setup_next_pin )

print( "Press the A switch (USR button) to select next PIN" )
__pin = None
__current_idx = __idx
while True:
	# Do we change the Pin ?
	if __idx != __current_idx:
		# reconfigure as input (High impedance)
		if __pin:
			__pin.release()

		__pin = pwm( PINS[__idx] )
		__pin.percent = 33 # 33% duty cycle
		__current_idx = __idx
		print( "Setting PWM on pin %s" % PIN_NAMES[__idx] )

	# Pulse the current Pin
	if __pin:
		if __pin.percent < 100:
			__pin.percent += 1
		else:
			__pin.percent = 0
		sleep_ms(10)
