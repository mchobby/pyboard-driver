# This script check the main functionnality of the Pyboard-Uno-R3
from pyb import Servo
from unoextra import *
from uno import *
from time import sleep
lcd = Unoled()

ERROR_TONE = 349

# Absolute position drawing & text
lcd.text("Board", 10,10, 1)
lcd.text("Test !", 10,20, 1)
# Draw a white rectangle - rect( x, y, w, h, c )
lcd.rect( 3, 3, 128-2*3, 64-2*3, 1 )
lcd.show() # must be called
sleep( 1 )

lcd.clear()
lcd.println("--Test--")

lcd.print( "Buzzer:" )
bz = Buzzer()
# Play the Do @ 523 Hertz
bz.tone( 523 )
sleep( 0.200 )
bz.tone()

lcd.println( "ok" )

lcd.print( "Charger: " ) # Auto refresh the screen
try:
	ch = Charger()
	pg = ch.power_good
	lcd.println( 'ok' )
except:
	lcd.println( 'FAILED!' )
	lcd.println( 'Check power')
	lcd.println( 'Check cord !!!')
	bz.tone( ERROR_TONE )
	sleep( 1 )
	bz.tone()
	raise

lcd.print( "NeoPixel:" )
led = pixels() # just one LED
red   = (255,0,0)
green = (0,255,0)
blue  = (0,0,255)
led.fill( red )
led.write()
sleep(1)

led.fill( green )
led.write()
sleep(1)

led.fill( blue )
led.write()
sleep(1)

led.fill( (255,0,255) ) # Magenta
led.write()
sleep(1)

led.fill( (0,0,0) ) # Black
led.write()
lcd.println( 'ok' )

lcd.print( "Servo:")
servo1 = Servo(1) # from -90 to +90 angle. At 0 degree at initialisation
servo2 = Servo(2)
servo3 = Servo(3)
servo4 = Servo(4)

# Create a list of sevo for convenience
servo_list = [ servo1,servo2, servo3, servo4 ]

print( "All servos at -90" )
for servo in servo_list:
	servo.angle( -90 )
	sleep( 0.5 )

print( "All servos at +90" )
for servo in servo_list:
	servo.angle( +90 )
	sleep( 0.5 )

print( "All servos at 0 degree (at once)" )
for servo in servo_list:
	servo.angle( 0 )
lcd.println( "ok" )

lcd.println( 'Test complete' )
# Play the Do @ 523 Hertz
bz.tone( 523 )
sleep( 0.200 )
bz.tone()
sleep( 0.200 )
bz.tone( 523 )
sleep( 0.200 )
bz.tone()
