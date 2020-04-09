"""
pin_out_heartbeat.py - Simulate a heartbeat pulse on the S8 pin

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
from time import sleep_ms
p = Pin( "S8", Pin.OUT )
while True:
	sleep_ms( 1300 )
	p.value( 1 )
	sleep_ms( 80 )
	p.value( 0 )
	sleep_ms( 80 )
	p.value( 1 )
	sleep_ms( 80 )
	p.value( 0 )
