# Show how to driver the Buzzer directly from MicroPython
from pyb import Pin, Timer
from time import sleep

# Jouer une frequence donnee (donc une note)
def tone( freq ):
	if freq == 0:
		ch.pulse_width_percent( 0 )
	else:
		tim.freq( freq )
		ch.pulse_width_percent( 30 )

tone( 523 ) # Do
sleep( 1 )
tone( 0 )
