# Test each output one at once every-time the user Switch is pressed
#
# WARNING: ALL PINS WILL BE SET AS OUTPUT and cycle HIGH/LOW voltage

from uno import *
from pyb import Switch
from time import sleep_ms, sleep

import micropython
micropython.alloc_emergency_exception_buf(100)

# List of pin to test
PINS = [PIN_A0, PIN_A1, PIN_A2, PIN_A3, PIN_A4, PIN_A5,
	PIN_0, PIN_1, PIN_2, PIN_3, PIN_4, PIN_5, PIN_6, PIN_7,
	PIN_8, PIN_9, PIN_10, PIN_11, PIN_12, PIN_13 ]

PIN_NAMES = ["A0", "A1", "A2", "A3", "A4", "A5",
	"0", "1", "2", "3", "4", "5", "6", "7",
	"8", "9", "10", "11", "12", "13" ]

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
			__pin.init( mode=Pin.IN)
			del( __pin )
			__pin = None

		__pin = Pin( PINS[__idx], Pin.OUT, value=0 )
		__current_idx = __idx
		print( "Setting pin %s" %PIN_NAMES[__idx] )

	# Pulse the current Pin
	if __pin:
		__pin.value( not(__pin.value()))
		sleep_ms(10)
