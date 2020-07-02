"""
test_init.py - Just check the initial state of the PYBMation

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
