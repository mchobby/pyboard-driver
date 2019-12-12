"""
unoextra.py - Pyboard-UNO-R3 extra miscellaneous features like OLED and charger.

* Author(s): Meurisse D. from MCHobby (shop.mchobby.be).

See project source @ https://github.com/mchobby/pyboard-driver/tree/master/UNO-R3

"""
#
# The MIT License (MIT)
#
# Copyright (c) 2019 Meurisse D. for MC Hobby
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

__version__ = "0.0.1"

from machine import I2C, Pin
from ssd1306 import SSD1306_I2C
from math import ceil

__i2c = None
def get_i2c():
	""" Retreive reference to the software I2C bus for extra features (OLED,Charger,...)"""
	global __i2c
	if not(__i2c):
		__i2c = I2C( sda=Pin("Y4"), scl=Pin("Y3") )
	return __i2c

# --- OLED ---------------------------------------------------------------------
LINE_HEIGHT = 10 # Height of a character line (in pixels)

class Point():
	__slot__ = ['x','y']

	def set(self, xy ):
		self.x = xy[0]
		self.y = xy[1]

	def get( self ):
		return self.x, self.y

	def __repr__(self):
		return "<%s %i,%i>" % (self.__class__.__name__, self.x, self.y )

class Unoled( SSD1306_I2C ):
	""" Inherit of FrameBuffer drawing functions. see following link for examples:
		https://wiki.mchobby.be/index.php?title=FEATHER-MICROPYTHON-OLED#Tester_la_biblioth.C3.A8que

		font-size is 8x8
	"""
	def __init__(self):
		super().__init__( 128,64,get_i2c() )
		self.__cursor = Point()
		self.clear()

	def clear(self, show=True):
		self.fill(0)
		if show:
			self.show()
		self.__cursor.set( (0,0) ) # Inner text position (top,left - in pixel)

	def cursor( self ):
		""" Return the (line,col) position (0 based) of the cursor in characters """
		x,y = self.__cursor.get()
		return y//LINE_HEIGHT, x//8 # Line, Column

	def set_cursor( self, line_col ):
		""" set the cursor position with (line, col) tuple. 0 based value """
		self.__cursor.x = line_col[1]*8
		self.__cursor.y = line_col[0]*LINE_HEIGHT

	def println( self, text, wrap=False, show=True ):
		""" Print a line and scroll the screen if necessary (before drawing the text)"""
		if wrap:
			if self.__cursor.x != 0:
				raise Exception('Cursor must be at column 0')
			_chars_per_line = self.width//8
			for i in range( ceil(len(text)/_chars_per_line) ):
				self.println( text[i*_chars_per_line:(i+1)*_chars_per_line]  )
			return # not going further

		# Do we have to vertical scroll before we display text?
		if self.__cursor.y + LINE_HEIGHT > self.height:
			self.scroll(0, -1*LINE_HEIGHT) # Scroll content UP
			self.fill_rect(0,self.__cursor.y-1*LINE_HEIGHT,self.width, self.height-(self.__cursor.y-1*LINE_HEIGHT),0) # Clean up before drawing next text
			self.__cursor.y -= LINE_HEIGHT
		# clear the zone under drawing text
		self.fill_rect( self.__cursor.x,self.__cursor.y, len(text)*8, LINE_HEIGHT, 0 )
		self.text(text, self.__cursor.x,self.__cursor.y, 1)
		self.__cursor.y += LINE_HEIGHT
		self.__cursor.x = 0
		if show:
			self.show()

	def print( self, text,  show=True ):
		""" Just print on the same line """
		self.fill_rect( self.__cursor.x,self.__cursor.y, len(text)*8, LINE_HEIGHT, 0 )
		self.text( text, self.__cursor.x,self.__cursor.y, 1 )
		self.__cursor.x += len(text)*8
		if show:
			self.show()

# --- CHARGER ------------------------------------------------------------------
REG_CONF  = 0x02
REG_STAT  = 0x0B
REG_FAULT = 0x0C
REG_BATV  = 0x0E
REG_SYSV  = 0x0F
REG_VBUSV = 0x11

