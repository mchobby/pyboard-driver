# advanced example utisng  Initialization test for NADHAT-CONTROL-PANEL
#
# See: https://github.com/mchobby/pyboard-driver/tree/master/ctrl-panel
#
from machine import I2C
from cpanel import *
import time

i2c = I2C( 1, freq=400000 )
p = CtrlPanel( i2c )

# Oled is FrameBuffer based
# See https://docs.micropython.org/en/latest/library/framebuf.html
#
p.oled.text("Button Edge", 10,10, 1)
p.oled.text("Counter !", 10,20, 1)
# Dessiner un rectangle blanc - rect( x, y, w, h, c )

p.oled.rect( 0, 0, 128, 64, 1 )
p.oled.rect( 3, 3, 128-2*3, 64-2*3, 1 )
p.oled.text("Press...", 10, 40)
p.oled.show()

# Convenient translation
# SW2 = /Q_ON is not wired on the MCP23017 but on GPIO pin 28
# REQ_OFF also managed by SW2 and wired on MCP23017.GPA3
to_text = { SW1:'SW1',SW3:'SW3',SW4:'SW4',UP:'UP',DOWN:'DOWN',LEFT:'LEFT',RIGHT:'RIGHT',CLICK:'CLICK' }

while True:
	# Press the button for 10 secondes
	print( '---------------------------------------------------' )
	print( 'Collecting for 10 sec. Press the buttons')
	t = time.time()
	while (time.time()-t) < 10:
		p.update()
		#time.sleep_ms( 100 )

	# Yo! Display the key pressed and the number of time it has been done.
	print( '----------------------------------------------------' )
	for key,name in to_text.items():
		count = p.edges( key ) # read it will reset it to 0
		if count > 0:
			print( "%s pressed %i times" % (name,count) )

	# Prepare to next round
	t = time.time()
