"""
pyb_led.py - Exemple de démarrage de la PYBStick

* Author(s): Pierson F. from Garatronic (www.garatronic.fr).

Fiche produit:
---> https://shop.mchobby.be/fr/micropython/1830-pybstick-lite-26-micropython-et-arduino-3232100018303-garatronic.html

------------------------------------------------------------------------

History:
  19 june 2020 - Pierson F. - initial code
"""
import pyb
from pyb import LED, Switch
import time

orange=LED(3)
bleu=LED(4)
sw=Switch()

# pyb.freq(48000000)

# boucle d'affichage
while (1):
	for i in range (0,255):
		while sw.value() == True:
			time.sleep_ms(1000)
		orange.intensity(i)
		bleu.intensity(255-i)
		time.sleep_ms(5)
	for i in range (0,255):
		while sw.value() == True:
			time.sleep_ms(1000)
		orange.intensity(255-i)
		bleu.intensity(i)
		time.sleep_ms(5)
		
