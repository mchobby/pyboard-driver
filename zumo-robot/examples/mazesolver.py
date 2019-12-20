"""
mazesolver.py - easy mazesolver Example for Pyboard Original.

* Author(s):    Braccio M.  from MCHobby (shop.mchobby.be).
                Meurisse D. from MCHobby (shop.mchobby.be).

See project source @ https://github.com/mchobby/pyboard-driver/tree/master/zumo-robot
REQUIRES library qtrsensors.py in the project source

   *** NOT BUG FREE ***

In some maze cases, the simplifyPath() does encounter a bug and cannot drive
the goal by following the shorter path.

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
ZUMO_BUTTON=Pin("Y7",Pin.IN)
led = Pin("Y6", Pin.OUT)
buzzer=PololuBuzzer()
reflectanceSensors=ZumoReflectanceSensorArray()
motors = ZumoMotor()
button = Pushbutton(ZUMO_BUTTON)




NUM_SENSORS = 6
SENSOR_THRESHOLD = 600
TURN_SPEED = 180
SPEED = 150
sensors = [0 for i in range(6)]
LINE_THICKNESS = 0.75
INCHES_TO_ZUNITS = 17142.0

def ABOVE_LINE(sensors):
    #quand le capteur passe sur un ligne noir 1 en sortie, sinon 0
    if (sensors)>SENSOR_THRESHOLD:
        return (1)
    else :
        return(0)

def OVERSHOOT(LINE_THICKNESS):
    return ((INCHES_TO_ZUNITS * (LINE_THICKNESS))/SPEED)

path = [0 for i in range(50)]
path_length = 0





#---------- FONCTIONS -----------
def turn(dir):          # Tourne en fonction de la lettre d'entrée
    count = 0
    last_status = 0
    sensors=[0 for i in range(NUM_SENSORS)]
    buzzer.play("c8")
    if dir == "L":
            motors.setSpeeds(-TURN_SPEED,TURN_SPEED)

            while(count < 2):
                    reflectanceSensors.readLine(sensors)
                    count += ABOVE_LINE(sensors[0]) ^ last_status
                    last_status = ABOVE_LINE(sensors[0])

                    #print("Count: %s  |last status: %s" %(count,last_status))
                    #print(sensors)
            time.sleep_ms(int(OVERSHOOT(LINE_THICKNESS)/0.5))
            print("LEFT")

    if dir== "B":   # si B Left
            #tourne a gauche
            motors.setSpeeds(-TURN_SPEED,TURN_SPEED)
            while(count < 2):
                reflectanceSensors.readLine(sensors)
                count += ABOVE_LINE(sensors[0]) ^ last_status
                last_status = ABOVE_LINE(sensors[0])
            time.sleep_ms(int(OVERSHOOT(LINE_THICKNESS)/0.5))
            print("BACK")

    elif (dir=="R"): #Right
            motors.setSpeeds(TURN_SPEED,-TURN_SPEED)
            while (count<2):
                reflectanceSensors.readLine(sensors)
                count+=ABOVE_LINE(sensors[5]) ^ last_status
                last_status = ABOVE_LINE(sensors[5])
            #Timer un peu plus long car les moteurs ne sont pas les memes
            time.sleep_ms(int(OVERSHOOT(LINE_THICKNESS)/0.4))
            print("RIGHT")
    elif(dir=="S"):
            pass
    else:
            pass

#fonction qui détermine le sens de rotation durant la phase d'apprentisage.
def selectTurn(found_left,found_straight,found_right):
    if(found_left):
        return("L")
    elif(found_straight):
        return("S")
    elif(found_right):
        return("R")
    else:
        return("B")

def followSegment():


    lastError=0
    while(True):
        position = reflectanceSensors.readLine(sensors)
        #print("Position: %s "%position)
        error = position -2500
        speedDifference = (error/4) + (6*(error-lastError))
        lastError = error
        m1Speed=SPEED+speedDifference
        m2Speed=SPEED-speedDifference
        if(m1Speed<0):
            m1Speed=0
        if(m2Speed<0):
            m2Speed=0
        if(m1Speed>SPEED):
            m1Speed=SPEED
        if(m2Speed>SPEED):
            m2Speed=SPEED
        motors.setSpeeds(m1Speed,m2Speed)
        reflectanceSensors.readLine(sensors)
        """Si on rentre dans ce if cela veut dire qu'on est a un point sans continuation de ligne"""
        if( (ABOVE_LINE(sensors[0]) == 0) and (ABOVE_LINE(sensors[1]) == 0) and (ABOVE_LINE(sensors[2]) == 0) and (ABOVE_LINE(sensors[3]) == 0) and (ABOVE_LINE(sensors[4]) == 0) and (ABOVE_LINE(sensors[5]) == 0)):
            # Si on arrive dans ce if c'est qu'il n'y a plus de ligne

            print("Dead end")
            print(sensors)
            return
        reflectanceSensors.readLine(sensors)
        #print("Intersection 1: %s" %sensors)
        """If qui montre qu'il y a une intersection a gauche ou droite"""
        if( (ABOVE_LINE(sensors[0]) == 1) or ABOVE_LINE(sensors[5]) == 1 ):
            # Si on arrive dans ce if il y a une intersection
            reflectanceSensors.readLine(sensors)
            print("Intersection 2: %s" %sensors)
            return


