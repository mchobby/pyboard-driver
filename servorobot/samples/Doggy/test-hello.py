""" ENG: Doggy is a Robot built with 4 paws of 2 servo each.
         This sample use the special HELLO movement to say Hello

    FR: Doggy est un Robot constitué de 4 pattes ayant 2 servo chacune.
        Cet exemple utilise le mouvement special HELLO pour dire bonjour


    See our tutorial - voyez notre tutoriel
        https://wiki.mchobby.be/index.php?title=Hack-micropython-ServoRobot
    WebShop 
        on https://shop.mchobby.be
"""

from doggy import *
from pyb import delay
d = Doggy()

# ENG: Say HELLO (H) with the right Paw. See the Hello.step() for more détails on the parameters
# FR: Dit bonjour (HELLO, H) avec la patte gauche
d.prepare( 'H' )                                                            
d.move( 'H' )                                                               

# ENG: the same with the right paw (do it twice)
# FR: la même chose avec la patte droit (le faire deux fois)
d.prepare( 'H', right=True )                                               
d.move( 'H', right=True  )                                                 
d.move( 'H', right=True  )

# ENG: Release the servo motors
# FR: Relache les servo moteurs
d.release()