"""
test_buzzer.py - Exemple d'utilisation de Buzzer sur PYBStick

Fiche produit:
---> https://shop.mchobby.be/fr/micropython/1830-pybstick-lite-26-micropython-et-arduino-3232100018303-garatronic.html

------------------------------------------------------------------------

History:
  26 june 2020 - Meurisse D. - initial code
"""

from buzzer import Buzzer
from time import sleep

bz = Buzzer()
# Play the Do @ 523 Hertz
bz.tone( 523 )
# Wait one second
sleep( 1 )
# Play the Fa @ 349 Hertz
bz.tone( 349 )
# Wait one second
sleep( 1 )
# Silent
bz.tone()
