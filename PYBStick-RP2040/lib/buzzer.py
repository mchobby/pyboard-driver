"""
Buzzer.py - easy tune library for PYBStick-RP2040.

* Author(s): Meurisse D. from MCHobby (shop.mchobby.be).

See project source @ https://github.com/mchobby/pyboard-driver/tree/master/PYBStick-RP2040

See example test_buzzer.py in the project source

"""
#
# The MIT License (MIT)
#
# Copyright (c) 2021 Meurisse D. for MC Hobby
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

from machine import Pin, PWM
from time import sleep_us

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
__bz_pwm = None

class Buzzer():
	def __init__(self):
		global __bz_pin, __bz_pwm
		if not(__bz_pin):
			# Initialize timer and PWM
			__bz_pin = Pin(7) # Broche IO7
			__bz_pwm = PWM(__bz_pin)
			__bz_pwm.freq( 3000 )

	def tone( self, freq=0 ):
		""" Play a tone at a given frequency. Frequency = 0 for silent """
		global __bz_pwm
		if freq == 0:
			__bz_pwm.duty_u16( 0 )
		else:
			__bz_pwm.freq( freq )
			__bz_pwm.duty_u16( 19660 ) # 30%

	def note( self, note, duration ):
		""" Play a note abcdef... for a given period of time. note comes from NOTES dictionnary. duration is multiple of 1000 microSecond """
		# Note to freq
		freq = NOTES[ note ]
		self.tone( freq )
		# duration in microsecond (1=1000micros, 2=2000micros, etc)
		sleep_us( duration * 1000 ) # temps en micro-second

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
			sleep_us( (tempo * 1000) // 2 )
