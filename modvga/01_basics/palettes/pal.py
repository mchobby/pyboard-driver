"""
 Gameduino MicroPython examples (Pyboard) for Olimex MOD-VGA board.
 Wired using the UEXT pinout proposal @ https://github.com/mchobby/pyboard-driver/tree/master/UEXT

 pal.py is the porting of palette.ino

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
import urandom # on recent MicroPython Firmware v1.10+


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
gd.ascii() # see ascii-fast for faster init
gd.putstr(0, 0,"Sprite palettes")

# === Toolbox ==================================================================
sprnum = 0 # like static declaration
def spr( x, y, pal):
	""" int x, int y, byte pal """
	global gd
	global sprnum
	gd.sprite( sprnum, x, y, 0, pal, 0 )
	sprnum += 1

def random_color():
	return rgb(64 + urandom.randrange(0,192), 64 + urandom.randrange(0,192), 64 + urandom.randrange(0,192))

# === Setup ====================================================================
for i in range( 256 ):
	gd.wr(RAM_SPRIMG + i, i)

	# Fill all the palettes with random colors
	for i in range( 0, 4 * 256):
		gd.wr16(RAM_SPRPAL + (i << 1), random_color())
	for i in range( 0, 16):
		gd.wr16(PALETTE16A + (i << 1), random_color())
		gd.wr16(PALETTE16B + (i << 1), random_color())
	for i in range( 0, 4 ):
		gd.wr16(PALETTE4A + (i << 1), random_color())
		gd.wr16(PALETTE4B + (i << 1), random_color())

	gd.putstr(0, 8, "Four 256-color palettes")
	for i in range( 4 ):
		spr(200 + 20 * i, (8 * 8), i);

	gd.putstr(0, 12, "Two 16-color palettes")
	for i in range( 2 ):
		spr(200 + 20 * i, (8 * 12),      0x4 | i)
		spr(200 + 20 * i, (8 * 12) + 20, 0x6 | i)

	gd.putstr(0, 18, "Two 4-color palettes")
	for i in range( 2 ):
		spr(200 + 20 * i, (8 * 18),      0x8 | i)
		spr(200 + 20 * i, (8 * 18) + 20, 0xa | i)
		spr(200 + 20 * i, (8 * 18) + 40, 0xc | i)
		spr(200 + 20 * i, (8 * 18) + 60, 0xe | i)

# === Loop =====================================================================

# Nothing here

# Finally
print( "That's all folks" )
