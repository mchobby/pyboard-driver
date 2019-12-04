"""
pwm.py - easy PWM library for Pyboard Original.

* Author(s): Meurisse D. from MCHobby (shop.mchobby.be).

See project source @ https://github.com/mchobby/pyboard-driver/tree/master/UNO-R3
See example test_pwm.py in the project source

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

from machine import Pin
from pyb import Timer

PWM_DEFS = {"Y9"  : (2 ,3,Timer.PWM), # Pin, (timer,channel,PwmMode)
			"Y10" : (2 ,4,Timer.PWM),
			"Y6"  : (1 ,1,Timer.PWM_INVERTED),
			"Y7"  : (1 ,2,Timer.PWM_INVERTED),
			"Y8"  : (1 ,3,Timer.PWM_INVERTED),
			"X8"  : (14,1,Timer.PWM),
			"X10" : (4 ,2,Timer.PWM),
			"X9"  : (4 ,1,Timer.PWM),
			"X4"  : (5 ,4,Timer.PWM),
			"X3"  : (5 ,3,Timer.PWM),
			"X2"  : (2 ,2,Timer.PWM),
			"X1"  : (5 ,1,Timer.PWM),
			"X7"  : (13,1,Timer.PWM),
			"Y1"  : (8 ,1,Timer.PWM),
			"Y2"  : (8 ,2,Timer.PWM),
			"X6"  : (8, 1,Timer.PWM_INVERTED) # May be in conflict with Y1 when both are used at the same time
			}

class PwmException( Exception ):
	pass

class PwmPin( object ):
	""" Information about the created PWM Pin """
	# pin    : Ref to pin,
	# timer  : Ref to created timer,
	# channel: Ref to channel
	__slot__ = ["pin", "timer", "channel", "_percent" ]

	def __init__( self, pin, timer, channel ):
		""" Initialize for the PWM for the initialized objects """
		self.pin = pin
		self.timer = timer
		self.channel = channel
		self._percent = None

	def release( self ):
		""" Deinit the PWM pin """
		# Reinitialize it as High Impedance input
		self.pin.init( mode=Pin.IN )

	@property
	def percent( self ):
		""" PWM the duty_cycle in percent if available """
		return self._percent

	@percent.setter
	def percent( self, value ):
		assert 0 <= value <= 100, "Invalid %s PWM percent value" % value
		self._percent = value
		self.channel.pulse_width_percent( value )

	def write( self, value ):
		""" set the duty cycle based on a 8 bits value from 0 to 255 (like Arduino)."""
		assert 0 <= value <= 255, "Invalid %s value for 8 bits" % value
		if value==0:
			self.percent = 0
		elif value==255:
			self.percent = 100
		else:
			self.percent = int(value/255*100)

class PwmFactory( object ):
	""" Factory that allows to control the PwmPin """
	def __init__( self, freq=500 ):
		self.freq = 500 # Base frequence for the PWM. 500 Hz like Arduino
		self.timers = {} # Dictionnary with created timer
		self.pins = {} # list of existing pin_name having PwmPin objects

	def pwm( self, pin_name, duty_percent=0 ):
		""" Create or retreive a PwmPin object based on its pin_name. duty_percent can be used for initial duty_cycle initialization  """
		if pin_name in self.pins:
			# released pin ?
			if self.pins[pin_name].pin.mode() == Pin.IN:
				del( self.pins[pin_name] ) # So pin will be recreated
			else:
				return self.pins[pin_name]

		# Create the needed ressources and associated PwmPin
		if not(pin_name in PWM_DEFS):
			raise PwmException( "Pin %s not supported by pwm library" % pin_name )
		pwm_def = PWM_DEFS[ pin_name ]

		# create the pin
		_pin = Pin( pin_name )
		# retreive initialized timer
		if not( pwm_def[0] in self.timers ):
			self.timers[pwm_def[0]] = Timer( pwm_def[0], freq=self.freq )
		_timer = self.timers[pwm_def[0]]
		# each of the PinPwm instance (PWM output) uses its own channel, so no need to check for existence
		_channel = _timer.channel( pwm_def[1], pwm_def[2], pin=_pin ) # Timer, channel, pin
		_channel.pulse_width_percent( duty_percent )
		# register the PwmPin
		self.pins[pin_name]=PwmPin( _pin, _timer, _channel)
		return self.pins[pin_name]

pwm_factory = None
def pwm( pin_name, **kwargs ):
	global pwm_factory
	# Auto create the factory at first use (if not yet created). use default settings
	if not pwm_factory:
		pwm_factory = PwmFactory()
	return pwm_factory.pwm( pin_name, **kwargs )
