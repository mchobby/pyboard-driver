"""
borderdetect.py - easy BorderDetect Example for Pyboard Original.

* Author(s):    Braccio M.  from MCHobby (shop.mchobby.be).
                Meurisse D. from MCHobby (shop.mchobby.be).

See project source @ https://github.com/mchobby/pyboard-driver/tree/master/zumo-robot
REQUIRES library qtrsensors.py in the project source
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
from zumobuzzer import PololuBuzzer, NOTE_G
from pushbutton import PushbuttonStateMachine, Pushbutton, PushbuttonBase
from pyb import Timer, Pin
import time

QTR_THRESHOLD =1000
REVERSE_SPEED = 150
TURN_SPEED = 200
FORWARD_SPEED =200
REVERSE_DURATION=400
TURN_DURATION=400
NUM_SENSORS = 6
ZUMO_BUTTON=Pin("Y7",Pin.IN)
left_count=0
right_count=0
motors=ZumoMotor()
buzzer = PololuBuzzer()
button = Pushbutton(ZUMO_BUTTON)
led = Pin("Y6", Pin.OUT)

sensor_values=[0 for i in range(NUM_SENSORS)]
sensors=ZumoReflectanceSensorArray()

#motors.flipLeftMotor(True)
#motors.flipRightMotor(True)
def waitForButtonAndCountDown():

    led.value(1)
    button.waitForButton()
    led.value(0)
    for x in range(3):
        time.sleep(1)
        buzzer.playNote(NOTE_G(3),200,15)
    time.sleep(1)
    buzzer.playNote(NOTE_G(4),500,15)
    time.sleep(1)


led.value(1)
waitForButtonAndCountDown()

while(True):

    sensors.read(sensor_values)
    if (sensor_values[0]>QTR_THRESHOLD):
        motors.setSpeeds(-REVERSE_SPEED,-REVERSE_SPEED)
        time.sleep(REVERSE_DURATION/1000)
        motors.setSpeeds(TURN_SPEED,-TURN_SPEED)
        time.sleep(TURN_DURATION/1000)
        motors.setSpeeds(FORWARD_SPEED,FORWARD_SPEED)
        left_count+=1

    elif(sensor_values[5]>QTR_THRESHOLD):
        if (left_count>3 and right_count>3):

            REVERSE_DURATION=800
            TURN_DURATION=800
            left_count=0
            right_count=0
        motors.setSpeeds(-REVERSE_SPEED,-REVERSE_SPEED)
        time.sleep(REVERSE_DURATION/1000)
        motors.setSpeeds(-TURN_SPEED,TURN_SPEED)
        time.sleep(TURN_DURATION/1000)
        motors.setSpeeds(FORWARD_SPEED,FORWARD_SPEED)

        REVERSE_DURATION = 400
        TURN_DURATION =400
        right_count+=1

    else:
        motors.setSpeeds(FORWARD_SPEED,FORWARD_SPEED)
