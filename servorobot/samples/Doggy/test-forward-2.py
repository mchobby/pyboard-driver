""" ENG: Doggy is a Robot built with 4 paws of 2 servo each.
         Move the robot forward and stop action based on a test 

    FR: Doggy est un Robot constitué de 4 pattes ayant 2 servo chacune.
        Deplace le robot sur ses pattes et arrêter l'action sur base d'un test 

    See our tutorial - voyez notre tutoriel
        https://wiki.mchobby.be/index.php?title=Hack-micropython-ServoRobot
    WebShop 
        on https://shop.mchobby.be
"""
from doggy import *

d = Doggy()

# ENG: Define a callback function that will halt the move() when returning False
# FR: Definir une fonction callback pour arrêter la méthode move() lorsqu'elle retourne False. 
def forward_until_this( robot, name, iteration ):
    # ENG: perform your exit test once upon a while (to avoids general slowing down). Eg: measuring distance with ultrason 
    #      sensor
    # FR: Effectuer votre test de sortie une fois de temps en temps (pour éviter un ralentissement général).
    #     Ex: mesurer la distance avec un senseur ultrason.
    if (iteration % 10) == 0:
        print( 'iteration = %i' % iteration )

        if iteration >= 50:
            return False
    return True  

# ENG: Move forward and repeat the move as long as the forward_until_this() returns True
# FR: Faire un movement FORWARD (avancer) aussi longtemps que la fonction forward_until_this() retourne True
d.move( 'F', repeat=forward_until_this, prepare=True)

