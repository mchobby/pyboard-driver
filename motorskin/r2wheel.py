##
# Commande d'une plateforme robotique 2 roues avec un Motor-Skin, Senseur ultrason HC-SR04 et MicroPython PyBoard
# Control a 2 wheel robotic plateform with a Motor-Skin, Ultrasonic Sensor and MicroPython PyBoard
#
#   http://shop.mchobby.be/product.php?id_product=918
#   http://shop.mchobby.be/product.php?id_product=561
#   http://shop.mchobby.be/product.php?id_product=570
# 
# Voir Tutoriel - See our french tutorial
#   TODO - coming soon
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
from motorskin import MotorSkin

class Robot2Wheel( MotorSkin ):
    """ Specifics for 2 Wheel Robot. """

    (RIGHT_ROTATE, LEFT_ROTATE, RIGHT_BEND, LEFT_BEND ) = ('RP','LP','RB','LB')
    DIRECTIONS =  (RIGHT_ROTATE, LEFT_ROTATE, RIGHT_BEND, LEFT_BEND ) 

    (HALTED,MOVE_FORWARD,MOVE_BACKWARD) = ('H', 'MF', 'MB') 
    STATES = (HALTED,MOVE_FORWARD,MOVE_BACKWARD) + DIRECTIONS

    _state = None # Current state of the robot.
    
    def __init__( self, reverse_mot1 = False, reverse_mot2 = False, fix_rotate = True, derivative_fix = 0 ):
        """ Initialize the MotorSkin for a 2 Motor robot. Allows you to reverse the 
            spinning commands for the motors when the robot does not 
            move proprely when calling forward() or backward()

          :param reverse_mot1: switch the forward/backward commands for motor 1
          :param reverse_mot2: switch the forward/backward commands for motor 2
          :param fix_rotate: set this True when the robot turn left instead of turning right as requested
          :param derivative_fix: use +3 to speedup right motor when forward() does bend the path to the right. 
                                 use -3 to slow down the right motor when forward() bend the path to the left."""
        mot1 = ( MotorSkin.MOT1_PINS[1], MotorSkin.MOT1_PINS[0] ) if reverse_mot1 else MotorSkin.MOT1_PINS
        mot2 = ( MotorSkin.MOT2_PINS[1], MotorSkin.MOT2_PINS[0] ) if reverse_mot2 else MotorSkin.MOT2_PINS
        if not(fix_rotate):
            super( MotorSkin, self ).__init__( mot1, MotorSkin.MOT1_PWM, mot2, MotorSkin.MOT2_PWM, derivative_fix )
        else:
            # Robot is apparently rotating the wrong way... this is because
            # motor1 has been wired in place of the motor 2.
            super( MotorSkin, self ).__init__( mot2, MotorSkin.MOT2_PWM, mot1, MotorSkin.MOT1_PWM, derivative_fix )
        self._state = Robot2Wheel.HALTED
	
    @property 
    def state( self ):
        return self._state

    def turn( self, direction, speed=100 ):
        if not( direction in self.DIRECTIONS ):
            raise ValueError( 'invalid direction' )
        if direction == self.RIGHT_ROTATE:
            self.motor1.forward( speed )
            self.motor2.backward( speed )
        elif direction == self.LEFT_ROTATE: 
            self.motor1.backward( speed )
            self.motor2.forward( speed )
        elif direction == self.RIGHT_BEND:
            self.motor1.forward( 100 )
            self.motor2.forward( 100-speed ) 
        elif direction == self.LEFT_BEND:
            self.motor1.forward( 100-speed )
            self.motor2.forward( 100 )
        self._state = direction

    def right( self, speed=100 ):
        self.turn( Robot2Wheel.RIGHT_ROTATE, speed )

    def left( self, speed=100 ):
        self.turn( Robot2Wheel.LEFT_ROTATE, speed )

    def halt( self ):
        super( Robot2Wheel, self ).halt()
        self._state = Robot2Wheel.HALTED

    def forward( self, speed = 100, speed_2 = None ):
        super( Robot2Wheel, self ).forward( speed, speed_2 )
        self._state = Robot2Wheel.MOVE_FORWARD

    def backward( self, speed = 100, speed_2 = None ):
        super( Robot2Wheel, self ).backward( speed, speed_2 )
        self._state = Robot2Wheel.MOVE_BACKWARD
