"""
test_relays.py - Active les différents relays du module

Voir projet:
---> https://github.com/mchobby/pyboard-driver/tree/master/PYBMation

------------------------------------------------------------------------

History:
  28 june 2020 - Meurisse D. - initial code
"""

from machine import I2C
from pybmation import PYBMation
from time import sleep

i2c = I2C(1)
pm = PYBMation( i2c )

for i in range( 5, 13 ): # As labelled on the board
	print( 'Activate relay %i:' % i )
	pm.relay( i, True )
	print( ' --> Relay %i is %s' % (i, pm.relay(i)) ) # Reread output state
	sleep(1)
	pm.relay(i,False)
	print( ' --> Relay %i is %s' % (i, pm.relay(i)) )
