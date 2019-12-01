from uno import Buzzer, NOTES
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
