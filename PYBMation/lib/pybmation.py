from tca6424 import TCA6424
from machine import Pin

class PYBMation:
	def __init__( self, i2c ):
		self.i2c = i2c
		self.tca = TCA6424( i2c ) # on default address

		# Input buttons
		for i in range(8, 16): # P10 to P17
			self.tca.setup( i, Pin.IN, inversion=True )

		# Output LEDs
		for i in range(16,24): # P20 to P27
			self.tca.setup( i, Pin.OUT, inversion=True, value=False )

		# Output relay
		for i in range(0,8): # P0 to P7
			self.tca.setup( i, Pin.OUT, value=False )
		self.tca.apply_setup()

	def button( self, btn_index ):
		""" btn_index from 5 to 12 as written on the board. refresh=True, force TCA reading before returning value. """
		assert 5 <= btn_index <= 12, 'Invalid button index (5..12)'
		# button wired to entries 8 to 15
		pin = btn_index + 3
		return self.tca.input( pin )

	def all_buttons( self ):
		""" Return a list with the state of all the buttons (from 5 to 12) """
		self.tca.all_inputs() # Optimized read 
		r = []
		for btn_index in range( 5, 13 ):
			r.append( self.tca.input( btn_index+3, refresh=False) )
		return r


	def led( self, led_index, value=None ):
		""" led_index from 5 to 12 as written on the board. Value None will re-read the state """
		assert 5 <= led_index <= 12, 'Invalid led index (5..12)'
		# leds wired to entries 8 to 15
		pin = led_index + 11
		return self.tca.output( pin, value )

	def all_leds( self, value ):
		""" Change the status of all leds @ once """
		for i in range( 5, 13 ):
			self.tca.output( i+11, value )

	def relay( self, relay_index, value=None ):
		""" relay_index from 5 to 12 as written on the board. Value None will re-read the state """
		assert 5 <= relay_index <= 12, 'Invalid relay index (5..12)'
		# relay wired to entries 0 to 7
		pin = relay_index-5
		return self.tca.output( pin, value )
