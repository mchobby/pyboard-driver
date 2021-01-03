# Test the PYBStick-Feather-Face's EXT port with some Olimex Interface
#
# See Project: https://github.com/mchobby/pyboard-driver/tree/master/PYBStick-feather-face
#
# Use the following material
# *
#
import modio2
import modlcd19
from machine import I2C
i2c = I2C(1)

lcd = modlcd19.MODLCD1x9( i2c )
io  = modio2.MODIO2( i2c )

lcd.write( 'MCHobby')
lcd.update()

io.relais[0] = True
