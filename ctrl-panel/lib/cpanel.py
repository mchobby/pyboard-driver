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

class CtrlPanel:
	def __init__( self, i2c ):
		self.i2c = i2c

		self._mcp = MCP23017( i2c, address=0x21 )
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

	def is_down( self, btn_gpio ):
		# check if the button is down
		return self._mcp.input(btn_gpio, read=False)==False # Low when pressed, Do not reread

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
