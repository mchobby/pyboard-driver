""""
 Gameduino MicroPython examples (Pyboard) for Olimex MOD-VGA board.
 Wired using the UEXT pinout proposal @ https://github.com/mchobby/pyboard-driver/tree/master/UEXT

 collide.py is the porting of collision.ino

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
import os
from math import sqrt
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

os.chdir( '/sd' )

NBALLS = 80

coll = list( 0 for i in range(NBALLS) ) # each entry is a byte

# === Toolbox ==================================================================
# readn() has been added to the gameduino library
# void readn(byte *dst, unsigned int addr, int c)


def load_coll():
	""" Load collisions """
	global coll
	while gd.rd(VBLANK) == 0 :  # Wait until vblank
		pass
	while gd.rd(VBLANK) == 1 :  # Wait until display
		pass
	while gd.rd(VBLANK) == 0 :  # Wait until vblank
		pass
	# read NBalls bytes() and store it into "coll" list as seperate byte
	coll = list( gd.readn(COLLISION, NBALLS) )

class Ball:
	x, y = 0,0 # int
	vx, vy = 0,0 # vitesse in x & y
	lasthit = 0 # byte

balls = [ Ball() for i in range(NBALLS) ]

def plot_balls():
	global balls
	for i in range( NBALLS ):
		gd.sprite(i, balls[i].x >> 4, balls[i].y >> 4, 0, 0, 0)

def anycolliding():
	# Detect if we have any collision
	global coll

	plot_balls()
	load_coll()

	for i in range( NBALLS ):
		# If we have a collision AND a collision with another sprite ball
		if (coll[i] != 0xff) and (coll[i]<NBALLS):
			return 1
	return 0

def place_balls():
	""" Place all balls so that none collide.  Do this by placing all at random, then moving until there are no collisions """
	global balls, coll

	for i in range( NBALLS ):
		balls[i].x = (2 + urandom.randrange( 0, 380)) << 4
		balls[i].y = (2 + urandom.randrange( 0, 280)) << 4
		balls[i].vx = urandom.randrange(-128,127)
		balls[i].vy = urandom.randrange(-128,127)
		balls[i].lasthit = 255

	while anycolliding():
		for i in range(NBALLS):
			if coll[i] != 0xff:
				balls[i].x = (2 + urandom.randrange( 0, 380)) << 4
				balls[i].y = (2 + urandom.randrange( 0, 280)) << 4

def dot( x1, y1, x2, y2 ):
	""" Vectors multiplication ? """
	# Float operation
	return (x1 * x2) + (y1 * y2)

def collide( a, b ):
	""" Collide Ball a with Ball b, compute new velocities. Algorithm from
		http://stackoverflow.com/questions/345838/ball-to-ball-collision-detection-and-handling """

	collision_x, collision_y = 0.0, 0.0

	collision_x = a.x - b.x
	collision_y = a.y - b.y
	distance = sqrt(collision_x * collision_x + collision_y * collision_y)
	rdistance = 1.0 / distance
	collision_x *= rdistance
	collision_y *= rdistance

	aci = dot(a.vx, a.vy, collision_x, collision_y)
	bci = dot(b.vx, b.vy, collision_x, collision_y)
	acf = bci
	bcf = aci
	a.vx += int((acf - aci) * collision_x)
	a.vy += int((acf - aci) * collision_y)
	b.vx += int((bcf - bci) * collision_x)
	b.vy += int((bcf - bci) * collision_y)


# === Setup ====================================================================
print( 'Setup...' )
gd.wr(JK_MODE, 0);

gd.copybin( 'stone_wall_texture_chr.bin', RAM_CHR )
gd.copybin( 'stone_wall_texture_pal.bin', RAM_PAL )
for i in range( 4096 ):
	# Byte value > 255 will be reduced with ''% 256' operation
	gd.wr(RAM_PIC + i, (i & 15) + ((i >> 6) << 4))

gd.copybin( 'sphere_img.bin', RAM_SPRIMG )
gd.copybin( 'sphere_pal.bin', RAM_SPRPAL )

# Place oustide of the visible area
for i in range( 256 ):
	gd.sprite(i, 400, 400, 0, 0, 0)

print( 'Placing balls...' )
place_balls()
# === Loop =====================================================================
LWALL = (0 << 4)
RWALL = (384 << 4)
TWALL = (0 << 4)
BWALL = (284 << 4)

print( 'Colliding...' )
timer = 0
while True:
	plot_balls()

	load_coll()

	# Must stay in the screen area
	for i in range( NBALLS ):
		if balls[i].x <= LWALL:
			balls[i].x = LWALL
			balls[i].vx = -1*balls[i].vx

		if balls[i].x >= RWALL :
			balls[i].x = RWALL
			balls[i].vx = -1*balls[i].vx

		if balls[i].y <= TWALL:
			balls[i].y = TWALL
			balls[i].vy = -1*balls[i].vy

		if balls[i].y >= BWALL:
			balls[i].y = BWALL
			balls[i].vy = -1*balls[i].vy

	for i in range( 1, NBALLS ):
		other = coll[i]
		# only take care of other balls (no extra sprite stored outsite the screen)
		if other >= NBALLS:
			balls[i].lasthit = 0xff
			continue

		if ((balls[i].lasthit != other) and (other != 0xff)):
			collide( balls[i], balls[other] )
		balls[i].lasthit = other

	for i in range( NBALLS ):
		balls[i].x += balls[i].vx
		balls[i].y += balls[i].vy

	timer += 1
	if (timer == 2000):
		print( 'Do it again!' )
		print( 'Placing balls...' )
		place_balls()
		sleep(1)
		timer = 0
		print( 'Colliding...' )

# Finally
print( "That's all folks" )
