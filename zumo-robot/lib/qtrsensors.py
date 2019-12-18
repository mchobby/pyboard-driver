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

__version__ = "0.0.1"
__repo__ = "https://github.com/mchobby/pyboard-driver.git"

from machine import Pin
import time

    #def turn(self,sens,speed):
        #self.sens = sens
        #if sens == 1:
    #        self.motors[1].move(10)
    #        self.motors[0].move(-10)

    #    if sens == 2:
    #        self.motors[1].move(-10)
    #        self.motors[0].move(10)
QTR_NO_EMITTER_PIN = None
QTR_EMITTERS_OFF = 0       #valeurs pour voir comment l'emetteur doit se comporter
QTR_EMITTERS_ON = 1
QTR_EMITTERS_ON_AND_OFF = 2
QTR_MAX_SENSORS =16           #nombre max de capteurs IR possible


class QTRSensors(object):
    def __init__(self,pins,emitterPin,timeout=4000): #pins est une list, emitterPin=QTR_NO_EMITTER_PIN when no emitter pin
        #arduino (4,5,A0,A2,A3,11)
        #python  (X2,X3,X19,X21,X22,Y8)

        self.calibrationMinimumOn=None
        self.calibrationMaximumOn=None
        self.calibrationMinimumOff=None
        self.calibrationMaximumOff=None

        self._lastValue = 0
        self.timeout = timeout
        self._maxValue = timeout
        self._sensors = pins            #tableau qui regroupe les pins de la plaque IR


        if (len(self._sensors)>QTR_MAX_SENSORS):   #Si la taille de self._sensors est plus grande que le nombre max autorisé (16)
            self._numSensors=QTR_MAX_SENSORS       #Alors le nombre de capteur est = 16
        else:
            self._numSensors = len(self._sensors)       #si le nombre de capteurs est < 16 alors on regarde le nombre de capteur qu'il y a et on mets dans self._numSensors

        self._emitterPin=emitterPin                     #Broche ("X7,Pin.OUT") de l'emetteur



    def read(self,sensor_values,readMode=QTR_EMITTERS_ON):              #lire les valeurs. Entrées: sensor_values(lieste composé de 0) et readMode
        off_values=[0 for i in range(self._numSensors)]               #tableau de 16

        if (readMode ==  QTR_EMITTERS_ON) or (readMode == QTR_EMITTERS_ON_AND_OFF): #si readMode = 1 ou 2
            self.emittersOn()                                 #On allumé l'emetteur
        else:                                           #readmode == 0
            self.emittersOff()
                                               #Si readMode = 2 on eteint

        self.readPrivate(sensor_values)                     #Appel de la fonction readPrivate pour lire les valeurs des capteurs
        self.emittersOff()

        if (readMode == QTR_EMITTERS_ON_AND_OFF):        #si readMode = 2
            self.readPrivate(off_values)                 #Appel de la methode readPrivate avec off_values comem sensor_values
            for i in range(self._numSensors):
                sensor_values[i] += self._maxValue - off_values[i]

    def readPrivate(self,sensor_values):                #entrée d'un tableau vide
        """ return a list with timed values uS for each sensor. """


        assert len(sensor_values) == len( self._sensors ), "sensor_values must have %s items" % len( self._sensors )
        #vérifie si la longeur de sensor_values(entrée de la methode) est la même que self._sensors(entrée pin de la methode init)

        #faire un sensor_values clear
        for i in range(len(self._sensors)):   #pour chaque place de la liste self._sensors
            sensor_values[i] = self.timeout   #on va introduire timeout (4000)

        for x in self._sensors:               #on mets toutes les broches en sortie
            x.init(Pin.OUT)
            x.value([1])                      #on place les broches à un etat HIGH
        time.sleep_us(10)                     #delai de 10 microsecondes pour laisser les condensateurs se charger

        for x in self._sensors:               #on place toutes les broches en entrée pour lire quand elles arrivent a un etat LOW
            x.init(Pin.IN)

        startTime=time.ticks_us()             #debut du nombre de ticks



        while time.ticks_diff(time.ticks_us(),startTime) < self._maxValue: #tant que difference entre le debut et l'instant present est plus petit que 4000 on reste dans la boucle

            endTime=time.ticks_us()                                   #le temps mis est égal à la diff entre le temps a l'instant pesent et le debut des ticks
            _time = time.ticks_diff(endTime,startTime)
            for i in range( len(self._sensors) ):                     #boucle for pour obtenir les temps des capteurs
                if (self._sensors[i].value() == 0) and (_time < sensor_values[i]):  #si la broche est a LOW et que la diff de temps est < la valeur précédente de la liste t
                    sensor_values[i]=_time                                          #on retient le nouveau temps


    def emittersOn(self):

        if (self._emitterPin==QTR_NO_EMITTER_PIN): #si le numero de broche n'est pas = à 255
            return
        self._emitterPin.init(Pin.OUT)
        self._emitterPin.value(1)

        time.sleep_us(200)

    def emittersOff(self):
        if (self._emitterPin == QTR_NO_EMITTER_PIN):        #si if est true on quitte la methode
            return
        self._emitterPin.init(Pin.OUT)                      #si le if n'est pas bon on place la broche en sortie
        self._emitterPin.value(0)                           #et on le mets a l'était LOW

        time.sleep_us(200)

    def calibrate(self,readMode=QTR_EMITTERS_ON):                           #seul le type de lecture est introduite
        if (readMode == QTR_EMITTERS_ON_AND_OFF) or (readMode == QTR_EMITTERS_ON): #2 ou 0
            self.calibrationMinimumOn, self.calibrationMaximumOn = self.calibrateOnOrOff(self.calibrationMinimumOn, self.calibrationMaximumOn,QTR_EMITTERS_ON)
            print("calib min-max : %s - %s" %(self.calibrationMinimumOn, self.calibrationMaximumOn) )
        if (readMode==QTR_EMITTERS_ON_AND_OFF) or (readMode==QTR_EMITTERS_OFF):    # 2 ou 1

            self.calibrationMinimumOff, self.calibrationMaximumOff = self.calibrateOnOrOff(self.calibrationMinimumOff, self.calibrationMaximumOff,QTR_EMITTERS_OFF)



    def calibrateOnOrOff(self,calibrateMinimum,calibrateMaximum,readMode): #entrée calibrateMin=0 et calibrateMax = 0
        #retourne un tuple avec calib max et min
        #self._calibrateMaximum = [0 for i in self.calibrationMaximumOn]

        _sensor_values = [0 for i in range(self._numSensors)]
        max_sensor_values=[0 for i in range(self._numSensors)]
        min_sensor_values=[0 for i in range(self._numSensors)]
        _calibrateMinimum =[calibrateMinimum for i in range(self._numSensors)] #calibrateMinimum 0-6
        _calibrateMaximum =[calibrateMaximum for i in range(self._numSensors)] #calibrateMaximum 0-6

        for i in range(self._numSensors):         #self._numSensors = 6. On fait ceci 6 fois pour mettre des valeurs dans calibmin/max
            _calibrateMinimum[i]=self._maxValue
            _calibrateMaximum[i]=0
            """le code va beaucoup trop lentement"""

        for x in range(10):   #De 0-9. Dernière valeur est exclue. On fait 10 fois toute l'opératio

            self.read(_sensor_values,readMode)    #On lit les valeurs des capteurs

            for y in range(self._numSensors):     #self._numSensors = 6, 0-5
                #if pour trouver la valeur max
                if (x==0) or (max_sensor_values[y] < _sensor_values[y]): #Si c'est la premère fois (x=0) ou que la valeur max est plus petit que une nouvelle valeur détectée
                    max_sensor_values[y]=_sensor_values[y]               #Si on passe le if c'est que la nouvelle valeur est plus grande que l'ancienne et on la retient
            #if pour trouver la valeur min
                if (x==0) or (min_sensor_values[y] > _sensor_values[y]):
                    min_sensor_values[y]=_sensor_values[y]


        for i in range(self._numSensors):           #0-5
            if (min_sensor_values[i]> _calibrateMaximum[i]):    #si valeur mini est plus grand que 0
                _calibrateMaximum[i] = max_sensor_values[i]     #on mets la valeur on place cette valeur dans _calibmin
            if (max_sensor_values[i]< _calibrateMinimum[i]):    #si val < que 4000
                _calibrateMinimum[i]=min_sensor_values[i]       #on place cette valeur dans _calibmax

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
