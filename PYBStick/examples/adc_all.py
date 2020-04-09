"""
adc_all.py - read all the ADC available on the PYBStick and returns the value

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

from pyb import ADC
from time import sleep

PIN_NAMES = ["S8", "S10", "S12", "S19", "S23", "S26"]
print( "Preparing ADCs for pins : %s" % PIN_NAMES )
adcs = [ (pin_name, ADC(pin_name)) for pin_name in PIN_NAMES ]

while True:
	for pin_name, adc in adcs:
		val = adc.read()
		volt = val * 3.3 / 4095
		print( "ADC %s : %4i, %3.2f v" %(pin_name, val, volt) )
	print( "-"*40 )
	sleep( 1 )
