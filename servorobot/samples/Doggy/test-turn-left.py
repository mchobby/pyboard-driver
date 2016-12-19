""" ENG: Doggy is a Robot built with 4 paws of 2 servo each.
         Move the robot forward. There are many way to do it, form the easiest to the more complex one (parametrized)

    FR: Doggy est un Robot constitué de 4 pattes ayant 2 servo chacune.
        Deplace le robot sur ses pattes. Il y a de nombreuses facon de le faire, de la plus simple à la plus complexe (parametrisée)


    See our tutorial - voyez notre tutoriel
        https://wiki.mchobby.be/index.php?title=Hack-micropython-ServoRobot
    WebShop 
        on https://shop.mchobby.be
"""
from doggy import *
from pyb import delay
d = Doggy()

# ENG: Place the robot in standup position (wrist angle=90). Shoulders rotated at appropriate angles to start turning left
#      prepare() IS IMPORTANT BEFORE STARTING A MOVEMENT
# FR: Place le robot en positions de marche (debout). Les épaules sont placés a angles adéquat pour commencer à tourner à gauche
#     prepare() EST IMPORTANT AVANT DE COMMENCER UN MOUVEMENT  
d.prepare('LEFT')

delay( 2000 )

# ENG: Turn left (wrist angle=90) in one step of 90° (default value)
# FR: Tourne à gauche (angle poignet=90) un 1 étapes de 90° (valeur par défaut)
d.move( 'LEFT' )

delay( 2000 )

# ENG: Other ways to do it: call the prepare before executing 2 times the movement steps (of 90 degrees)
# FR: Une autre façon de faire: appelle prepare avant d'executer 2fois l'étape de mouvement (de 90 degrees)
d.reset()
d.move( 'LEFT', repeat=2, prepare=True)

delay( 2000 )

# ENG: Changing shoulder movement angles to turn on the left of 160 degree (in total) and the Wrist angle set to 75 degree. 
# ENG: All parameters fits to Left.step()
# FR: Changer les angles des mouvements des epaules pour touner à gauche de 160 degree (en total) et l'angle des poignet fixé à 5 degrees
# FR: Tous les paramètres correspondent a Left.step()
d.reset()
d.prepare('LEFT', wdegree=75 )
d.move( 'LEFT', sdegree=160, wdegree=75 )
# All in one - Tout en un
d.move( 'LEFT', sdegree=160, wdegree=75, prepare=True )

delay( 2000 )

# ENG: Do it really the hard way (getting the Movement object). See how is implemented the Doggy.move()
# FR: Faisons le vraiment a la dure (obtenir l'objet Movement). Voyez comment est implémenté Doggy.move()
d.reset()
mov_obj = d.movement('LEFT')
mov_obj.prepare( wdegree=65 )            
mov_obj.step( sdegree=60, wdegree=65, prepare=True, repeat=3 ) # repeat 3 times the turn left

# ENG: Reducing the range of movement from 60 degree (the default) to 30 degree & make a turn left of 75 degree
# FR: Réduire l'amplitude du mouvement de 60 degrés (valeur par défaut) à 30 degrées & faire une rotation à gauche de 75 degrée
d.move( 'L', sdegree=75, sdegree_max=30, prepare=True )

# ENG: You can replace LEFT by RIGHT and everything will work as expected
# FR: Vous pouvez replacer LEFT par RIGHT et tout fonctionnera comme attendu 