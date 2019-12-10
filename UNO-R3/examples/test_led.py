# Test the Neopixel present on the PYBOARD-UNO-R3 board
# 
from uno import pixels
from time import sleep

led = pixels() # just one LED
red   = (255,0,0)
green = (0,255,0)
blue  = (0,0,255)
led.fill( red )
led.write()
sleep(1)

led.fill( green )
led.write()
sleep(1)

led.fill( blue )
led.write()
sleep(1)

led.fill( (255,0,255) ) # Magenta
led.write()
sleep(1)

led.fill( (0,0,0) ) # Black
led.write()
print("That's all Folks!")
