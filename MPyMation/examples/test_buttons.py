"""
test_buttons.py - Read the value of each buttons

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

val = {5:None,6:None,7:None,8:None,9:None,10:None,11:None,12:None}

while True:
	# read the value and store into the dictionnary
	for btn in range( 5, 13 ): # As labelled on the board
		val[btn] = pm.button(btn)

	print( val ) # Nice display on REPL
	sleep(1)
