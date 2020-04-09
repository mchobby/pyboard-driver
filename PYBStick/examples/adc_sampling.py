"""
adc_sampling.py - Make a sampling on the PYBStick S26 (collect 8 bits values)

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

from pyb import ADC, Timer
from time import sleep

SAMPLE_FREQ = 50 # Smapling time @ 50Hz, so 50 sample per second

buffer = bytearray( 200 ) # collect 200 values
tim = Timer( 9, freq=50 ) # Set the sampling timer

adc = ADC("S26")
# Fill the buffer @ timer frequency. This will take 4 seconds in this case
# This call is blocking
adc.read_timed( buffer, tim )
# print out the collected values
timing = 0.0
for value in buffer:
	print( "%5.4f : %3i" % (timing, value) )
	timing += 1/SAMPLE_FREQ