# For REG_STAT
USB100 = 0 # USB100 input is detected
USB500 = 1 # USB500 input is detected
# For REG_STAT
CHARGING_NOT_CHARGING = 0b00
CHARGING_PRE_CHARGE   = 0b01 # < V BATLOWV
CHARGING_FAST_CHARGE  = 0b10 # Fast Charging
CHARGING_DONE         = 0b11 # Charge Termination Done
# For REG_STAT
VBUS_NO_INPUT = 0b000
VBUS_USB_SDP  = 0b001 # USB Host SDP
VBUS_USB_CDP  = 0b010 # USB CDP (1.5A)
VBUS_USB_DCP  = 0b011 # USB DCP (3.25A)
VBUS_USB_DCP_MAX = 0b100 # Adjustable High Voltage DCP (MaxCharge) (1.5A)
VBUS_USB_UNKNOW  = 0b101 # Unknown Adapter (500mA)
VBUS_NOT_STD     = 0b110 # Non-Standard Adapter (1A/2A/2.1A/2.4A)
VBUS_OTG         = 0b111 # USB OTG

# For REG_FAULT
CHARGING_FAULT_NORMAL = 0b00
CHARGING_FAULT_INPUT  = 0b01 # Input fault. VBUS > V ACOV or VBAT < VBUS < V VBUSMIN (typical 3.8V)
CHARGING_FAULT_THERMAL= 0b10 # Thermal shutdown
CHARGING_FAULT_TIMER  = 0b11 # Charge Safety Timer Expiration
# For REG_FAULT
NTC_FAULT_NORMAL      = 0b000
NTC_FAULT_BUCK_COLD   = 0b001 # TS Cold in Buck mode
NTC_FAULT_BUCK_HOT    = 0b010 # TS Hot in Buck mode
NTC_FAULT_BOOST_COLD  = 0b101 # TS Cold in Boost mode
NTC_FAULT_BOOST_HOT   = 0b110 # TS Hot in Boost mode

# Bits to voltage conversion
BTV_VSYS = ( 2.304, # Base value
 			[0.02, 0.04, 0.08, 0.160, 0.320, 0.640, 1.280 ] ) # Bits 0 to 6 weight
BTV_VBUSV= ( 2.6,
			 [0.1,0.2,0.4,0.8,1.6,3.2,6.4])

