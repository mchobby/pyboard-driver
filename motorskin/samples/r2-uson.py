from pyb import delay
from r2wheel import Robot2Wheel
from ultrasonic import Ultrasonic

r2 = Robot2Wheel() 

MIN_DISTANCE = 20 # Minimum distance 

r2.forward()
while True:
    if r2.distance() < MIN_DISTANCE:
        r2.halt()
        delay(100)
        r2.backward( 50 )
        delay(300)

        r2.right()
        delay( 350 )

        r2.halt()
        delay(100)

    # If nothing in front then move
    if (r2.state == Robot2Wheel.HALTED) and (r2.distance() > MIN_DISTANCE): 
        r2.forward()