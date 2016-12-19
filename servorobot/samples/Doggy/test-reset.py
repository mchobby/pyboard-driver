""" ENG: Doggy is a Robot built with 4 paws of 2 servo each.
         This code just reset all servo to their initial centered position

    FR: Doggy est un Robot constitué de 4 pattes ayant 2 servo chacune.
         Ce code réinitialise tous les servos à leur position initiale (centrée)


    See our tutorial - voyez notre tutoriel
        https://wiki.mchobby.be/index.php?title=Hack-micropython-ServoRobot
    WebShop 
        on https://shop.mchobby.be
"""
from doggy import *

# ENG: Doggy class already issue a reset() at init time
#      Reset is needed to fix and know the initial angles of all servo motors
#
# FR: Doggy fait deja un reset() au moment de son initialisation
#      Le reset() est necessaire pour connaitre l'angle initial de tous les servo moteurs

d = Doggy()
# d.reset() 