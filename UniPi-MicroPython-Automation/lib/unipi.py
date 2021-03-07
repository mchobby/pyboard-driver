""" UniPi module for MicroPython - Manage the UniPi interface

	See PybStick-UniPi interface @ MCHobby
	https://shop.mchobby.be/fr/nouveaute/1891-carte-interface-unipi-pro-et-lite-pour-pybstick-3232100018914.html

	See project https://github.com/mchobby/pyboard-driver/tree/master/UniPi-MicroPython-Automation

	domeu, 02 june 2020, Initial Writing (shop.mchobby.be)
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

from machine import I2C, SPI, UART, Pin
from pyb import Timer
from mcp230xx import MCP23017, MCP23008
from eeprom24Cxx import Eeprom_24C02C
import struct

BOARD_PYBSTICK = 0
BOARD_PYBOARD  = 1

DEFAULT_ADC_FACTOR = 5.54 # ADC have voltage Divider 10K + 2K. More precise value is stored into the EEPROM

def input_to_gp( input_nr ):
	""" Transform the input_nr 1..14 to the GPIO_nr (0..15) on the MCP23017 """
	assert 1 <= input_nr <= 14, "Invalid input nr %s" % input_nr
	# GPIO A0=0 & B0=8 are still available
	if input_nr <= 7:
		return input_nr
	else:
		return input_nr+1

class UniPiError( Exception ):
	pass

class UniPi:
	def __init__( self, i2c, board ):
		self.i2c = i2c # main bus for controling the UniPi interface
		self.board = board # Type of the board BOARD_PYBOARD

		# --- Relays ---
		try:
			self._relays = MCP23008(i2c,0x20)
		except OSError as err:
			if err.args[0] == 19: # ENODEV
				raise UniPiError( "UniPi board missing or not powered (ENODEV)!" )
			else:
				raise
		# Set all pins as output
		for i in range(8):
			self._relays.setup(i,Pin.OUT)

		# --- Inputs ---
		self._inputs = MCP23017(i2c,0x27)
		# Set all pins as input
		for i in range(1,15): # 1 to 14
			self._inputs.setup( input_to_gp(i), Pin.IN )
			self._inputs.pullup( input_to_gp(i), True )

		# --- Access EEPROM ---
		self.eeprom = UniPiEeprom( self.i2c, addr=0x50 )
		# EEprom must be formatted properly !
		if not self.eeprom.check_unipi():
			raise UniPiError( 'Invalid UniPi Magic Key' )
		# Read coef back from eeprom (should be close from 5.54)
		adc_scale_0, adc_scale_1 = self.eeprom.analog_input_coefs

		# --- ADCs ---
		from mcp342x import MCP342x
		self._adc_channels = [
			MCP342x(i2c, 0x68, channel=0, resolution=12, gain=1, scale_factor=adc_scale_0),
			MCP342x(i2c, 0x68, channel=1, resolution=12, gain=1, scale_factor=adc_scale_1) ]

		# Assign facades
		self.relays = RelayFacade( self._relays )
		self.inputs = InputFacade( self._inputs )
		self.adcs   = AdcFacade( self._adc_channels )
		self.uext   = UExtFacade( self )

		# Analog 0 (controled via PWM)
		self._A0_percent = 0
		if self.board == BOARD_PYBSTICK:
			self._pin_A0 = Pin( 'S12' )
			self._tim2 = Timer(2, freq=500 ) # 500 Hz like Arduino
			self._ch_A0 = self._tim2.channel( 1, Timer.PWM, pin=self._pin_A0 ) # Channel 1
			self._ch_A0.pulse_width_percent( self._A0_percent )
		elif self.board == BOARD_PYBOARD:
			self._pin_A0 = Pin( 'X4' )
			self._tim2 = Timer(2, freq=500 ) # 500 Hz like Arduino
			self._ch_A0 = self._tim2.channel( 4, Timer.PWM, pin=self._pin_A0 ) # Channel 1
			self._ch_A0.pulse_width_percent( self._A0_percent )
		else:
			raise UniPiError( 'Board type %s not implemented' % self.board )

	@property
	def analog_out( self ):
		""" Analog output between 0 and 100 percent """
		return self._A0_percent

	@analog_out.setter
	def analog_out( self, value ):
		""" set value betwee, 0 and 100 percent """
		value = int( value ) # ensure it is an INT
		if value <= 0:
			value = 0
		if value >= 100:
			value = 100
		self._A0_percent = value
		# print( "set A0 PC to %s" % self._A0_percent )
		self._ch_A0.pulse_width_percent( self._A0_percent )

class UExtFacade:
	def __init__( self, owner ):
		self.owner = owner

	def i2c( self, **kwargs ):
		# I2C(1) for PYBStick & Pyboard
		return I2C(1, **kwargs)

	def spi( self, **kwargs ):
		# SPI(1) for PYBStick & Pyboard
		return SPI(1, **kwargs )

	def uart( self, baudrate, **kwargs ):
		# UART(6) for PYBStick & Pyboard
		return UART( 6, baudrate, **kwargs )

class UniPiEeprom( Eeprom_24C02C ):
	""" Access the EEPROM on UniPi board """

	def dump( self ):
		""" Dump UniPi EEPROM content to repl """
		for index in range( self.capacity//8 ):
			base_addr = index * 8
			data = [ self.read(base_addr+offset)[0] for offset in range(8) ]
			hex_repr = [ '{:02X}'.format(value) for value in data ]
			str_repr = [ chr(value) if 32 <=value<=126 else '.' for value in data ]
			print( "%4s : %s : %s" % ( hex(base_addr), ' '.join(hex_repr),''.join(str_repr) ) )

	def check_unipi( self ):
		""" Check the UniPi magic Key in the EEPROM """
		return self.check_magic( 0xE0, [0xFA,0x55] )

	@property
	def board_version( self ):
		""" Read UniPi Version """
		return '%s.%s' % ( self.read(0xe2)[0],self.read(0xe3)[0] )

	@property
	def analog_input_coefs( self ):
		""" Read the Analog Input Scales stored in the EEPROM. Should be close from 5.54 """
		ai1 = struct.unpack( '>f', self.read(0xF0,4) )[0]
		ai2 = struct.unpack( '>f', self.read(0xF4,4) )[0]
		return (ai1,ai2)


class AdcFacade:
	""" Access to two ADC inputs (0..10V) """
	def __init__( self, instances ):
		self._channels = instances # Must be list of MCP342x

	def __getitem__( self, key ):
		""" Voltage for ADC inputs 1 or 2 (0 to 10V) """
		assert key in (1,2), "Invalid ADC Channel number %s" % key
		return self._channels[key-1].convert_and_read() # returns voltage of the channels

class RelayFacade:
	""" Access relay by their number 1..8 """
	def __init__( self, instance ):
		self._relay = instance

	def __getitem__( self, key ):
		""" Last know state of relay (as stored by the object)"""
		return self._relay.input_pins( [key-1], read=False ) # reused stored value

	def __setitem__( self, key, value ):
		""" Last know state of relay (as stored by the object)"""
		return self._relay.output( key-1, value ) # change the relay


class InputFacade:
	""" Access relay by their number 1..8 """
	def __init__( self, instance ):
		self._input = instance
		# list of (input_nr, gp_nr)
		self._list = [ (input_nr, input_to_gp(input_nr)) for input_nr in range(1,15) ]

	def read( self ):
		""" read all the GPIOs input states from MCP230017 """
		self._input.read_gpio()

	def __getitem__( self, key ):
		""" Last know state of input stored in the object """
		index = input_to_gp( key )
		# Input are low when activated --> Invert the logic
		return not( self._input.input_pins( [index], read=False )[0]  )# reused stored value

	def read_all( self, read=False ):
		""" returns a dictionnary with all entries """
		values = self._input.input_pins( [ item[1] for item in self._list ], read=read ) # reuse stored value
		r = {}
		for i in range(len(self._list)):
			r[self._list[i][0]] = not(values[i])
		return r

# Detect board type
board_type = None
try:
	Pin(S12)
	board_type = BOARD_PYBSTICK
	print('PYBSTICK detected')
except:
	pass

if not(board_type):
	try:
		Pin('X4')
		board_type = BOARD_PYBOARD
		print('PYBOARD detected')
	except:
		pass


# Must have a board type
if not(board_type):
	raise UniPiError( 'Unknown MicroPython board type!' )

# I2C bus for PYBStick (S11=sda, S13=scl)
# I2C bus for Pyboard  (Y10=sda, Y9=scl)
i2c = I2C( 2 )

# Instanciate the UniPi
unipi = UniPi( i2c, board_type )
