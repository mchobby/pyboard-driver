""""
 Gameduino MicroPython examples (Pyboard) for Olimex MOD-VGA board.
 Wired using the UEXT pinout proposal @ https://github.com/mchobby/pyboard-driver/tree/master/UEXT

 bitmap.py is the porting of bitmap.ino

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
import urandom # on recent MicroPython Firmware v1.10+
# from math import sqrt
from time import sleep


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

# os.chdir( '/sd' )

# === Toolbox ==================================================================
def replicate( color ):
	# replicate a 2-bit color across the whole byte.  Optimization for setpixel
	return (color << 6) | (color << 4) | (color << 2) | color

def setpixel( x, y, color):
	""" Set pixel at (x,y) to color.  (note that color is replicated). """

	# Because of the way the sprites are laid out in setup(), it's not too
	# hard to translate the pixel (x,y) to an address and mask.  Taking the
	# two byte values as x7-x0 and y7-y0, the address of the pixel is:
	#    x5 x4 y7 y6 y5 y4 y3 y2 y1 y0 x3 x2 x1 x0
	# (x6, x7) gives the value of the mask.

	addr = RAM_SPRIMG | (x & 0xf) | (y << 4) | ((x & 0x30) << 8)
	mask = 0xc0 >> ((x >> 5) & 6)
	gd.wr( addr, (gd.rd(addr) & ~mask) | (color & mask) )

def line( x0, y0, x1, y1, color):
	# Draw color line from (x0,y0) to (x1,y1).

	color = replicate(color)
	steep = abs(y1 - y0) > abs(x1 - x0)
	if steep :
		x0, y0 = y0, x0
		x1, y1 = y1, x1

	if x0 > x1 :
		x0, x1 = x1, x0
		y0, y1 = y1, y0

	deltax = x1 - x0
	deltay = abs(y1 - y0)
	error = deltax / 2

	ystep = None
	if (y0 < y1):
		ystep = 1
	else:
		ystep = -1

	y = y0
	for x in range( x0, x1 ):
		if steep:
			setpixel(y, x, color)
		else:
			setpixel(x, y, color)
		error -= deltay
		if error < 0:
			y += ystep
			error += deltax

class Point():
	""" Point with speed vector """
	__slot__ = ['x','y','xv', 'yv' ]

class Triangle():
	""" Triangle with 3 moving angles """
	def __init__( self ):
		self.__points = [Point(),Point(),Point()]

	@property
	def points(self):
		return self.__points

triangle = Triangle()

def random_rgb():
	return rgb( urandom.randrange(0,256), urandom.randrange(0,256), urandom.randrange(0,256) )

def restart():
	""" Restart the drawing """
	global triangle
	# Clear the screen
	gd.fill(RAM_SPRIMG, 0, 16384);

 	#Position triangle at random
	for i in range( 3 ):
		triangle.points[i].x = 3 + urandom.randrange(0, 250)
		triangle.points[i].y = 3 + urandom.randrange(0, 250)

	# Define triangle
	# Improvement regarding the original code is the random move coeficient
	# "* urandom.randrange(1,5)". But it will also create some minor glicth
	# 
	triangle.points[0].xv = 1
	triangle.points[0].yv = 1
	# triangle.points[1].xv = -1
	triangle.points[1].xv = -1 * urandom.randrange(1,5)
	triangle.points[1].yv = 1
	triangle.points[2].xv = 1
	# triangle.points[2].yv = -1
	triangle.points[2].yv = -1 * urandom.randrange(1,5)

	# Choose a random palette
	gd.wr16(PALETTE4A, rgb(0,0,0));
	gd.wr16(PALETTE4A + 2, random_rgb())
	gd.wr16(PALETTE4A + 4, random_rgb())
	gd.wr16(PALETTE4A + 6, random_rgb())

# === Setup ====================================================================
print( 'Setup...' )
gd.ascii();
gd.putstr(0, 0,"Bitmap demonstration");

# Draw 256 sprites left to right, top to bottom, all in 4-color
# palette mode.  By doing them in column-wise order, the address
# calculation in setpixel is made simpler.
# First 64 use bits 0-1, next 64 use bits 2-4, etc.
# This gives a 256 x 256 4-color bitmap.

for i in range( 256 ):
	x =     72 + 16 * ((i >> 4) & 15)
	y =     22 + 16 * (i & 15)
	image = i & 63         # image 0-63
	pal =   3 - (i >> 6)   # palettes bits in columns 3,2,1,0
	gd.sprite( i, x, y, image, 0x8 | (pal << 1), 0)

restart()
# === Loop =====================================================================
print( "Go go go..." )
color = 0
while True:
	if urandom.randrange(1000) == 0:
		print("Restart drawing...")
		restart()

	line( triangle.points[0].x, triangle.points[0].y, triangle.points[1].x, triangle.points[1].y, color)
	line( triangle.points[1].x, triangle.points[1].y, triangle.points[2].x, triangle.points[2].y, color)
	line( triangle.points[2].x, triangle.points[2].y, triangle.points[0].x, triangle.points[0].y, color)
	color = (color + 1) & 3

	for i in range(3):
		triangle.points[i].x += triangle.points[i].xv
		triangle.points[i].y += triangle.points[i].yv
		if (triangle.points[i].x <= 0) or (triangle.points[i].x >= 255):
			triangle.points[i].xv = -1* triangle.points[i].xv
		if (triangle.points[i].y <= 0) or (triangle.points[i].y >= 255):
			triangle.points[i].yv = -1* triangle.points[i].yv;

# Finally
print( "That's all folks" )
