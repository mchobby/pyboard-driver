from servorobot import *
from pyb import I2C

# Initialise le bus I2C
i2c = I2C( 2, I2C.MASTER )

# Define the PCA9685 controlers (i2c_bus, controler_address)
ctrls = [ (i2c,0x40) ]

# Initialise the RobotBase
r = RobotBase( controlers=ctrls ) 

# Control a RobotBase Servo via the ServoJoint class
# Set the servo #15 (set on +45°) on the first controler
# With ServoJoint, angles are in the range -90°, +90°
j = ServoJoint( r, 15 )
j.set( 45 )  