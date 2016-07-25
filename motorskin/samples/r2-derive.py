""" Make the robot move forward for 4 seconds. 
    Adjust derivative_fix to a value between -20 to 20 to make it running on a straight line """

from r2wheel import Robot2Wheel
from pyb import delay 

r  = Robot2wheel( derivative_fix = -10 )
r.forward()
delay( 4000 )
r.halt()