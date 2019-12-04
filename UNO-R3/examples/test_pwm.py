"""
test_pwm.py - how to use the easy PWM library on Pyboard Original.

* Author(s): Meurisse D. from MCHobby (shop.mchobby.be).

See project source @ https://github.com/mchobby/pyboard-driver/tree/master/UNO-R3
"""
from pwm import *
from uno import *
from time import sleep

print( "PWM on Pin 13 (Y6)")
pwm13 = pwm(PIN_13) # PIN_13 = "Y6"

print( "from 0 to 100% PWM")
for i in range(0,101, 5): # by step of 5
	pwm13.percent = i  # 0 to 100 percent of duty cycle
	sleep(0.200)

# switch back as an Input Pin
print( "Release the Pin" )
pwm13.release()
sleep( 1 )

# Reactivate PWM
print( "Reactivate PWM at 50%" )
pwm13 = pwm(PIN_13)
pwm13.percent = 50
sleep( 1 )
pwm13.percent = 0
sleep( 1 )

# Do it the Arduino Way (with 8 bit value)
print( "Use a 8bit value (0-255) to control PWM" )
for i in range(0,256,3): # by step of 3
	pwm13.write( i )
	sleep(0.050)

pwm13.release()
