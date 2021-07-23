"""
zumoshield.py - Pololu's Zumo Robot Shield library for MicroPython Pyboard Original.

* Author(s):    Braccio M.  from MCHobby (shop.mchobby.be).
                Meurisse D. from MCHobby (shop.mchobby.be).

See project source @ https://github.com/mchobby/pyboard-driver/tree/master/zumo-robot

See example line_follower.py in the project source
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
__repo__ = "https://github.com/mchobby/pyboard-driver.git"

from pyb import Timer, Pin
from qtrsensors import QTRSensors
import time

ZUMO_SENSOR_ARRAY_DEFAULT_EMITTER_PIN = "X7"
PWM_L="X8"
PWM_R="X10"
DIR_L="X9"
DIR_R="Y5"
class ZumoMotor( object ):

    def __init__(self,use_20khz_pwm=False):
        self.dir_l=Pin(DIR_L,Pin.OUT)
        self.dir_r=Pin(DIR_R,Pin.OUT)
        self.pwm_l=Pin(PWM_L,Pin.OUT)
        self.pwm_r=Pin(PWM_R,Pin.OUT)

        self.tim_r=Timer(4,freq=1000 if not(use_20khz_pwm) else 20000)
        self.ch_r=self.tim_r.channel(2,Timer.PWM,pin=self.pwm_r)
        self.tim_l=Timer(14,freq=500 if not(use_20khz_pwm) else 20000)
        self.ch_l=self.tim_l.channel(1,Timer.PWM,pin=self.pwm_l)

        self.flipLeft = False
        self.flipRight = False

        initialized = True # This class is always initialised and doens't need to initialised before
                           # every change of speed

    def flipLeftMotor(self,flip):
        self.flipleft = flip # True/False

    def flipRightMotor(self,flip):
        self.flipRight = flip

    def setLeftSpeed(self,speed):
        reverse=False
        if (speed<0):                                   #if speed is negatif we make tha value positif again
            speed = -speed                              #but put the reverse value to 1 so we know we need to go backwars
            reverse = True
        if(speed > 400):                                #speed can be maximum 400
            speed = 400

        self.ch_l.pulse_width_percent(int(speed/4))     # value goes from 0-400 but in python we need % for PWM.
                                                        #We divide by 4 to have a value that goes from 0-100
        if (reverse ^ self.flipLeft):
            self.dir_l.value(1)
        else:
            self.dir_l.value(0)

    def setRightSpeed(self,speed):
        reverse=False
        if (speed<0):
            speed = -speed
            reverse = True
        if(speed > 400):
            speed = 400

        self.ch_r.pulse_width_percent(int(speed/4))
        if (reverse ^ self.flipRight):
            self.dir_r.value(1)
        else:
            self.dir_r.value(0)

    def setSpeeds(self,leftSpeed,rightSpeed):

        self.setLeftSpeed(leftSpeed)
        self.setRightSpeed(rightSpeed)


class ZumoReflectanceSensorArray( QTRSensors ):
    def __init__(self):

        self.pin1=Pin("X2",Pin.IN)
        self.pin2=Pin("X22",Pin.IN)
        self.pin3=Pin("Y8",Pin.IN)
        self.pin4=Pin("X19",Pin.IN)
        self.pin5=Pin("X21",Pin.IN)
        self.pin6=Pin("X3",Pin.IN)
        self.emitterPin=Pin(ZUMO_SENSOR_ARRAY_DEFAULT_EMITTER_PIN ,Pin.OUT)
        super().__init__( [self.pin1,self.pin2,self.pin3,self.pin4,self.pin5,self.pin6],self.emitterPin, timeout=2000)



#car=Zumo()
