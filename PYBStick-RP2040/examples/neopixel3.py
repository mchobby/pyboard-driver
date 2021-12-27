"""
 Example using the ws2812/NeoPixel  PIO library for RP2040 based boardts.

 * Author(s): Meurisse D. from MCHobby (shop.mchobby.be).

 See project source @ https://github.com/mchobby/pyboard-driver/tree/master/PYBStick-RP2040
"""

import ws2812 as ws
import time

leds = ws.WS2812( pin_num=11, num_leds=12, brightness=0.2 )
for color in ws.COLORS:
	leds.fill(color)
	leds.write() # show() will also work
	time.sleep(0.2)

leds.clear()

#print("rainbow")
#rainbow_cycle(0)
