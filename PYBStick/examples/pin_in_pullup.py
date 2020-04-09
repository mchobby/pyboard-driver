"""
pint_in_pullup.py - Active a pull-up on the pin S3. Just link it to the ground via
                    a push button to change its state.

* Author(s): Meurisse D. from MCHobby (shop.mchobby.be).

Fiche produit:
---> https://shop.mchobby.be/fr/micropython/1830-pybstick-lite-26-micropython-et-arduino-3232100018303-garatronic.html

MCHobby investit du temps et des ressources pour écrire de la
documentation, du code et des exemples.
Aidez nous à en produire plus en achetant vos produits chez MCHobby.

------------------------------------------------------------------------

History:
  09 april 2020 - Dominique - initial code
"""
from machine import Pin
from time import sleep
p = Pin( "S3", Pin.IN, Pin.PULL_UP  )
while True:
	s = "HIGH" if p.value() else "LOW (pressed)"
	print( "S3 : %s" % s )
	sleep( 0.5 ) # wait an half second
