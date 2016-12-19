from servorobot import RobotBase
from pyb import I2C

# Initialise le bus I2C
i2c = I2C( 2, I2C.MASTER )

# Define the PCA9685 controlers (i2c_bus, controler_address)
ctrls = [ (i2c,0x40) ]

# Initialise the RobotBase
r = RobotBase( controlers=ctrls ) 

# Direct control of the servo #15 (set on 60°) on the first controler
r.ctrls[0].position(15,60)  