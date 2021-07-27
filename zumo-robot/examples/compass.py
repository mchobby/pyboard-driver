"""
compass.py - easy magnetometer Example for Pyboard Original.

* Author(s):    Braccio M.  from MCHobby (shop.mchobby.be).
                Meurisse D. from MCHobby (shop.mchobby.be).

See project source @ https://github.com/mchobby/pyboard-driver/tree/master/zumo-robot
REQUIRES Library LSM303.py in the project source
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
# OUT OF OR IN

from zumoshield import ZumoReflectanceSensorArray, ZumoMotor
from pushbutton import Pushbutton
from zumobuzzer import PololuBuzzer
from lsm303 import LSM303,Vector

from pyb import Timer, Pin
from micropython import const
from machine import I2C

import time
import struct
import math

ZUMO_BUTTON=Pin("Y7",Pin.IN, Pin.PULL_UP)
#Magnetometer gauss avec high resolution
MAGGAIN_2       =const(0x00)
MAGGAIN_4       =const(0x01)
MAGGAIN_8       =const(0x02)
MAGGAIN_12      =const(0x03)

#magnetometre data rates
MAGRATE_3_1     = const(0x60)
MAGRATE_6_2     = const(0x64)
MAGRATE_12_5    = const(0x68)
MAGRATE_25      = const(0x6C)
MAGRATE_50      = const(0x70)
MAGRATE_100     = const(0x74)


#I2C Initiation
i2c = I2C(2)
# i2c.scan()
# print(i2c.scan())

#Initiation
compass = LSM303(i2c)
reflectanceSensors = ZumoReflectanceSensorArray()
motors = ZumoMotor()
button = Pushbutton(ZUMO_BUTTON)
buzzer = PololuBuzzer()

#constants
SPEED = 150
TURN_BASE_SPEED = 100
CALIBRATION_SAMPLES = 70
DEVIATION_THRESHOLD = 5

#---------- FUNCTIONS ----------
def averageHeading():
    global compass
    global avg
    avg=Vector(0,0,0)
    for x in range(10):
        compass.read()
        avg.x += compass.m.x
        avg.y += compass.m.y

    avg.x /= 10.0
    avg.y /= 10.0
    #moyenne des 10 mesures du magnétometre
    #avg est un vecteur
    rep=heading()

    return(rep) #retourn un angle en degrées

def relativeHeading(heading_from,heading_to):
    relative_heading=float(heading_to) - float(heading_from)

    if (relative_heading > 180):
        relative_heading -=360
    if (relative_heading <-180):
        relative_heading +=360

    return (relative_heading)

def heading():
    x_scaled = 2.0*(avg.x-compass.m_min.x)/(compass.m_max.x - compass.m_min.x) - 1.0
    y_scaled = 2.0*(avg.y-compass.m_min.y)/(compass.m_max.y - compass.m_min.y) - 1.0

    angle = math.atan2(y_scaled, x_scaled)*180/ math.pi    #sortie en radian, angle entre le vecteur magnétique qui pointe vers le nord
    if (angle < 0):
        angle+= 360
    return(angle)


#---------- SETUP CODE ----------

running_min = Vector(32767,32767,32767)
running_max = Vector(-32767,-32767,-32767)


compass.enableDefault()
compass._write_u8(0x25,(MAGGAIN_2<<5))
compass._write_u8(0x24,MAGRATE_100 )


button.waitForButton()
print("Starting calibration...")
motors.setLeftSpeed(SPEED)
motors.setRightSpeed(-SPEED)

for x in range(CALIBRATION_SAMPLES):
    compass.read()
    running_min.x = min(running_min.x,compass.m.x)
    running_min.y = min(running_min.y,compass.m.y)

    running_max.x = max(running_max.x,compass.m.x)
    running_max.y = max(running_max.y,compass.m.y)
    print("COMPTEUR: %s | Running_max: %s | Running_min: %s " %(x,running_max,running_min))

    time.sleep_ms(50)
motors.setLeftSpeed(0)
motors.setRightSpeed(0)
print("====================================================================================================================================")
print("Max.x: %s | Max.y: %s | Min.x: %s | Min.y: %s" %(running_max.x,running_max.y,running_min.x,running_min.y))
print("====================================================================================================================================")
print("Calibration Done.")
compass.m_max.x = running_max.x
compass.m_max.y = running_max.y
compass.m_min.x = running_min.x
compass.m_min.y = running_min.y
button.waitForButton()
target_heading = averageHeading()           #


#---------- LOOP CODE ----------

while(True):

    #target_heading = averageHeading()    ERREUR la variable est tout le temps mis a joure
    _heading = averageHeading()
    relative_heading = relativeHeading(_heading,target_heading)

    print("Target heading: %s | Actual heading: %s | Difference: %s " %(target_heading,_heading,relative_heading))
    if(abs(relative_heading)<DEVIATION_THRESHOLD):     #si la différence est plus petite que 5 on avance, sinon on tourne
        motors.setSpeeds(SPEED,SPEED)
        print("       STRAIGHT")
        time.sleep_ms(1000)
        motors.setSpeeds(0,0)
        time.sleep_ms(100)

        target_heading=math.fmod((averageHeading()+90.0), 360)               #on avance tout droit et on calcul la nouvelle position pour tourner
    else:
        speed=SPEED*relative_heading/180
        if (speed<0):
            speed -= TURN_BASE_SPEED
        else:
            speed += TURN_BASE_SPEED
        motors.setSpeeds(speed,-speed)
        print("        TURN")
