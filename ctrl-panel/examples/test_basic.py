# Basic Initialization test for NADHAT-CONTROL-PANEL
#
# See: https://github.com/mchobby/pyboard-driver/tree/master/ctrl-panel
#
from machine import I2C
from cpanel import *
import time

i2c = I2C( 1, freq=2000000 )
p = CtrlPanel( i2c )

# Oled is FrameBuffer based
# See https://docs.micropython.org/en/latest/library/framebuf.html
#
p.oled.text("Bonjour", 10,10, 1)
p.oled.text("MicroPython !", 10,20, 1)
# Dessiner un rectangle blanc - rect( x, y, w, h, c )

p.oled.rect( 0, 0, 128, 64, 1 )
p.oled.rect( 3, 3, 128-2*3, 64-2*3, 1 )
p.oled.show() # doit être appelé

# Print the Led States
print( "Red is %s, Green is %s" % (p.red, p.green))

# Show RED led
p.red = True
p.oled.fill_rect( 10, 40, 100, 10, 0 )
p.oled.text("Red led", 10, 40)
p.oled.show()
time.sleep( 2 )

p.red = False
p.green = True
p.oled.fill_rect( 10, 40, 100, 10, 0 )
p.oled.text("Green led", 10, 40)
p.oled.show()
time.sleep( 2 )

# press the Buttons.
p.oled.fill_rect( 10, 40, 100, 10, 0 )
p.oled.text("Press buttons", 10, 40)
p.oled.show()

# Convenient translation
# SW2 = /Q_ON is not wired on the MCP23017 but on GPIO pin 28
# REQ_OFF also managed by SW2 and wired on MCP23017.GPA3
to_text = { SW1:'SW1',SW3:'SW3',SW4:'SW4',UP:'UP',DOWN:'DOWN',LEFT:'LEFT',RIGHT:'RIGHT',CLICK:'CLICK' }
while True:
	p.update()
	for key,name in to_text.items():
		if p.is_down( key ):
			p.oled.fill_rect( 10, 40, 100, 10, 0 )
			p.oled.text(name, 10, 40)
			p.oled.show()
		if p.request_off:
			p.oled.fill_rect( 10, 40, 100, 10, 0 )
			p.oled.text("Req. OFF", 10, 40)
			p.oled.show()
	time.sleep_ms( 100 )