class QB25895(object):
	""" Driver for the BQ25895 from Texas Instrument
		I2C Controlled Single Cell 5-A Fast Charger with MaxCharge TM for High Input Voltage and Adjustable Voltage 3.1-A Boost Operation """
	def __init__( self, i2c ):
		self._i2c = i2c
		self._address = 0x6A

		# see update_status()
		self.vsys_stat = None # VSYS Regulation Status. False:BAT > VSYSMIN, True:BAT < VSYSMIN
		self.sdp_stat  = None # USB Input Status
		self.pg_stat   = None # Power Good
		self.chrg_stat = None # Charging stat
		self.vbus_stat = None # VBUS Status Register

		# see update_fault()
		self._watchdog_fault = None
		self._boost_fault    = None
		self._chrg_fault     = None
		self._bat_fault      = None
		self._ntc_fault      = None

	def _read_u8(self, address):
		# Read an 8-bit unsigned value from the specified 8-bit address.
		# Make sure to add command bit to read request.
		return self._i2c.readfrom_mem( self._address, address, 1 )[0] # read one byte

	def _write_u8(self, address, value):
		# write an 8-bit unsigned value to the specified 8-bit address.
		# Make sure to add command bit to read request.
		return self._i2c.writeto_mem( self._address, address, value ) # write one byte

	def bits_to_volts( self, value, btv ):
		# The BQxxx use a baseline voltage + volt_weight to add for each bit positionned to 1
		# btv is a BTV_xxx constant with base value + list of bit weight
		result = btv[0] # Base voltage
		for i in range(1,7): #from 1 to 6
			if (value & (1<<i))>0 :
				result = result + btv[1][i]
		return result

	def config( self, **kwargs ):
		""" Set one or several configuration bits. See REG02  """
		val = self._read_u8( REG_CONF )
		# Set the CONV_RATE Bit
		if 'conv_rate' in  kwargs:
			if kwargs['conv_rate']:
				val = val | (1<<6)
			else:
				val = val & 0b10111111

		data = bytes( [val] )
		self._write_u8( REG_CONF, data )

	def update_status( self ):
		""" Read and update the various charging STATus """
		val = self._read_u8(REG_STAT)
		self.vsys_stat = (val & 0b1) == 1
		self.sdp_stat  = USB500 if ((val & 0b10)>>1) else USB100
		self.pg_stat   = (val & 0b100) > 1
		self.chrg_stat = (val & 0b11000) >> 3
		self.vbus_stat = (val & 0b11100000) >> 5

	def update_fault( self ):
		""" Read and update the various Fault flags """
		val = self._read_u8(REG_FAULT)
		self._watchdog_fault  = (val & 0b10000000) > 0
		self._boost_fault     = (val & 0b01000000) > 0
		self._chrg_fault      = (val & 0b110000)>>4
		self._bat_fault       = (val & 0b1000)>0
		self._ntc_fault       = (val & 0b111)

	@property
	def vsys_regulation( self ):
		""" STATUS: VSYS Regulation Status.
			False:BAT > VSYSMIN, True:BAT < VSYSMIN """
		return self.vsys_stat

	@property
	def usb_input_status( self ):
		"""  STATUS: returns USB100 or USB500 depending on the detected input """
		return self.sdp_stat

	@property
	def power_good( self ):
		""" STATUS: returns the Power Good status as boolean """
		return self.pg_stat

	@property
	def charging_status(self):
		""" STATUS: returns a CHARGING_xxx constant """
		return self.chrg_stat

	@property
	def vbus_status( self ):
		""" STATUS: Returns a VBUS_xxx constant """
		return self.vbus_stat

	@property
	def watchdog_fault( self ):
		""" FAULT: Watchdog timer expiration (boolean) """
		return self._watchdog_fault

	@property
	def boost_fault( self ):
		""" FAULT: Boost mode Fault. VBUS overloaded in OTG, or VBUS OVP,
				or battery is too low in boost mode """
		return self._boost_fault

	@property
	def charging_fault( self ):
		""" FAULT: see the CHARGING_FAULT_xxx constants """
		return self._chrg_fault

	@property
	def battery_fault( self ):
		""" FAULT: True when BATOVP=Battery Over Voltage Protection (VBAT > V BATOVP )"""
		return self._bat_fault

	@property
	def ntc_fault( self ):
		""" FAULT: status of the NTC température sensor. See NTC_FAULT_xxx constants """
		return self._ntc_fault

	@property
	def vbat( self ):
		""" Battery voltage in volts """
		val = self._read_u8(REG_BATV)
		# Thermal Status = val & 0b10000000
		# BatV = val & 0b01111111
		return self.bits_to_volts( val & 0b01111111, BTV_VSYS )

	@property
	def vsys( self ):
		""" SYS voltage in volts """
		val = self._read_u8(REG_SYSV)
		# first bit is reserved
		# BatV = val & 0b01111111
		return self.bits_to_volts( val & 0b01111111, BTV_VSYS )

	@property
	def vbus( self ):
		""" BUS (USB VBUS) Voltage """
		val = self._read_u8(REG_VBUSV)
		# VBUS Good Status = val & 0b10000000
		return self.bits_to_volts( val & 0b01111111, BTV_VBUSV )

class Charger( QB25895 ):
	""" Interface class for the PYBOARD-UNO-R3 board (based on QB25895 driver) """
	def __init__(self):
		super().__init__( get_i2c() )
		self.update_status()  # Update the STATUS properties
		self.update_fault() # Update the FAULT properties
