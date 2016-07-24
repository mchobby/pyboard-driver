##
# Commande d'un pont-H L293D à l'aide de MicroPython PyBoard
# Control a L293D H Bridge with MicroPython PyBoard
#
#   http://shop.mchobby.be/product.php?id_product=155
#   http://shop.mchobby.be/product.php?id_product=570
# 
# Voir Tutoriel - See our french tutorial
#   http://wiki.mchobby.be/index.php?title=Hack-micropython-L293D
#
# Copyright 2016 - Dominique Meurisse for MC Hobby SPRL <info (at) mchobby (dot) be>
#
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##
import pyb
from pyb import Timer

class HBridge:
    """ Control à H-Bridge. Also support PWM to control the speed (between 0 to 100%) """
    PWM_FREQ = 100  # Frequency 100 Hz
    (UNDEFINED,HALT,FORWARD,BACKWARD) = (-1, 0,1,2)

    def __init__( self, input_pins, pwm = None ):
        """:param input_pins: tuple with input1 and input 2 pins
           :param pwm: dic with pin, timer and channel """
        self.speed = 0
        self.state = HBridge.UNDEFINED
        
        # Init HBridge control pins
        self.p_input1 = pyb.Pin( input_pins[0], pyb.Pin.OUT_PP )
        self.p_input2 = pyb.Pin( input_pins[1], pyb.Pin.OUT_PP )

        # Init PWM Control for speed control (without PWM, the L293D's
        #   Enable pin must be place to HIGH level)
        self.has_pwm = (pwm != None)
        if self.has_pwm: 
            self._timer = pyb.Timer( pwm['timer'], freq=self.PWM_FREQ )
            self._channel = self._timer.channel( pwm['channel'], Timer.PWM, pin=pwm['pin'], pulse_width_percent=100 )

        self.halt()

    def set_speed( self, speed ):
        if not(0 <= speed <= 100):
            raise ValueError( 'invalid speed' )
        # Use PWM speed ?
        if self.has_pwm:
            self._channel.pulse_width_percent( speed )
            self.speed = speed
        else:
            # Non PWM
            self.speed = 0 if speed == 0 else 100
            if self.speed == 0 and self.state != HBridge.HALT:
                self.halt() # force motor to stop by manipulating input1 & input2
                
    
    def halt( self ):
        self.p_input1.low()
        self.p_input2.low()
        self.state = HBridge.HALT # Do not invert ...
        self.set_speed( 0 )       #    thoses 2 lines

    def forward(self, speed = 100 ):
        # reconfigure HBridge
        if self.state != HBridge.FORWARD :
            self.halt()
            self.p_input1.low()
            self.p_input2.high()
            self.state = HBridge.FORWARD
        # Set speed
        self.set_speed( speed )
        
    def backward(self, speed = 100 ):
        # reconfigure HBridge
        if self.state != HBridge.BACKWARD:
            self.halt()
            self.p_input1.high()
            self.p_input2.low()
            self.state = HBridge.BACKWARD
        # Set speed 
        self.set_speed( speed )
        
class DualHBridge():
    """ Control 2 x H-Bridges on L293D to control the 2 motors of a 
        robotic plateforme """

    def __init__( self, mot1_pins, mot1_pwm, mot2_pins, mot2_pwm, derivative_fix=0 ):
        """:param mot1_pins: tuple with input1 and input 2 pins
           :param mot1_pwm: dic with pin, timer and channel. Use None for no PWM.
           :param mot2_pins: tuple with input3 and input 4 pins
           :param mot2_pwm: dic with pin, timer and channel. Use None for no PWM.
           :param derivative_fix: use +3 to speedup right motor when forward() does bend on the right. 
                                 use -3 to slow down the right motor when forward() bend on the left."""
        if (derivative_fix != 0) and ( (mot1_pwm == None) or (mot2_pwm == None) ):
            raise EValueError( 'derivative_fix needs PWM control to work' )
        self.motor1 = HBridge( mot1_pins, mot1_pwm )
        self.motor2 = HBridge( mot2_pins, mot2_pwm )
        self.derivative_fix = derivative_fix

    def forward( self, speed = 100, speed_2 = None ):
        if speed_2 == None: # not different speed for motor 2?
            speed_2 = speed 
        #adjust speed with derivative_fix
        if self.derivative_fix > 0:
            speed = speed - self.derivative_fix
            speed = 0 if speed < 0 else speed
        elif self.derivative_fix < 0:
            speed_2 = speed_2 - abs(self.derivative_fix)
            speed_2 = 0 if speed_2 < 0 else speed_2
        
        self.motor1.forward( speed )
        self.motor2.forward( speed_2 )
        

    def backward( self, speed = 100, speed_2 = None ):
        if speed_2 == None: # not different speed for motor 2?
            speed_2 = speed 
        #adjust speed with derivative_fix
        #adjust speed with derivative_fix
        if self.derivative_fix > 0:
            speed = speed - self.derivative_fix
            speed = 0 if speed < 0 else speed
        elif self.derivative_fix < 0:
            speed_2 = speed_2 - abs(self.derivative_fix)
            speed_2 = 0 if speed_2 < 0 else speed_2

        self.motor1.backward( speed )
        self.motor2.backward( speed_2 )

    def halt( self ):
        self.motor1.halt()
        self.motor2.halt()
