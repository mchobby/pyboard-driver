"""
 Gameduino MicroPython examples (Pyboard) for Olimex MOD-VGA board.
 Wired using the UEXT pinout proposal @ https://github.com/mchobby/pyboard-driver/tree/master/UEXT

 ASCII FAST - write ASCII text after fast GAMEDUINO initialisation

 based on porting of Arduino's GameDuino Library

Where to buy:
* MOD-VGA: https://shop.mchobby.be/uext/1431-mod-vga-33v-gameduino-alike-board-3232100014312-olimex.html
* MOD-VGA: https://www.olimex.com/Products/Modules/Video/MOD-VGA/open-source-hardware
* Pyboard: https://shop.mchobby.be/fr/micropython/570-micropython-pyboard-3232100005709.html

The MIT License (MIT)
Copyright (c) 2018 Dominique Meurisse, support@mchobby.be, shop.mchobby.be
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from machine import Pin, SPI
from gd import *
import os

# Initialize the SPI Bus (on ESP8266-EVB)
# Software SPI
#    spi = SPI(-1, baudrate=4000000, polarity=1, phase=0, sck=Pin(14), mosi=Pin(13), miso=Pin(12))
# Hardware SPI
spi = SPI(2) # MOSI=Y8, MISO=Y7, SCK=Y6, SS=Y5
spi.init( baudrate=2000000, phase=0, polarity=0 )
# We must manage the SS signal ourself
ss = Pin( Pin.board.Y5, Pin.OUT )


# Gameduino Lib
gd = Gameduino( spi, ss )
gd.begin()

# Replace initialization with faster method realoading Gameduino RAM state from
# binary files.
#   gd.ascii()
os.chdir('/sd')
with open( 'ram_pic.bin', 'rb' ) as f:
	gd.copybin( f, RAM_PIC )
with open( 'ram_chr.bin', 'rb' ) as f:
	gd.copybin( f, RAM_CHR )
with open( 'ram_pal.bin', 'rb' ) as f:
	gd.copybin( f, RAM_PAL )

gd.putstr( 5 ,  0, "  *** DEMOs ***" )
gd.putstr( 5 ,  1, "04_demo/ascii-fast/asciif.py" )

# Drawing from the 4th ligne because of a bug
gd.putstr( 0,4, 'Gameduino MicroPython driver')
gd.putstr( 0,5, 'Allow to write strings on screen.')
gd.putstr( 0,6, 'Word wraps only happens at the end of buffer' )
gd.putstr( 0,7, 'buffer which is larger than the screen.')
gd.putstr( 0,9, '1234567890'*8)
print( 'That''s all folks')
