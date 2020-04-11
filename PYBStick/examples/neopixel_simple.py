# Utilisation de la bibliothèque ws2812/neopixel avec la PYBStick
#
# Shop: https://shop.mchobby.be/55-leds-neopixels-et-dotstar
# Wiki: https://wiki.mchobby.be/index.php?title=MicroPython-Accueil#ESP8266_en_MicroPython

"""
neopixel_simple.py - Using ws2812.py (neopixel) library with the PYBStick.

* Author(s): Meurisse D. from MCHobby (shop.mchobby.be).

See:
* project source @ https://github.com/mchobby/pyboard-driver/tree/master/PYBStick
* Library source @ https://github.com/mchobby/esp8266-upy/tree/master/neopixel
* Shop: https://shop.mchobby.be/55-leds-neopixels-et-dotstar
"""
from ws2812 import NeoPixel
from time import sleep
np = NeoPixel( spi_bus=1, led_count=8, intensity=1 )

# Fixer la couleur la couleur du premier pixel
# avec un tuple (r,g,b) ou chaque valeur est
# située entre 0 et 255
np[0] = (255,0,0) # rouge

np[1] = (0,255,0) # vert
np[2] = (0,0,128) # bleu (1/2 brillance)

# Voir aussi HTML Color Picker
# https://www.w3schools.com/colors/colors_picker.asp
np[3] = (255, 102, 0) # Orange
np[4] = (255, 0, 102) # Rose bonbon
np[5] = (153, 51, 255) # Violet
np[6] = (102, 153, 255) # bleu pastel
np[7] = (153, 255, 153) # vert pastel

np.write()

sleep( 2 )

# Tout éteindre
np.fill( (0,0,0) )
np.write()
