# Test the OLED FeatherWing with the PYBStick-Feather-Face
#
# See Project: https://github.com/mchobby/pyboard-driver/tree/master/PYBStick-feather-face
#
import ssd1306
import time
from machine import I2C, Pin
i2c = I2C(1)
lcd = ssd1306.SSD1306_I2C( 128, 32, i2c )

lcd.fill(0) # Rempli l'écran en noir
# rect( x, y, w, h, c )
lcd.rect( 3, 3, 128-2*3, 32-2*3, 1 )
lcd.text("Bonjour!", 10,10, 1 )
lcd.show()  # Afficher!

pin = Pin("S15", Pin.IN, Pin.PULL_UP)
time.sleep(3)
while True:
	lcd.fill(0) # Rempli l'écran en noir
	if pin.value()==0:
		lcd.text("A pressed!", 10,10, 1 )
	else:
		lcd.text("Press A", 10,10, 1 )
	lcd.show()
	time.sleep(0.100)
