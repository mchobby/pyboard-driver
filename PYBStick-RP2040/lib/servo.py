"""
servo.py - easy SERVO motor library for PYBStick-RP2040 (and Raspberry-Pi Pico).

* Author(s): Meurisse D. from MCHobby (shop.mchobby.be).

See project source @ https://github.com/mchobby/pyboard-driver/tree/master/PYBStick-RP2040

"""
from machine import PWM, Pin

class Servo():
	""" Servo class for 0-180 degree Hobby Servo """
	def __init__( self, pin_id ):
		self._pin = Pin(pin_id)
		self._pwm = PWM( self._pin )
		self._pwm.freq( 50 )
		self._pwm.duty_u16( 0 ) # Disabling
		# default calibration
		self.calibration( 1.0, 2.0, 1.5, 0, 180 )

	def calibration( self, pulse_min=1.0, pulse_max=2.0, pulse_center=1.5, degree_min=0, degree_max=180 ):
		self.deg_min=degree_min
		self.deg_max=degree_max
		self.deg_center = ( degree_min + degree_max) // 2

		self.pulse_min=pulse_min # ms
		self.pulse_max=pulse_max
		self.pulse_center=pulse_center

	def angle( self, value ):
		assert self.deg_min <= value <= self.deg_max, "Not in supported degree range"

		if value <= self.deg_center:
			_pulse_ms = self.pulse_min + (self.pulse_center-self.pulse_min) * (value / (self.deg_center-self.deg_min))
		else:
			_pulse_ms = self.pulse_center + (self.pulse_max-self.pulse_center) * ((value-self.deg_center) / (self.deg_max-self.deg_center))

		#print( int(_pulse_ms*1000000) )
		self._pwm.duty_ns( int(_pulse_ms*1000000) ) # 1 ms = 1E6 ns

	def speed( self, value ):
		""" set motor speed between -100..+100 """
		assert -100 <= value <= 100, "Not in range -100..+100"

		if value==0:
			_pluse_ms = self.pulse_center
		if value<0:
			_pulse_ms = self.pulse_min + (self.pulse_center-self.pulse_min) * ((100+value) / 100)
		else:
			_pulse_ms = self.pulse_center + (self.pulse_max-self.pulse_center) * (value / 100)

		self._pwm.duty_ns( int(_pulse_ms*1000000) ) # 1 ms = 1E6 ns


	def detach( self ):
		self._pwm.duty_u16( 0 )
