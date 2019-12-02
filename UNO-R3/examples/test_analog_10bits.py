# Read the voltage (0 to 3.3) on the PIN_A3 (X22) analog input
# This version of the script read the value with 10 bits resolution.
from pyb import ADC
from uno import *
from time import sleep

a3 = ADC(PIN_A3) # same as ADC("X22")
while True:
	val = analog_read(a3) # 10 bits resolution reading
	volts = val/1024*3.3
	print( "read: %i  Volts: %3f v" % (val,volts) )
	sleep( 0.500 )
