"""
test_pwm_all.py - Test each PWM output, once every-time.
Press the user Switch (A) button to move the PWM test to the NEXT PIN.

WARNING: ALL PINS WILL BE SET AS PWM OUTPUT with duty cycle from 0 to 100%

* Author(s): Meurisse D. from MCHobby (shop.mchobby.be).

See project source @ https://github.com/mchobby/pyboard-driver/tree/master/UNO-R3
"""
from uno import *
from pyb import Switch
from time import sleep_ms, sleep
from pwm  import *

import micropython
micropython.alloc_emergency_exception_buf(100)

# List of pin to test
PINS = [PIN_A5,
	PIN_0, PIN_1, PIN_2, PIN_3, PIN_4, PIN_5, PIN_6,
	PIN_8, PIN_9, PIN_10, PIN_11, PIN_12, PIN_13,
	"Y10", "Y9" ]

PIN_NAMES = ["A5",
	"0", "1", "2", "3", "4", "5", "6",
	"8", "9", "10", "11", "12", "13",
	"Y10-SDA", "Y9-SCL" ]

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
