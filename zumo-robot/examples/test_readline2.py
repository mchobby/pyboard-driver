""" test_readline2.py - version of test_readline.py using the ZumoShield class.

See project source @ https://github.com/mchobby/pyboard-driver/tree/master/zumo-robot

23 jul 2021 - domeu - initial writing
"""
# Arrêter les moteurs
from zumoshield import ZumoShield
import time
zumo = ZumoShield()

# Move the Zumo over the line while calibrating (in 10 steps).
# This will helps to identifies the white/black contrast.
#
for i in range(10):
	print( "Calibrate %i / 10" % (i+1) )
	zumo.ir.calibrate()
	time.sleep(0.5)

# Read the line position
#
while True:
	sensors = [0 for i in range(6)]
	# With the Zumo blade going forward
	#   Value from 500 to 4500 : line is placed from left to right
	#   value 2500 : line centered on the zumo
	#   value 0 : line exceed on the left
	#   value 5000 : line exceed on the right
	position = zumo.ir.readLine( sensors )
	print( 'Line position: ', position )
	time.sleep( 1 )
