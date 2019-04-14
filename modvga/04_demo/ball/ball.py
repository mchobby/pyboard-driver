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
spi.init( baudrate=20000000, phase=0, polarity=0 ) # raise @ 20 Mhz
# We must manage the SS signal ourself
ss = Pin( Pin.board.Y5, Pin.OUT )

# Gameduino Lib
gd = Gameduino( spi, ss )
gd.begin()

# === Toolbox ==================================================================
def draw_ball( x, y, pal ):
	global gd
	gd.xsprite(x, y, -40, -56, 0, pal, 0)
	gd.xsprite(x, y, -24, -56, 1, pal, 0)
	gd.xsprite(x, y, -8, -56, 2, pal, 0)
	gd.xsprite(x, y, 8, -56, 3, pal, 0)
	gd.xsprite(x, y, 24, -56, 4, pal, 0)
	gd.xsprite(x, y, -56, -40, 5, pal, 0)
	gd.xsprite(x, y, -40, -40, 6, pal, 0)
	gd.xsprite(x, y, -24, -40, 7, pal, 0)
	gd.xsprite(x, y, -8, -40, 8, pal, 0)
	gd.xsprite(x, y, 8, -40, 9, pal, 0)
	gd.xsprite(x, y, 24, -40, 10, pal, 0)
	gd.xsprite(x, y, 40, -40, 11, pal, 0)
	gd.xsprite(x, y, -56, -24, 12, pal, 0)
	gd.xsprite(x, y, -40, -24, 13, pal, 0)
	gd.xsprite(x, y, -24, -24, 14, pal, 0)
	gd.xsprite(x, y, -8, -24, 15, pal, 0)
	gd.xsprite(x, y, 8, -24, 16, pal, 0)
	gd.xsprite(x, y, 24, -24, 17, pal, 0)
	gd.xsprite(x, y, 40, -24, 18, pal, 0)
	gd.xsprite(x, y, -56, -8, 19, pal, 0)
	gd.xsprite(x, y, -40, -8, 20, pal, 0)
	gd.xsprite(x, y, -24, -8, 21, pal, 0)
	gd.xsprite(x, y, -8, -8, 22, pal, 0)
	gd.xsprite(x, y, 8, -8, 23, pal, 0)
	gd.xsprite(x, y, 24, -8, 24, pal, 0)
	gd.xsprite(x, y, 40, -8, 25, pal, 0)
	gd.xsprite(x, y, -56, 8, 26, pal, 0)
	gd.xsprite(x, y, -40, 8, 27, pal, 0)
	gd.xsprite(x, y, -24, 8, 28, pal, 0)
	gd.xsprite(x, y, -8, 8, 29, pal, 0)
	gd.xsprite(x, y, 8, 8, 30, pal, 0)
	gd.xsprite(x, y, 24, 8, 31, pal, 0)
	gd.xsprite(x, y, 40, 8, 32, pal, 0)
	gd.xsprite(x, y, -56, 24, 33, pal, 0)
	gd.xsprite(x, y, -40, 24, 34, pal, 0)
	gd.xsprite(x, y, -24, 24, 35, pal, 0)
	gd.xsprite(x, y, -8, 24, 36, pal, 0)
	gd.xsprite(x, y, 8, 24, 37, pal, 0)
	gd.xsprite(x, y, 24, 24, 38, pal, 0)
	gd.xsprite(x, y, 40, 24, 39, pal, 0)
	gd.xsprite(x, y, -40, 40, 40, pal, 0)
	gd.xsprite(x, y, -24, 40, 41, pal, 0)
	gd.xsprite(x, y, -8, 40, 42, pal, 0)
	gd.xsprite(x, y, 8, 40, 43, pal, 0)
	gd.xsprite(x, y, 24, 40, 44, pal, 0)


# === Setup ====================================================================
with open( 'bg_pic.bin', 'rb' ) as f:
	gd.copybin( f, RAM_PIC )
with open( 'bg_pal.bin', 'rb' ) as f:
	gd.copybin( f, RAM_PAL )
with open( 'bg_chr.bin', 'rb' ) as f:
	gd.copybin( f, RAM_CHR )

# Sprite graphics
print( 'Uncompressing ball...')
with open( 'ball.bin', 'rb' ) as f:
	gd.uncompress( RAM_SPRIMG, f ) # Uncompress a file instead of a Bytes

# Palettes 0 and 1 are for the ball itself,
# and palette 2 is the shadow.  Set it to all gray.
print( 'setting palette...' )
for i in range( 256 ):
	gd.wr16(RAM_SPRPAL + (2 * (512 + i)), rgb(64, 64, 64));

# Set color 255 to transparent in all three palettes
gd.wr16(RAM_SPRPAL + 2 * 0xff,  TRANSPARENT);
gd.wr16(RAM_SPRPAL + 2 * 0x1ff, TRANSPARENT);
gd.wr16(RAM_SPRPAL + 2 * 0x2ff, TRANSPARENT);

# === Loop =====================================================================
RADIUS = int((112 / 2)) # radius of the ball, in pixels
YBASE = (300 - RADIUS)

print( 'Go go go...' )
x, y = 200, RADIUS   # x,y ball position
xv, yv = 2, 0        # ball velocity
r = 0				 # frame counter
while True:
	r += 1
	gd.__wstartspr( 256 if r & 1 else  0 ) # write sprites to other frame
	draw_ball(x + 15, y + 15, 2) # draw shadow using palette 2
	draw_ball(x, y, r & 1)       # draw ball using palette 0 or 1
	gd.__end();

	# paint the new palette
	palette = RAM_SPRPAL + 512 * (r & 1)
	for li in range( 7 ):
		liv = 0x90 + 0x10 * li  # brightness goes 0x90, 0xa0, etc
		red = rgb(liv, 0, 0)    # uint16_t
		white = rgb(liv, liv, liv)
		for i in range(32): # palette cycling using 'r'
			gd.wr16(palette, red if ((i + r) & 16) else white)
			palette += 2

	# bounce the ball around
	x += xv
	if ((x < RADIUS) or (x > (400 - RADIUS))):
		xv = -1 * xv
	y += yv
	if ((yv > 0) and (y > YBASE)) :
		y = YBASE - (y - YBASE)  # reflect in YBASE
		yv = -1* yv              # reverse Y velocity

	if 0 == (r & 3):
		yv += 1 # gravity

	# swap frames
	gd.waitvblank()
	gd.wr(SPR_PAGE, (r & 1) )

# Finally
print( "That's all folks" )
