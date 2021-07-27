"""
qtrsensors.py - easy library for Pololu Reflectance Sensors for MicroPython Pyboard Original.

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

__version__ = "0.0.2"
__repo__ = "https://github.com/mchobby/pyboard-driver.git"

from machine import Pin
import time

QTR_NO_EMITTER_PIN = None
QTR_EMITTERS_OFF = 0
QTR_EMITTERS_ON = 1
QTR_EMITTERS_ON_AND_OFF = 2
QTR_MAX_SENSORS =16


class QTRSensors(object):
    def __init__(self,pins,emitterPin,timeout=4000):
        # pins est une list, emitterPin=QTR_NO_EMITTER_PIN when no emitter pin
        # arduino (4,5,A0,A2,A3,11)
        # python  (X2,X3,X19,X21,X22,Y8)
        self.calibrationMinimumOn=None
        self.calibrationMaximumOn=None
        self.calibrationMinimumOff=None
        self.calibrationMaximumOff=None

        self._lastValue = 0
        self.timeout = timeout
        self._maxValue = timeout
        self._sensors = pins

        if (len(self._sensors)>QTR_MAX_SENSORS): # Max 16
            self._numSensors=QTR_MAX_SENSORS
        else:
            self._numSensors = len(self._sensors)

        self._emitterPin=emitterPin

    def read(self,sensor_values,readMode=QTR_EMITTERS_ON):
        off_values=[0 for i in range(self._numSensors)]

        if (readMode ==  QTR_EMITTERS_ON) or (readMode == QTR_EMITTERS_ON_AND_OFF):
            self.emittersOn()
        else:
            self.emittersOff()

        self.readPrivate(sensor_values)
        self.emittersOff()

        if (readMode == QTR_EMITTERS_ON_AND_OFF):
            self.readPrivate(off_values)
            for i in range(self._numSensors):
                sensor_values[i] += self._maxValue - off_values[i]

    def readPrivate(self,sensor_values):
        """ return a list with timed values uS for each sensor. """
        assert len(sensor_values) == len( self._sensors ), "sensor_values must have %s items" % len( self._sensors )

        for i in range(len(self._sensors)): # clear sensor values
            sensor_values[i] = self.timeout

        for x in self._sensors:
            x.init(Pin.OUT)
            x.value([1])
        time.sleep_us(10) # Let Capacitor loading

        for x in self._sensors: # Now read back the pins lebels
            x.init(Pin.IN)

        startTime=time.ticks_us()
        while time.ticks_diff(time.ticks_us(),startTime) < self._maxValue:
            endTime=time.ticks_us()
            _time = time.ticks_diff(endTime,startTime)
            for i in range( len(self._sensors) ):
                if (self._sensors[i].value() == 0) and (_time < sensor_values[i]):
                    sensor_values[i]=_time


    def emittersOn(self):
        if (self._emitterPin==QTR_NO_EMITTER_PIN):
            return
        self._emitterPin.init(Pin.OUT)
        self._emitterPin.value(1)
        time.sleep_us(200)

    def emittersOff(self):
        if (self._emitterPin == QTR_NO_EMITTER_PIN):
            return
        self._emitterPin.init(Pin.OUT)
        self._emitterPin.value(0)
        time.sleep_us(200)

    def calibrate(self,readMode=QTR_EMITTERS_ON):
        if (readMode == QTR_EMITTERS_ON_AND_OFF) or (readMode == QTR_EMITTERS_ON): #2 ou 0
            self.calibrationMinimumOn, self.calibrationMaximumOn = self.calibrateOnOrOff(self.calibrationMinimumOn, self.calibrationMaximumOn,QTR_EMITTERS_ON)
            # print("calib min-max : %s - %s" %(self.calibrationMinimumOn, self.calibrationMaximumOn) )
        if (readMode==QTR_EMITTERS_ON_AND_OFF) or (readMode==QTR_EMITTERS_OFF):
            self.calibrationMinimumOff, self.calibrationMaximumOff = self.calibrateOnOrOff(self.calibrationMinimumOff, self.calibrationMaximumOff,QTR_EMITTERS_OFF)

    def calibrateOnOrOff(self,calibrateMinimum,calibrateMaximum,readMode): #entrée calibrateMin=0 et calibrateMax = 0
        # Return a tuple with max & min calibration
        _sensor_values = [0 for i in range(self._numSensors)]
        max_sensor_values=[0 for i in range(self._numSensors)]
        min_sensor_values=[0 for i in range(self._numSensors)]
        _calibrateMinimum =[calibrateMinimum for i in range(self._numSensors)] #calibrateMinimum 0-6
        _calibrateMaximum =[calibrateMaximum for i in range(self._numSensors)] #calibrateMaximum 0-6

        for i in range(self._numSensors):
            _calibrateMinimum[i]=self._maxValue
            _calibrateMaximum[i]=0

        for x in range(10):
            self.read(_sensor_values,readMode)
            for y in range(self._numSensors):
                # find a Max value
                if (x==0) or (max_sensor_values[y] < _sensor_values[y]):
                    max_sensor_values[y]=_sensor_values[y]
                # find a min value
                if (x==0) or (min_sensor_values[y] > _sensor_values[y]):
                    min_sensor_values[y]=_sensor_values[y]

        for i in range(self._numSensors):
            if (min_sensor_values[i]> _calibrateMaximum[i]):
                _calibrateMaximum[i] = max_sensor_values[i]
            if (max_sensor_values[i]< _calibrateMinimum[i]):
                _calibrateMinimum[i]=min_sensor_values[i]

        return (_calibrateMinimum,_calibrateMaximum)


    def resetCalibration(self):
        for i in range(self._numSensors):
            if (self.calibrationMinimumOn):
                self.calibrationMinimumOn[i]=self._maxValue
            if (self.calibrationMinimumOff):
                self.calibrationMinimumOff[i]=self._maxValue
            if (self.calibrationMaximumOn):
                self.calibrationMaximumOn[i]=0
            if (self.calibrationMaximumOff):
                self.calibrationMaximumOff[i]=0

    def readCalibrated(self,sensor_values,readMode=QTR_EMITTERS_ON):
        x=0
        calmax = [0 for i in range(self._numSensors)]
        calmin = [0 for i in range(self._numSensors)]
        if (readMode == QTR_EMITTERS_ON_AND_OFF) or (readMode == QTR_EMITTERS_OFF):  #0 ou 2
            if (self.calibrationMinimumOff==None) or (self.calibrationMaximumOff==None):
                return
        if (readMode == QTR_EMITTERS_ON_AND_OFF) or (readMode == QTR_EMITTERS_ON):    # 1 ou 2
            if (self.calibrationMinimumOn==None)  or (self.calibrationMaximumOn==None):
                return
        self.read(sensor_values,readMode)

        for i in range(self._numSensors):
            if (readMode == QTR_EMITTERS_ON):
                calmax = self.calibrationMaximumOn[i]
                calmin = self.calibrationMinimumOn[i]
            elif(readMode == QTR_EMITTERS_OFF):
                calmax = self.calibrationMaximumOff[i]
                calmin = self.calibrationMinimumOff[i]
            else: #QTR_EMITTERS_ON_AND_OFF
                if self.calibrationMinimumOff[i] < self.calibrationMinimumOn[i]:
                    calmin = self._maxValue
                else:
                    calmin = self.calibrationMinimumOn[i] + self._maxValue - self.calibrationMinimumOff[i]

                if self.calibrationMaximumOff[i] < self.calibrationMaximumOn[i]:
                    calmax = self._maxValue
                else:
                    calmax = self.calibrationMaximumOn[i] + self._maxValue - self.calibrationMaximumOff[i]
            denominator = calmax-calmin

            if (denominator != 0):
                x = (sensor_values[i] - calmin)*1000/denominator

            if (x<0):
                x=0
            elif (x>1000):
                x = 1000
                sensor_values[i] = x

    def readLine(self,sensor_values,readMode=QTR_EMITTERS_ON,white_line=False):
        """ return around 0 for left most sensor, 1000 for second sensor, ... 5000 the right most sensor """
        on_line=0

        avg=0
        sum=0
        self.readCalibrated(sensor_values,readMode)

        for i in range(self._numSensors):
            value = sensor_values[i]
            if(white_line):
                value = 1000-value
            if(value > 400): # was 200 in original code
                on_line = 1
            if (value > 50):
                avg += value * (i*1000)
                sum +=value

        if (on_line==0):
            if((self._lastValue)< ((self._numSensors -1)*1000/2)):
                return 0
            else:
                return (self._numSensors-1)*1000
        self._lastValue = avg/sum
        return self._lastValue

class QTRSensorsAnalog(object):
    """this class isn't used in this projet. The original arduino library can be found on: https://github.com/pololu/qtr-sensors-arduino/releases"""
    pass
