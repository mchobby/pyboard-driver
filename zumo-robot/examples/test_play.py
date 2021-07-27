""" test_play.py - just play a note

See project source @ https://github.com/mchobby/pyboard-driver/tree/master/zumo-robot

23 jul 2021 - domeu - initial writing
"""
from zumoshield import ZumoShield
zumo = ZumoShield()
zumo.buzzer.play(">g32>>c32")
