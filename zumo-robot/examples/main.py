"""
main.py - the minimalist main.py - just avoids the motors to starts.

* Author(s):  Meurisse D. from MCHobby (shop.mchobby.be).

See project source @ https://github.com/mchobby/pyboard-driver/tree/master/zumo-robot
REQUIRES library zumoshield.py in the project source
"""

from zumoshield import ZumoMotor
from pyb import LED

z = ZumoMotor() # will stop the motors

# Light Up the Blue LED
LED(4).on()
