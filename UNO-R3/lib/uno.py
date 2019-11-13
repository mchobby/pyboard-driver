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

from machine import SPI, I2C, Pin, UART

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
	""" Returns an I2C bus placed on the Aruino Pin A4, A5.

	 	i2c = i2c_analog_bus( freq=10000 ) """
	# Create a bitbanging bus for Arduino A4, A5
	return I2C( sda=Pin("X5"), scl=Pin("X6"), **kwargs )

def uart_bus( **kwargs ):
	""" Returns the UART initialized on Arduino pin 0 & 1.

	serial = uart_bus( baudrate=9600 ) """
	return UART(6, **kwargs )
