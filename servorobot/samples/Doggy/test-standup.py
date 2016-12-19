""" ENG: Doggy is a Robot built with 4 paws of 2 servo each.
         Standup the robot on its paws

    FR: Doggy est un Robot constitué de 4 pattes ayant 2 servo chacune.
         Met le robot debout sur ses pattes


    See our tutorial - voyez notre tutoriel
        https://wiki.mchobby.be/index.php?title=Hack-micropython-ServoRobot
    WebShop 
        on https://shop.mchobby.be
"""
from doggy import *
from pyb import delay
d = Doggy()

# ENG: We need to know the initial position at startup
# FR: Nous avons besoin de connaître la position initiale
d.reset() 

# ENG: Give some time for mechanical oscillation to stop
# FR: Laisser un peu de temps pour que les oscillations mécaniques se calme 
delay( 1500 )

# ENG: Place all shoulder to +20 and -20 degree
# FR: Place toutes les epaules à +20 et -20 degree
d.align( sdegree=20, asymetric=True )

# ENG: Place all wrist to +90 to standup Doggy
# FR: Place tous les poignet à +90 pour mettre Doggy debout
d.standup()
