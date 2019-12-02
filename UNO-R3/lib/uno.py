"""
uno.py - Arduino Pin mapping for Pyboard (based on Pyboard-UNO-R3 board).

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

from machine import SPI, I2C, Pin, UART
from pyb import Timer, udelay, ADC

# -- UNO -> Pyboard Pin conversion ----------
PIN_0 = "Y2"
PIN_1 = "Y1"
PIN_2 = "X7"
PIN_3 = "X1"
PIN_4 = "X2"
PIN_5 = "X3"
PIN_6 = "X4"
PIN_7 = "Y5"
PIN_8 = "X9"
PIN_9 = "X10"
PIN_10 = "X8"
PIN_11 = "Y8"
PIN_12 = "Y7"
PIN_13 = "Y6"
PIN_SCL = "Y9"
PIN_SDA = "Y10"

PIN_A0 = "X19"
PIN_A1 = "X20"
PIN_A2 = "X21"
PIN_A3 = "X22"
PIN_A4 = "X5"
PIN_A5 = "X6"

SERVO1 = "X1"
SERVO2 = "X2"
SERVO3 = "X3"
SERVO4 = "X4"

def map(x, in_min, in_max, out_min, out_max):
	""" Equivalent of Arduino map() function """
	return int( (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min )

# -- Analog Read --------------
# Make an analog read like Arduino UNO (on 10 bits)
def analog_read( pin ):
	""" Make a 10 bits reading (like Arduino UNO) on a Analog Pin """
	assert type( pin ) is ADC, "pin must be a pyb.ADC object"
	# read with 12bit & convert to 10 bits
	return map( pin.read(), 0, 4095, 0, 1024 )

# -- BUS tooling --------------
def spi_bus( **kwargs ):
	""" Returns the SPI bus and control Pin for Arduino pins 10,11,12,13.

	spi, ss = spi_bus( baudrate=20000 ) """
	_spi = SPI(2, **kwargs )
	_pin = Pin("X8", Pin.OUT, value=1)
	return _spi,_pin

def i2c_bus( **kwargs ):
	""" Returns the I2C bus placed over the Arduino pin 13.

	    i2c = i2c_bus( freq=20000 ) """
	return I2C(2, **kwargs )

def i2c_analog_bus( **kwargs ):
	""" Returns an I2C bus placed on the Arduino Pin A4, A5.

	 	i2c = i2c_analog_bus( freq=10000 ) """
	# Create a bitbanging bus for Arduino A4, A5
	return I2C( sda=Pin("X5"), scl=Pin("X6"), **kwargs )

def uart_bus( **kwargs ):
	""" Returns the UART initialized on Arduino pin 0 & 1.

	serial = uart_bus( baudrate=9600 ) """
	return UART(6, **kwargs )

# -- NeoPixel helper ----------
__pixels = None
def pixels( led_count=1, intensity=1 ):
	""" Create a WS2812/NeoPixel object for one or more LEDs """
	global __pixels
	if __pixels:
		return __pixels
	from ws2812 import NeoPixel
	__pixels = NeoPixel( spi_bus=1, led_count=led_count, intensity=intensity )
	return __pixels

# -- Buzzer -------------------
# Notes/tone with corresponding frequence
NOTES = { ' ' : 0,   # Silent
		  'c' : 261, # Do
		  'd' : 294, # Ré
		  'e' : 329, # Mi
		  'f' : 349, # Fa
		  'g' : 392, # Sol
		  'a' : 440, # La
		  'b' : 493, # Si
		  'C' : 523  # Do
		}
# Buzzer use a cConfigurer les broches PWM pour la sortie sur buzzer
__bz_pin = None
__bz_tim = None
__bz_ch  = None
class Buzzer(object):
	def __init__(self):
		global __bz_pin, __bz_tim, __bz_ch
		if not(__bz_pin):
			# Initialize timer and channels if not yet done
			__bz_pin = Pin("Y11") # Broche Y2 avec timer 8 et Channel 2
			__bz_tim = Timer(8, freq=3000)
			__bz_ch  = __bz_tim.channel(2, Timer.PWM_INVERTED, pin=__bz_pin)

	def tone( self, freq=0 ):
		""" Play a tone at a given frequency. Frequency = 0 for silent """
		global __bz_tim, __bz_ch
		if freq == 0:
			__bz_ch.pulse_width_percent( 0 )
		else:
			__bz_tim.freq( freq )
			__bz_ch.pulse_width_percent( 30 )

	def note( self, note, duration ):
		""" Play a note abcdef... for a given period of time. note comes from NOTES dictionnary. duration is multiple of 1000 microSecond """
		# Note to freq
		freq = NOTES[ note ]
		self.tone( freq )
		# duration in microsecond (1=1000micros, 2=2000micros, etc)
		udelay( duration * 1000 ) # temps en micro-second

	def tune( self, tune_string, tempo ):
		""" play a melody encoded within a string at a given tempo (ex: 300)"""
		tune_list = tune_string.split( ',' )
		duration = 1
		for tune_item in tune_list:
			# print( tune_item )
			if len( tune_item )>1:
				try:
					duration = int( tune_item[1:] )
				except:
					raise ValueError( 'Invalid duration %s for note %s' % (tune_item[1:], tune_item[0]) )
			else:
				duration = 1

			# Jouer la note
			self.note( tune_item[0], tempo * duration )
			# Pause entre 2 notes
			self.tone()
			udelay( (tempo * 1000) // 2 )
