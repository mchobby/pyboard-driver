"""
test_buzzer_tune.py - Exemple d'utilisation de Buzzer sur PYBStick

Fiche produit:
---> https://shop.mchobby.be/fr/micropython/1830-pybstick-lite-26-micropython-et-arduino-3232100018303-garatronic.html

------------------------------------------------------------------------

History:
  26 june 2020 - Meurisse D. - initial code
"""
from buzzer import Buzzer
from time import sleep

bz = Buzzer()

# Play a melody:
#   List of note + rythm (coma separated)
#   First char = The note as contained in NOTES dictionnary
#   Second char = note duration (defaut=1 if missing)
tune1 = "c,c,g,g,a,a,g2,f,f,e,e,d,d,c2, 4"
tune2 = "c2,c,d3,c3,f3,e3,c2,c,d3,c3,g3,f3, 4"

bz.tune( tune1, tempo=300 ) # Slower
sleep(1)
bz.tune( tune2, tempo=200 ) # Faster

print("That's all Folks!")