#regle de la main gauche. Le robot suit la ligne jusqu'a arriver à un intersection. ORDRE: Gauche, tout droit, droite.
#la fonction retient chaque tournant qu'il fait tant qu'il n'y a pas de boucle.
#Le chemin est ensuite raccourci en enlevent les chemins sans issues
#plus d'info dans le 3pi maze solving exemple
def solveMaze():
    dir = None
    comptnointer=0
    global path
    global path_length
    while(True):

        followSegment()

        """Quand on sort de la fonction followSegment c'est qu'on a trouv" une intersection ou qu'on est a la fin du labyrinthe.
        Variables pour voir si la ligne est a gauche,tout droit ou a droite"""
        found_left = 0
        found_straight = 0
        found_right = 0

        sensors=[0 for i in range(NUM_SENSORS)]
        """Juste après l'intersection ait été détectée on regarde ce qu'il y a en dessous des capteurs.
        #On regarde si il y a une chemin à gauche et/ou à droite"""
        reflectanceSensors.readLine(sensors)
        if( ABOVE_LINE(sensors[0]) == 1):
            found_left = 1
        if( ABOVE_LINE(sensors[5]) == 1):
            found_right = 1
        #print("Left: %s | right: %s | STRAIGHT: %s " %(found_left,found_right,found_straight))






        """On avance un petit peu pour être plus centré sur l'intersection au cas ou aurait loupé un chemin."""
        motors.setSpeeds(SPEED,SPEED)
        time.sleep_ms(int(OVERSHOOT(LINE_THICKNESS)/2.0))    # (((INCHES_TO_ZUNITS * (LINE_THICKNESS))/SPEED)/2)
        motors.setSpeeds(0,0)                                #   ((17142 * 0.75)/150)/2 = 42,8 ms
        reflectanceSensors.readLine(sensors)
        #on reverifie comment est l'intersection
        if( ABOVE_LINE(sensors[0]) == 1):
            found_left = 1
        if( ABOVE_LINE(sensors[5]) == 1):
            found_right = 1
        #print("Left: %s | right: %s | STRAIGHT: %s " %(found_left,found_right,found_straight))


        """On avance plus loin que l'intersection pour vérifier si il y a un chemin tout droit."""
        motors.setSpeeds(SPEED,SPEED)
        time.sleep_ms(int(OVERSHOOT(LINE_THICKNESS)*2.5))   # (((INCHES_TO_ZUNITS * (LINE_THICKNESS))/SPEED)/2)
        motors.setSpeeds(0,0)                               #   ((17142 * 0.75)/150)*2 = 171,42ms
        reflectanceSensors.readLine(sensors)



        reflectanceSensors.readLine(sensors)
        if( ABOVE_LINE(sensors[0]) == 1):
            found_left = 1
        if( ABOVE_LINE(sensors[5]) == 1):
            found_right = 1
        #print("Left: %s | right: %s | STRAIGHT: %s " %(found_left,found_right,found_straight))
        """ Si capteur 2-3 sont sur du noir il y a une ligne en face"""
        if( (ABOVE_LINE(sensors[2])==1) or (ABOVE_LINE(sensors[3])==1) ):
            reflectanceSensors.readLine(sensors)
            found_straight = 1
        """Si les 6 capteurs sont a ce point la encore toutes sur du noir c'est qu'on est arrivé a la fin"""
        if( (ABOVE_LINE(sensors[0])==1) and (ABOVE_LINE(sensors[1])==1) and (ABOVE_LINE(sensors[2])==1) and (ABOVE_LINE(sensors[3])==1) and (ABOVE_LINE(sensors[4])==1) and (ABOVE_LINE(sensors[5])==1)):
            motors.setSpeeds(0,0)
            break



        #print("Left: %s | right: %s | STRAIGHT: %s " %(found_left,found_right,found_straight))
        dir = selectTurn(found_left,found_straight,found_right)
        turn(dir)
        path[path_length]=dir
        path_length +=1
        simplifyPath()

