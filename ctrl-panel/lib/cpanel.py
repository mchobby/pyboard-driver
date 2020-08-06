""" Class managing the NADHAT-CTRL-PANEL (Oled control panel with OLED)

See: https://github.com/mchobby/pyboard-driver/tree/master/ctrl-panel

domeu, 5 Aug 2020, Initial Writing (shop.mchobby.be)
----------------------------------------------------------------------------

MCHobby invest time and ressource in developping project and libraries.
It is a long and tedious work developed with Open-Source mind and freely available.
IF you like our work THEN help us by buying your product at MCHobby (shop.mchobby.be).

----------------------------------------------------------------------------
Copyright (C) 2020  - Meurisse D. (shop.mchobby.be)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>
"""
__version__ = '0.0.1'

from machine import Pin
from SSD1306 import SSD1306_I2C
from mcp230xx import MCP23017
import time


# Button_name = MCP_GPIO_nr
SW1  = 14
SW3  = 8
SW4  = 15
UP   = 11
DOWN = 9
LEFT = 13
RIGHT= 10
CLICK= 12 # Labeled CTR

class MCPEdge( MCP23017 ):
	""" Class managing and signaling the state change """

	def __init__(self, i2c, address=0x21, falling_edge=True ):
		super().__init__(i2c,address)
		self.falling_edge = falling_edge # Falling edge detection
		self.last_gpio = bytearray(self.gpio_bytes) # retain last GPIO reading
		self.edge_count = bytearray(self.NUM_GPIO) # Count the number of falling edges since last has_changed( pin ) read
		self.edge_gpios = []

	def old_input( self, pin ):
		# return the Old Status of a pin
		return (self.last_gpio[int(pin/8)] & 1 << (int(pin%8))) > 0

	def is_input( self, pin ):
		# Check if a pin is configured as Input
		return self.iodir[int(pin/8)] & (1 << int(pin%8)) > 0

	def edge_begin( self, edge_gpios ):
		""" Call it after initialization of GPIO In/Out to collect last values of the list of GPIOs to monitor for EDGES. """
		assert type(edge_gpios) is list, "edge_gpios must be a list"

		self.edge_gpios = edge_gpios
		self.read_gpio()
		for i in range(self.gpio_bytes):
			self.last_gpio[i] = self.gpio[i]

	def update( self ):
		# Call it after a read_gpio from main code

		# Check if at least one change for input pins
		#for item in [ (pin,self.input(pin,read=False),self.old_input(pin)) for pin in range(self.NUM_GPIO) if self.is_input(pin)]:
		#	print(item)

		if not any( [self.input(pin,read=False) != self.old_input(pin) for pin in self.edge_gpios if self.is_input(pin)] ):
			return
		# debouncing - only process updates if last check reveal a difference
		time.sleep_ms(10)
		self.read_gpio()
		for pin in  self.edge_gpios:
			if self.is_input(pin) and (self.input(pin,read=False) != self.old_input(pin)):
				# is falling edge
				if self.falling_edge and (self.old_input(pin) and not(self.input(pin,read=False)) ):
					self.edge_count[pin] += 1
				elif not(self.falling_edge) and ( not(self.old_input(pin)) and self.input(pin,read=False) ):
					self.edge_count[pin] += 1
		for i in range(self.gpio_bytes):
			self.last_gpio[i] = self.gpio[i]

	def edges( self, pin ):
		""" Return the number of edge counts for a pin then reset it """
		assert pin in self.edge_gpios, "%s not in edge_gpios" % pin
		r = self.edge_count[pin]
		self.edge_count[pin] = 0
		return r

class CtrlPanel:
	def __init__( self, i2c ):
		self.i2c = i2c

		self._mcp = MCPEdge( i2c, address=0x21, falling_edge=True )
		# Configure PinOut
		#   GPA0..GPA3 are input
		for pin in range( 0, 4 ):
			self._mcp.setup( pin, Pin.IN )
			# GPA0, GPA1, GPA3 needs for PullUp because the 910K external Pull up is too weak
			# GPA2 is an INT active @ low level --> Need a pull-up!
			self._mcp.pullup( pin, True  )
		#  GPA4..GPA7 are output
		for pin in range( 4, 8 ):
			self._mcp.setup( pin, Pin.OUT )
		#  GPB0..GPB7 are input (for the buttons)
		for pin in range( 8, 16 ):
			self._mcp.setup( pin, Pin.IN )
		self._mcp.edge_begin( [SW1, SW3, SW4, UP, DOWN, LEFT, RIGHT, CLICK] ) # Initialize Edge counter
		self.oled_reset()

		self.oled = SSD1306_I2C(width=128, height=64, i2c=i2c, addr=0x3c, external_vcc=True)
		self.oled.init_display()

	def oled_reset( self ):
		""" Reinitialize the OLED driver """
		self._mcp.output_pins( {6:False,7:False} )
		time.sleep_ms(1)
		self._mcp.output_pins( {6:True,7:True} )

	def update( self ):
		# read the GPIO
		self._mcp.read_gpio() # Just read all the GPIOs (2 bytes)
		self._mcp.update() # Update edges counters

	def is_down( self, btn_gpio ):
		# check if the button is down
		return self._mcp.input(btn_gpio, read=False)==False # Low when pressed, Do not reread

	def edges( self, btn_gpio ):
		return self._mcp.edges(btn_gpio)

	@property
	def request_off( self ):
		return self._mcp.input(3, read=False) == False

	@property
	def green( self ):
		return self._mcp.input( 4, read=False ) # Just need to read the stored value

	@green.setter
	def green( self, value ):
		self._mcp.output( 4, value )

	@property
	def red( self ):
		return self._mcp.input( 5, read=False ) # Just need to read the stored value

	@red.setter
	def red( self, value ):
		self._mcp.output( 5, value )
