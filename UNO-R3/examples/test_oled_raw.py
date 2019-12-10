# Test the OLED screen present on the PYBOARD-UNO-R3 board
#
# This example use MicroPython SSD1306 driver (see MicroPython GitHub)

from machine import I2C, Pin
from ssd1306 import SSD1306_I2C

i2c=I2C(sda=Pin("Y4"), scl=Pin("Y3"))
lcd=SSD1306_I2C(128,64,i2c)
# clear the screen
lcd.fill(0)
# Draw the text
lcd.text("Bonjour", 10,10, 1)
lcd.text("MicroPython !", 10,20, 1)
# Draw a white rectangle - rect( x, y, w, h, c )
lcd.rect( 3, 3, 128-2*3, 64-2*3, 1 )
lcd.show()