def goToFinishLine():  #dernier loop pour refaire tout le labyrinthe en une fois
    global path
    global path_length
    sensors=[0 for i in range(NUM_SENSORS)]
    i = 0
    j = 0
    if (path[0] == "B"):
        turn("B")
        i+=1

    for j in range(i,path_length):
        followSegment()
        motors.setSpeeds(SPEED,SPEED)
        time.sleep_ms(int(OVERSHOOT(LINE_THICKNESS)/2.0))
        time.sleep_ms(int(OVERSHOOT(LINE_THICKNESS)*3.0))

        motors.setSpeeds(0,0)
        print("Tournant: %s" %path[j])
        turn(path[j])

    followSegment()
    reflectanceSensors.readLine(sensors)
    motors.setSpeeds(0,0)
    return

def simplifyPath():
    global path
    global path_length

    if ((path_length < 3) or (path[path_length -2] != "B")):
        return
    total_angle = 0

    for i in range(4):
        if(path[path_length - i] == "S"):
            total_angle += 0
        if(path[path_length - i] == "R"):
            total_angle += 90
        if(path[path_length - i] == "L"):
            total_angle += 270
        if(path[path_length - i] == "B"):
            print("if4: B")
            total_angle += 180
        total_angle = total_angle % 360
    if(total_angle == 0 ):
        path[path_length - 3] = 'S';
    if(total_angle == 90):
        path[path_length - 3] = 'R';
    if(total_angle == 180):
        path[path_length - 3] = 'B';
    if(total_angle == 270):
        path[path_length - 3] = 'L';

    for i in range(3):
        path[path_length - i] = 0

    path_length -= 2




#---------- SETUP CODE ----------


sensors=[0 for i in range(NUM_SENSORS)]
count = 0
last_status =0
turn_direction = 1

buzzer.play(">g32>>c32")
reflectanceSensors.__init__()
time.sleep_us(500)
led.value(1)
button.waitForButton()
time.sleep(1)

for i in range(4):

    # Zumo will turn clockwise if turn_direction = 1.
    # If turn_direction = -1 Zumo will turn counter-clockwise.
    turn_direction *= -1
    motors.setSpeeds(turn_direction*TURN_SPEED, -1*turn_direction * TURN_SPEED)
    while (count<2):
        reflectanceSensors.calibrate()
        reflectanceSensors.readLine(sensors)
        if (turn_direction < 0):

            #If the right  most sensor changes from (over white space -> over
            #line or over line -> over white space) add 1 to count.

            count +=ABOVE_LINE(sensors[5]) ^ last_status
            last_status=ABOVE_LINE(sensors[5])

            print(sensors)
        else:
            #Quand le capteur 0 passe sur une ligne noir above_line =1 . On fait ensuite un xor avec last_status
            count+= ABOVE_LINE(sensors[0]) ^ last_status
            last_status=ABOVE_LINE(sensors[0])

    count = 0
    last_status =0
turn("L")
motors.setSpeeds(0,0)
button.waitForButton()
motors.setSpeeds(0,0)
buzzer.play("l16 cdegreg4")
led.value(0)

#---------- LOOP ----------

while(True):
    solveMaze()
    buzzer.play(">>a32")
    while(True):
        button.waitForButton()
        goToFinishLine()
        buzzer.play("l16 cdegreg4")
		
