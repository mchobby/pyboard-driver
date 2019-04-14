"""
 Gameduino MicroPython examples (Pyboard) for Olimex MOD-VGA board.
 Wired using the UEXT pinout proposal @ https://github.com/mchobby/pyboard-driver/tree/master/UEXT

 scroll.py is the porting of scroll.ino - scrolling of image

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
from time import sleep_ms

# change current directory (where the bin files are stored)
os.chdir( '/sd' )

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

# === Toolbox ==================================================================
# keep the file open
f_pic = open( 'platformer_pic.bin', 'rb' )

def atxy( x, y ):
	""" Memory offset corresponding to a cursor position """
	return (y<<6)+x

def rect( gd, dst, x, y, w, h):
 	""" copy a (w,h) rectangle from the source image (x,y) into picture RAM """
	# rect(unsigned int dst, byte x, byte y, byte w, byte h)
	src = (16 * y) + x # flash_uint8_t *src = platformer_pic + (16 * y) + x
	f_pic.seek( src )
	while h>0:
		h -= 1
		gd.copybin( f_pic, dst, w )
		dst += 64
		src += 16
		f_pic.seek( src )

def single( x,y ):
	global f_pic
	f_pic.seek( (16 * y) + x )
	_r = f_pic.read( 1 ) # return a bytes object (len = 1)
	return _r[0]

def  draw_column( gd, dst ):
	""" Draw a random 8-character wide background column at picture RAM dst """
	# byte y, x, ch;

	# Clouds and sky, 11 lines
	rect(gd, dst, 0, 0, 8, 11) #8, 11

	# bottom plain sky, lines 11-28
	ch = single(0,11)
	for y in range( 11, 28 ): # for (y = 11; y < 28; y++)
		gd.fill(dst + (y << 6), ch, 8);

	# randomly choose between background elements
	what = urandom.randrange( 0, 256 )
	if (what < 10):
		# big mushroom thing
		y = urandom.randrange(11, 18)
		rect(gd, dst + atxy(0, y), 8, 18, 8, 9)
		y += 9
		i = 0
		while (y < 28):
			rect(gd, dst + atxy(0, y), 8, 23 + (i & 3), 8, 1)
			i += 1
			y += 1
	elif (what < 32):
		# pair of green bollards
		for x in range(0, 8, 4): # for (x = 0; x < 8; x += 4) {
			y = urandom.randrange(20, 25)
			rect(gd, dst + atxy(x, y), 6, 11, 4, 3)
			y += 3
			while (y < 28):
				rect(gd, dst + atxy(x, y), 6, 13, 4, 1)
				y += 1
	else:
		# hills
		for x in range( 0, 8, 2 ): # for (x = 0; x < 8; x += 2) {
			y = urandom.randrange(20, 25)
			rect( gd, dst + atxy(x, y), 4, 11, 2, 3)
			y += 3
			while (y < 28):
				rect( gd, dst + atxy(x, y), 4, 13, 2, 1)
				y += 1

	#  foreground blocks
	x = urandom.randrange(5)
	y = urandom.randrange(11, 24)
	blk = urandom.randrange(4)
	rect(gd, dst + atxy(x, y), blk * 4, 14, 4, 3)
	y += 3
	while (y < 28):
		rect( gd, dst + atxy(x, y), blk * 4, 17, 4, 1)
		y += 1

	# Ground, line 28
	ch = single(0,18)
	gd.fill( dst + atxy(0,28), ch, 8)
	# Underground, line 29
	ch = single(0,19)
	gd.fill( dst + atxy(0,29), ch, 8);


# === Setup ====================================================================
# Pic is already open
#with open( 'platformer_pic.bin', 'rb' ) as f:
f_pic.seek( 0 )
gd.copybin( f_pic, RAM_PIC )

with open( 'platformer_pal.bin', 'rb' ) as f:
	gd.copybin( f, RAM_PAL )
with open( 'platformer_chr.bin', 'rb' ) as f:
	gd.copybin( f, RAM_CHR )

for i in range(256):
	gd.sprite(i, 400, 400, 0, 0, 0)

for i in range(0,64,8):
	draw_column(gd, atxy(i, 0))

# === Loop =====================================================================
# unsigned long xscroll; 32 bits (4 bytes). range from 0 to 4,294,967,295
xscroll = 0
while True:
	xscroll += 1
	if (xscroll & 63) == 0 :
		# -- This portion of code takes about 40ms to execute --
		# figure out where to draw the 64-pixel draw_column
		# offscreen_pixel is the pixel x draw_column that is offscreen...
		offscreen_pixel = (xscroll + (7 * 64)) & 511
		# offscreen_ch is the character address
		offscreen_ch = offscreen_pixel >> 3
		draw_column( gd, atxy(offscreen_ch, 0) )
	else:
		sleep_ms( 40 )

	gd.waitvblank()
	gd.wr16( SCROLL_X, xscroll )


# Finally
print( "That's all folks" )
