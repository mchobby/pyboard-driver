"""
test_buzzer_notes.py - Exemple d'utilisation de Buzzer sur PYBStick-RP2040

Fiche produit:
---> https://shop.mchobby.be/fr/micropython/1830-pybstick-lite-26-micropython-et-arduino-3232100018303-garatronic.html

------------------------------------------------------------------------

History:
  26 june 2020 - Meurisse D. - initial code
"""
from buzzer import Buzzer, NOTES
from time import sleep

bz = Buzzer()
tempo = 300 # Play tempo
note_duration = 2 # Duration of the note
# Display available notes (space is for silent)
print( ", ".join(NOTES.keys()) )
for note in NOTES.keys():
	print( "Play note: %s " % note )
	bz.note( note, tempo*note_duration ) # 600*1000uS per note
	sleep( 0.3 ) # Wait 300ms to ear each note
# Silent
bz.tone()
