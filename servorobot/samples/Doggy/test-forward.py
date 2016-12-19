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

# ENG: Place the robot in standup position (wrist angle=90). Shoulders rotated at appropriate angles to start walking
#      prepare() IS IMPORTANT BEFORE STARTING A MOVEMENT
# FR: Place le robot en positions de marche (debout). Les épaules sont placés a angles adéquat pour commencer la marche
#     prepare() EST IMPORTANT AVANT DE COMMENCER UN MOUVEMENT  
d.prepare('FORWARD')

delay( 2000 )

# ENG: Move forward (wrist angle=90) in 40 steps (5 degree each)
# FR: Deplacement en marche avant (angle poignet=90) en 40 étapes (de 5 degres chacun)
for i in range( 40 ):
	d.move( 'FORWARD' )

delay( 2000 )

# ENG: Other ways to do it: call the prepare before executing 40 times the movement steps
# FR: Une autre façon de faire: appelle prepare avant d'executer 40 fois l'étape de mouvement
d.reset()
d.move( 'FORWARD', repeat=40, prepare=True)

delay( 2000 )

# ENG: Changing shoulder movement angles (min & max) as the Wrist angle (to 75degree). Set the step_angle to 2 degree instead of 5
# ENG: All parameters fits to Forward.step()
# FR: Changer les angles des mouvements des epaules (shoulder min & max) ainsi que l'angle du poignet (a 75 degrés). Chaque pas fait un déplacement de 2 degres
# FR: Tous les paramètres correspondent a Forward.step()
d.reset()
d.prepare('FORWARD', sdegree_min=0, sdegree_max=85, wdegree=75 )
for i in range( 150 ):
	d.move( 'FORWARD', sdegree_min=0, sdegree_max=85, wdegree=75, step_angle=2 )
# All in one - Tout en un
d.move( 'FORWARD', sdegree_min=0, sdegree_max=85, wdegree=75, step_angle=2, repeat=150, prepare=True )

delay( 2000 )

# ENG: Do it really the hard way (getting the Movement object). See how is implemented the Doggy.move()
# FR: Faisons le vraiment a la dure (obtenir l'objet Movement). Voyez comment est implémenté Doggy.move()
d.reset()
mov_obj = d.movement('FORWARD')
mov_obj.prepare( wdegree=65 )
for i in range( 50 ):                                                       
    mov_obj.step( wdegree=65, step_angle=10 ) 