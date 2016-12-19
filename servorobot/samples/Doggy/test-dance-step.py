""" ENG: Doggy is a Robot built with 4 paws of 2 servo each.
         This sample use the prepare position for moving right and left to make a nice dance step

    FR: Doggy est un Robot constitué de 4 pattes ayant 2 servo chacune.
        Cet exemple utilise la preparation des mouvements droit et gauche pour realiser un chouette pas de dance.


    See our tutorial - voyez notre tutoriel
        https://wiki.mchobby.be/index.php?title=Hack-micropython-ServoRobot
    WebShop 
        on https://shop.mchobby.be
"""

from doggy import *
from pyb import delay
d = Doggy()

for i in range( 5 ):
	d.prepare('L')
	d.prepare('R')
	