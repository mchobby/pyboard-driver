"""
line_follower.py - easy linefollower Example for Pyboard Original (demonstrated at Maker Faire Paris 2019)

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
from pushbutton import PushbuttonStateMachine, Pushbutton, PushbuttonBase
from pyb import Timer, Pin
import time
from zumobuzzer import PololuBuzzer
ZUMO_BUTTON=Pin("Y7",Pin.IN, Pin.PULL_UP)

reflectanceSensors = ZumoReflectanceSensorArray()
motors = ZumoMotor()
button = Pushbutton(ZUMO_BUTTON)
buzzer = PololuBuzzer()
#reflectanceSensors.calibrate()

MAX_SPEED = 200
lastError=0
compteur = 0
buzzer.play(">g8>>c8")
reflectanceSensors.__init__()

button.waitForButton()
time.sleep(1)
for i in range(80):
    if(((i>10) and (i<=30)) or ((i>50) and (i <= 70))):  #entre 10 et 30 il tourne dans un sens entre 50 et 70 il tourne dans l'autre sens
        print(i)
        motors.setSpeeds(-100,100)
    else:
        print(i)
        motors.setSpeeds(100,-100)

    reflectanceSensors.calibrate()
    time.sleep(0.02)

motors.setSpeeds(0,0)
buzzer.play(">g8>>c8")
while(True):
    sensors = [0 for i in range(6)]
    position = reflectanceSensors.readLine(sensors)
    error = position -2500
    speedDifference = (error/4) + (6*(error-lastError))
    lastError = error
    m1Speed=MAX_SPEED+speedDifference
    m2Speed=MAX_SPEED-speedDifference
    if(m1Speed<0):
        m1Speed=0
    if(m2Speed<0):
        m2Speed=0
    if(m1Speed>MAX_SPEED):
        m1Speed=MAX_SPEED
    if(m2Speed>MAX_SPEED):
        m2Speed=MAX_SPEED
    motors.setSpeeds(m1Speed,m2Speed)
    compteur = compteur+1
    if (compteur==10):
        print("line follower")
        print(sensors)
        print(position)
        compteur = 0
