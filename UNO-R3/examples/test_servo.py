# Test the 4 servo ouputs labelled SERVO1, SERVO2, SERVO3 & SERVO4
from pyb import Servo
from time import sleep
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

print( "Wait 2 seconds")
sleep( 2 )

print( "coordinate servo movement" )
# Coordonate move to -90° for servo1 & servo2 during 2 seconds
# while coordinate move to +90° for servo3 & servo4 during the same 2 seconds.
servo1.angle( +90, 2000 ) # 2000 ms = 2 sec
servo2.angle( +90, 2000 ) # 2000 ms = 2 sec
servo3.angle( -90, 2000 ) # 2000 ms = 2 sec
servo4.angle( -90, 2000 ) # 2000 ms = 2 sec
sleep( 2 ) # wait end of movement

print( "That's all folks!")
