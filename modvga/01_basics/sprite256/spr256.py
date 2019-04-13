"""
 Gameduino MicroPython examples (Pyboard) for Olimex MOD-VGA board.
 Wired using the UEXT pinout proposal @ https://github.com/mchobby/pyboard-driver/tree/master/UEXT

 spr256.py is the porting of sprites256.ino

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

# Structure definition
class Sprite:
	x = 0 # int
	y = 0 # int
	vx = 0 # char. X speed (with sign)
	vy = 0 # char. Y speed (with sign)

sprites = []
for i in range( 256 ):
	sprites.append( Sprite() )

def plot( gd ):
	""" plot the sprites in gameduino """
	for i in range(256):
		# spr, x, y, image, palette, rot, jk
		gd.sprite(i, sprites[i].x >> 4, sprites[i].y >> 4, i % 47, 0, 0)

LWALL = (0 << 4)   # Left Wall
RWALL = (384 << 4) # Right Wall
TWALL = (0 << 4)   # Top Wall
BWALL = (284 << 4) # Bottom Wall

def move():
	""" Move the 256 sprites on the screen between WALLs """
	for sprite in sprites: #  for (i = 256, ps = sprites; i--; ps++) {
		if sprite.x <= LWALL:
			sprite.x = LWALL
			sprite.vx = -1 * sprite.vx
		if sprite.x >= RWALL:
			sprite.x = RWALL
			sprite.vx = -1 * sprite.vx
		if sprite.y <= TWALL:
			sprite.y = TWALL
			sprite.vy = -1 * sprite.vy
		if sprite.y >= BWALL:
			sprite.y = BWALL
			sprite.vy = -1 * sprite.vy

		sprite.x += sprite.vx;
		sprite.y += sprite.vy;

# Gameduino Lib
gd = Gameduino( spi, ss )
gd.begin()

with open( 'sprites256_pic.bin', 'rb' ) as f:
	gd.copybin( f, RAM_PIC )
with open( 'sprites256_chr.bin', 'rb' ) as f:
	gd.copybin( f, RAM_CHR )
with open( 'sprites256_pal.bin', 'rb' ) as f:
	gd.copybin( f, RAM_PAL )
with open( 'pickups2_img.bin', 'rb' ) as f:
	gd.copybin( f, RAM_SPRIMG )
with open( 'pickups2_pal.bin', 'rb' ) as f:
	gd.copybin( f, RAM_SPRPAL )

# randomize the sprites position
for sprite in sprites:
	sprite.x = urandom.randrange( 0, 400 << 4 )
	sprite.y = urandom.randrange( 0, 300 << 4 )
	sprite.vx = urandom.randrange( -16, 16 )
	sprite.vy = urandom.randrange( -16, 16 )

while True:
	plot(gd)
	move()

print( 'That''s all folks')
