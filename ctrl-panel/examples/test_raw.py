# Raw Initialization test for NADHAT-CONTROL-PANEL
# *** For DEMONSTRATION PURPOSE ONLY, do not use this as reference ***
#
# See: https://github.com/mchobby/pyboard-driver/tree/master/ctrl-panel
#
from machine import I2C, Pin
import ssd1306
from time import sleep, sleep_ms


# init bus i2c a 2MHz
i2c=I2C(1, freq=2000000)



# port A high nibble en sortie (avec GPIOA=0 POR)
i2c.writeto_mem(0x21, 0x00, b'\x0F')

# on fixe les PU de l'OLED avec les sorties PP
i2c.writeto_mem(0x21, 0x12, b'\x0F')
# reset LCD
sleep_ms(1)
i2c.writeto_mem(0x21, 0x12, b'\xCF')
sleep_ms(10)
# fin reset LCD

# Initialisation afficheur
spd0301 = ssd1306.SSD1306_I2C(width=128, height=64, i2c=i2c, addr=0x3c, external_vcc=True)
spd0301.init_display()

# Methode FrameBuffer = position absolue
# pour texte et dessin
spd0301.text("Bonjour", 10,10, 1)
spd0301.text("MicroPython !", 10,20, 1)
# Dessiner un rectangle blanc - rect( x, y, w, h, c )
spd0301.rect( 3, 3, 128-2*3, 64-2*3, 1 )
spd0301.show() # doit être appelé

sleep(2)


#from mcp230xx import MCP23017
#mcp=MCP23017(i2c, address=0x21)



loopnb = 10
while loopnb :

	sleep(1)	# sleep for 1 second
	i2c.writeto_mem(0x21, 0x12, b'\xDF')	# led D2 ON
	sleep(1)	# sleep for 1 second
	i2c.writeto_mem(0x21, 0x12, b'\xFF')	# led D2 and D1 ON
	sleep(1)	# sleep for 1 second
	i2c.writeto_mem(0x21, 0x12, b'\xCF')	# leds off
	loopnb = loopnb -1/home/domeu>
