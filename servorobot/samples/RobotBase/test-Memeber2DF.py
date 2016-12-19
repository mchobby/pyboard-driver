from servorobot import *
from pyb import I2C
import time

# Initialise le bus I2C
i2c = I2C( 2, I2C.MASTER )

# Define the PCA9685 controlers (i2c_bus, controler_address)
ctrls = [ (i2c,0x40) ]

# Initialise the RobotBase
r = RobotBase( controlers=ctrls ) 

# Control a RobotBase Member2DF class wired to 2 Servo
# shouler on #0
# wrist on #1
# 
m = Member2DF( r, 0, 1 )
m.shoulder.inverted( True ) # Invert the shoulder movements
m.wrist.set( 45 )
time.sleep(2)
m.wrist.set( -45 )
m.shoulder.set( -30 )
time.sleep(2)
m.reset()  
