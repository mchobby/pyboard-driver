"""
pushbutton.py - easy Button library for MicroPython Pyboard Original.
                See example line_follower.py in the project source

* Author(s):    Braccio M.  from MCHobby (shop.mchobby.be).
                Meurisse D. from MCHobby (shop.mchobby.be).

See project source @ https://github.com/mchobby/pyboard-driver/tree/master/zumo-robot

  23 jul 2021 - domeu - code cleaning
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


__version__ = "0.0.3"
__repo__ = "https://github.com/mchobby/pyboard-driver.git"

from pyb import Timer, Pin
import time

PULL_UP_DISABLED = 0
PULL_UP_ENABLED =1
DEFAULT_STATE_LOW = 0
DEFAULT_STATE_HIGH = 1

class PushbuttonStateMachine (object):
    def __init__(self):

        self.state = 0

    def getSingleDebouncedRisingEdge(self,value):
        self.value=value
        timeMillis = time.ticks_ms()

        if (self.state==0):
            if (self.value==False):
                prevTimeMilllis=timeMillis
                self.state=1
            return(False)
        elif(self.state==1):
            if(self.value==True):
                state=0
            elif(timeMillis-prevTimeMilllis>=15):
                self.state=2
            return(False)
        elif(self.state==2):
            if (self.value==True):
                prevTimeMilllis=timeMillis
                self.state=3
            return(False)
        elif(self.state==3):
            if(self.value==False):
                self.state=2
            elif(timeMillis-prevTimeMilllis>=15):
                self.state = 0
                return (True)
            return(False)
        return (False)

class PushbuttonBase(object):
    def __init__(self):
        self.pressState=PushbuttonStateMachine()
        self.releaseState=PushbuttonStateMachine()

    def waitForPress(self):
        while(True):
            while(self.isPressed()==True):
                time.sleep(0.01)
                return

    def waitForRelease(self):
        while(True):
            while(self.isPressed()==False):
                time.sleep(0.01)
                return

    def waitForButton(self):
        self.waitForPress()
        self.waitForRelease()

    def getSingleDebouncedPress(self):
        return(self.pressState.getSingleDebouncedRisingEdge(Pushbutton.isPressed()))

    def getSingleDebouncedRelease(self):
        return(self.releaseState.getSingleDebouncedRisingEdge(Pushbutton.isPressed()))

class Pushbutton(PushbuttonBase):
    def __init__(self, pin_name , pullup=PULL_UP_ENABLED, defaultState=DEFAULT_STATE_HIGH):
        super().__init__()
        self.pin = Pin( pin_name, Pin.IN )
        self._pullup=pullup
        self._defaultstate=defaultState
        initialized = True # This class is always initialised and doens't need to initialised before
                           # button

        if(self._pullup == PULL_UP_ENABLED):
            self.pin.init(Pin.IN, Pin.PULL_UP)
        else:
            self.pin.init(Pin.IN, Pin.PULL_NONE)
        time.sleep_us(5)

    def isPressed(self):
        return(self.pin.value()!= self._defaultstate)
