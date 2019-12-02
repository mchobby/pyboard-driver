# Read the voltage (0 to 3.3) on the PIN_A3 (X22) analog input
from pyb import ADC
from uno import *
from time import sleep

a3 = ADC(PIN_A3) # same as ADC("X22")
while True:
	val = a3.read()
	volts = val/4096*3.3
	print( "read: %i  Volts: %3f v" % (val,volts) )
	sleep( 0.500 )
