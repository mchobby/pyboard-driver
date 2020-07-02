"""
test_blink.py - Blink the relay and the led when pressing the corresponding
button.

Voir projet:
---> https://github.com/mchobby/pyboard-driver/tree/master/PYBMation

------------------------------------------------------------------------

History:
  27 june 2020 - Meurisse D. - initial code
"""

from machine import I2C
from pybmation import PYBMation
from time import sleep

i2c = I2C(1)
pm = PYBMation( i2c )

# Inform user that interface is ready
pm.all_leds(True)
sleep(0.5)
pm.all_leds(False)

# Detect pressed button
pressed = None
while True:
	# read the value and store into the dictionnary
	for btn in range( 5, 13 ): # As labelled on the board
		if pm.button(btn):
			pressed = btn

	if pressed:
		for i in range(3):
			pm.relay(pressed,True)
			pm.led(pressed,True)
			sleep(1)
			pm.relay(pressed,False)
			pm.led(pressed,False)
			sleep(1)
		pressed = None
