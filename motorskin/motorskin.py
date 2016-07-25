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
from hbridge import DualHBridge
from ultrasonic import Ultrasonic

class MotorSkin( DualHBridge ):
    """ Specifics for 2 bidirectional motor driving (with speed control via PWM) """

    MOT1_PINS = ( pyb.Pin.board.X6, pyb.Pin.board.X5 )
    MOT1_PWM = {'pin' : pyb.Pin.board.X3, 'timer' : 5, 'channel' : 3 }   

    MOT2_PINS = ( pyb.Pin.board.X7, pyb.Pin.board.X8 )
    MOT2_PWM = {'pin' : pyb.Pin.board.X4, 'timer' : 5, 'channel' : 4 }  

    (TRIGGER_PIN,ECHO_PIN) = (pyb.Pin.board.Y5, pyb.Pin.board.Y6)

    ultrason = None
    _switches = []
    
    def __init__( self, reverse_mot1 = False, reverse_mot2 = False, fix_rotate = False, derivative_fix = 0 ):
        """ Initialize the DualHBridge L293D. Allows you to reverse/tune the 
            spinning commands for the motors when the underlaying plateform does not 
            move proprely when calling forward() or backward()

          :param reverse_mot1: switch the forward/backward commands for motor 1
          :param reverse_mot2: switch the forward/backward commands for motor 2
          :param fix_rotate: set this True when the robot turn left instead of turning right as requested
          :param derivative_fix: use +3 to speedup right motor when forward() does bend the path to the right. 
                                 use -3 to slow down the right motor when forward() bend the path to the left."""
        mot1 = ( self.MOT1_PINS[1], self.MOT1_PINS[0] ) if reverse_mot1 else self.MOT1_PINS
        mot2 = ( self.MOT2_PINS[1], self.MOT2_PINS[0] )  if reverse_mot2 else self.MOT2_PINS
        if not fix_rotate:
            DualHBridge.__init__( self, mot1, self.MOT1_PWM, mot2, self.MOT2_PWM, derivative_fix )
        else:
            # Robot is apparently rotating the wrong way... this is because
            # motor1 has been wired in place of the motor 2.
            DualHBridge.__init__( self, mot2, self.MOT2_PWM, mot1, self.MOT1_PWM, derivative_fix )

        self.ultrason = Ultrasonic( self.TRIGGER_PIN, self.ECHO_PIN )

        for pin in ('X18','X19','X20','X21'):
            self._switches.append( pyb.Pin( pin, pyb.Pin.IN, pull=pyb.Pin.PULL_UP) )


    def distance( self ):
      """ Read distance in cm from Ultrasonic sensor """
      return self.ultrason.distance_in_cm()

    def button_pin( self, button_nr ):
      """ Return Pin for a user button 1 to 4 (SW1..SW4) """
      return self._switches[ button_nr-1 ]

    def button_pressed( self, button_nr ):
      """ Check if a user button is pressed """
      return self._switches[ button_nr-1 ].value() == 0