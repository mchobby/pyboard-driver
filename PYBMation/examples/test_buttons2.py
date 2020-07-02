"""
test_buttons2.py - Optimized read of all entries (also on the I2C bus where
  only 3 bytes are transfered

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

while True:
	# read all entries with one optimized operation
	lst = pm.all_buttons()
	print( lst )
	sleep(1)
