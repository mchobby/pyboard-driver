"""
ws2812.py - easy to use library for PYBStick-RP2040.

* Author(s): Meurisse D. from MCHobby (shop.mchobby.be).

See project source @ https://github.com/mchobby/pyboard-driver/tree/master/PYBStick-RP2040

"""
import array
from machine import Pin
import rp2
import time

# WS2812 default configuration.
NUM_LEDS = 8 # Nombre de LEDs
PIN_NUM = 11 # Broche de sortie
BRIGHTNESS = 0.2 # Luminosité (0 à 1, 0.2 est déjà très lumineux)

######################## NEOPIXEL UTILITY ######################################
@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def _ws2812():
	T1 = 2
	T2 = 5
	T3 = 3
	wrap_target()
	label("bitloop")
	out(x, 1)               .side(0)    [T3 - 1]
	jmp(not_x, "do_zero")   .side(1)    [T1 - 1]
	jmp("bitloop")          .side(1)    [T2 - 1]
	label("do_zero")
	nop()                   .side(0)    [T2 - 1]
	wrap()

BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
COLORS = (BLACK, RED, YELLOW, GREEN, CYAN, BLUE, PURPLE, WHITE)

class WS2812():

	def __init__( self, pin_num = PIN_NUM, num_leds=NUM_LEDS, brightness=BRIGHTNESS ):
		self.pin_num = pin_num
		self.num_leds = num_leds
		self.brightness = brightness
		# Create the StateMachine with the ws2812 program, outputting on pin
		self.sm = rp2.StateMachine(0, _ws2812, freq=8_000_000, sideset_base=Pin(self.pin_num))
		# Start the StateMachine, it will wait for data on its FIFO.
		self.sm.active(1)
		# Display a pattern on the LEDs via an array of LED RGB values.
		self.ar = array.array("I", [0 for _ in range(self.num_leds)])

	def show( self ):
		""" Should also receive a data parameter (list of color tuples) to be fully compatible with esp8266-upy/neopixel/ """
		dimmer_ar = array.array("I", [0 for _ in range(self.num_leds)])
		for i,c in enumerate(self.ar):
			r = int(((c >> 8) & 0xFF) * self.brightness)
			g = int(((c >> 16) & 0xFF) * self.brightness)
			b = int((c & 0xFF) * self.brightness)
			dimmer_ar[i] = (g<<16) + (r<<8) + b
		self.sm.put(dimmer_ar, 8)
		time.sleep_ms(10)

	write = show

	def set(self, index, color):
		""" Assigne une couleur (r,g,b) à un pixel numéroté de 0 à N-1 """
		self.ar[index] = (color[1]<<16) + (color[0]<<8) + color[2]

	def __setitem__( self, index, color ):
		self.set( index, color )

	def fill( self, color):
		""" Remplit le ruban avec une couleur donnée """
		for i in range(self.num_leds):
			self.set(i, color)

	def clear( self ):
		self.fill( BLACK )
		self.show()

	@property
	def pixels( self ):
		return self.ar

	@property
	def count( self ):
		return self.num_leds

	n = count


##########################################################################
