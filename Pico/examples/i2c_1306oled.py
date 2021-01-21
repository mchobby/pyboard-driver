# Affiche des Images et du Texte sur un ecran OLED ssd1306 OLED pilote en I2C
#
# Utilise le Pilote MicroPython SSD1306 disponible ici:
# https://github.com/micropython/micropython/blob/master/drivers/display/ssd1306.py
# 
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import framebuf

WIDTH = 128 # oled display width
HEIGHT = 32 # oled display height

i2c = I2C(0) # Init I2C using I2C0 defaults, SCL=Pin(GP9), SDA=Pin(GP8), freq=400000
print("I2C Address: "+hex(i2c.scan()[0]).upper())  # Display device address
print("I2C Configuration: "+str(i2c)) # Display I2C config


oled = SSD1306_I2C(WIDTH, HEIGHT, i2c) # Init oled display

# Raspberry Pi logo sous forme d un tableau d octets de 32x32
buffer = None
buffer =bytearray(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00|?\x00\x01\x86@\x80\x01\x01\x80\x80\x01\x11\x88\x80\x01\x05\xa0\x80\x00\x83\xc1\x00\x00C\xe3\x00\x00~\xfc\x00\x00L'\x00\x00\x9c\x11\x00\x00\xbf\xfd\x00\x00\xe1\x87\x00\x01\xc1\x83\x80\x02A\x82@\x02A\x82@\x02\xc1\xc2@\x02\xf6>\xc0\x01\xfc=\x80\x01\x18\x18\x80\x01\x88\x10\x80\x00\x8c!\x00\x00\x87\xf1\x00\x00\x7f\xf6\x00\x008\x1c\x00\x00\x0c \x00\x00\x03\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")


# Charge le logo raspberry pi dans le framebuffer (l image mesure 32x32)
fb = framebuf.FrameBuffer(buffer, 32, 32, framebuf.MONO_HLSB)

# Efface l ancien contenu de l ecran au cas ou il y ait des choses dessus
oled.fill(0)

# Envoie l image du framebuffer vers l ecran
oled.blit(fb, 96, 0)

# Ajouter du texte
oled.text("Raspberry Pi",5,5)
oled.text("Pico",5,15)

# Finalement faire afficher l image et le texte par l ecran OLED.
oled.show()

