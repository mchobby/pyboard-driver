"""
test_leds.py - Allumer les différentes LEDs du module relais

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

for i in range( 5, 13 ): # As labelled on the board
	print( 'Light LED %i:' % i )
	pm.led( i, True )
	print( ' --> LED %i is %s' % (i, pm.led(i)) ) # Reread output state
	sleep(1)
	pm.led(i,False)
	print( ' --> LED %i is %s' % (i, pm.led(i)) )
