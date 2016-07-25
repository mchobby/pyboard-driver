##
# Commande d'une plateforme robotique 2 roues avec le motor-skin et un détecteur UltraSon HC-SR04.
#    Tourne sur la droite quand il détecte un objet à moins de 20 cm. Sinon avance en ligne droite.
# Presser le bouton "SW1" pour démarrer / arrêter le robot. La LED bleue s'allume pendant que le programme est actif.
# 
# Control a 2 wheel robotic plateform with the Motor-Skin and MicroPython PyBoard
#    Turn right when detecting an object within the 20 cm. Otherwise move forward.
# Press the button "SW1" to start/stop the software. Le blue LED is lit when the software is driving the robot.
#
#   http://shop.mchobby.be/product.php?id_product=919
#   http://shop.mchobby.be/product.php?id_product=918
#   http://shop.mchobby.be/product.php?id_product=561
#   http://shop.mchobby.be/product.php?id_product=570
# 
# Voir Tutoriel - See our french tutorial
#   XXXX TODO XXXXX
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

from pyb import delay, LED
from r2wheel import Robot2Wheel                                             

r2 = Robot2Wheel() 
l = LED(4)   # LED Bleue

MIN_DISTANCE = 20 # Minimum distance 

def drive_robot():
    r2.forward()
    # Tant que pas bouton User --> Continuer
    while not( r2.button_pressed(1) ):
        #DEBUG: print( 'Running' )
        if r2.distance() < MIN_DISTANCE:
            r2.halt()
            delay(100)
            r2.backward( 50 )
            delay( 300 )

            r2.right()
            delay( 300 )

            r2.halt()
            delay(100)
        # Si rien devant --> Marche avant
        if (r2.state == Robot2Wheel.HALTED) and (r2.distance() > MIN_DISTANCE): 
            r2.forward()
    r2.halt()

# Routine principale
l.off()
while True:
    #DEBUG: print( 'Wait' )
    if r2.button_pressed(1):
        # Deparasitage logiciel
        delay( 10 )
        if r2.button_pressed(1) == True:
           # Signaler le démarrage
           l.on()
           delay( 2000 ) 
           # Piloter le robot
           drive_robot()
           l.off()
           delay( 2000 )

    delay( 300 ) # ne rien faire 