""""
 Gameduino MicroPython examples (Pyboard) for Olimex MOD-VGA board.
 Wired using the UEXT pinout proposal @ https://github.com/mchobby/pyboard-driver/tree/master/UEXT

 chess.py is the porting of chessboard.ino

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
from math import sqrt

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

f_woodpic = open( 'Wood32_pic.bin', 'rb' )

# === Toolbox ==================================================================
QROOK   =  0
QKNIGHT =  1
QBISHOP =  2
QUEEN   = 3
KING    = 4
KBISHOP = 5
KKNIGHT = 6
KROOK   = 7
PAWN    = 8
WHITE   = 0x00
BLACK   = 0x10

board = []
for i in range(32):
	board.append( 0 )

def startboard():
	global board
	for i in range(8):
		board[i] = 56+i
		board[8+i] = 48+i
		board[16+i] = i
		board[24+i] = 8+i

def find( pos ):
	# Return the piece at pos, or -1 if pos is empty
	global board
	for slot in range( 32 ):
		if board[slot] == pos:
			return slot
	return -1

images = [ 0, 1, 2, 3, 4, 2, 1, 0, 5, 5, 5, 5, 5, 5, 5, 5 ]

def piece( slot, x, y ):
	""" Place a piece (sprite) on the board """
	#print( 'piece x,y = %s, %s' % (x,y) )
	global images
	i = (4 * slot)
	j = images[slot & 0xf] * 2
	bw = (slot >> 4) & 1
	gd.sprite(i, x, y, j, bw, 0)
	gd.sprite(i + 1, x + 16, y, j + 1, bw, 0)
	gd.sprite(i + 2, x, y + 16, j + 12, bw, 0)
	gd.sprite(i + 3, x + 16, y + 16, j + 13, bw, 0)

def board_x( pos ):
	return (8 + (((pos) & 7) << 5))

def board_y( pos ):
	return (24 + ((((pos) >> 3) & 7) << 5))

def drawboard():
	for slot in range( 32 ):
		pos = board[slot]
		if (pos < 0):
			piece(slot, 400, 400)
		else:
			piece(slot, board_x(pos), board_y(pos))

def smoothstep( x ):
	""" x - float """
	return x*x*(3-2*x)

def movepiece( slot, pos ):
	""" move piece 'slot' to position 'pos'. Return true if a piece was taken. """
	global board
	x0 = board_x(board[slot])
	y0 = board_y(board[slot])
	x1 = board_x(pos)
	y1 = board_y(pos)
	# move at 1.5 pix/frame
	d = int(sqrt(pow(x0 - x1, 2) + pow(y0 - y1, 2)) / 2);
	for it in range( d ):
		t = smoothstep( it / d ) # float
		gd.waitvblank()
		gd.waitvblank()
		piece(slot, int(x0 + t * (x1 - x0)), int(y0 + t * (y1 - y0)))
	taken = (find(pos) != -1)
	if (taken):
		board[find(pos)] = -1
	board[slot] = pos
	drawboard()
	return taken

def digits():
	return 24 # (sizeof(staunton_img) / 256) = 6144 / 256 = 24

def atxy( x, y ):
  return (y << 6) + x

def square( x, y, light ):
	src = 16 * light # Wood32_pic
	addr = atxy(x, y)
	f_woodpic.seek( src )
	gd.copybin( f_woodpic, addr + 0 * 64, 4)
	gd.copybin( f_woodpic, addr + 1 * 64, 4);
	gd.copybin( f_woodpic, addr + 2 * 64, 4);
	gd.copybin( f_woodpic, addr + 3 * 64, 4);

clock = [0, 0] # int

def digit( spr, d, bw, x, y ):
	""" draw digit d in sprite slots spr,spr+1 at (x,y) """
	# byte spr, byte d, byte bw, int x, int y)
	gd.sprite(spr, x, y, digits() + d, 2 + bw, 0)
	gd.sprite(spr + 1, x, y + 16, digits() + d + 11, 2 + bw, 0)

def showclock( bw ):
	# Show the clock for Black or White (0 or 1)
	#
	# remarks: X position have been decrease from 400 to 380
	global clock
	t = clock[bw]
	spr = 128 + (bw * 16)
	s = t % 60
	y = (31 if bw>0 else 3) * 8
	d0 = s % 10
	s /= 10
	digit(spr,         d0, bw, 380 - 1 * 16, y)
	digit(spr + 2, int(s), bw, 380 - 2 * 16, y)

	digit(spr + 4,  10, bw, 380 - 3 * 16, y) # colon
	spr += 6
	x = 380 - 4 * 16 # 400

	m = t / 60
	while True:
		d0 = int(m) % 10
		m /= 10
		digit(spr,  d0, bw, x, y)
		spr += 2
		x -= 16
		if m<1:
			break

turn = 0

def alg( r, f ):
	return ( (ord(r) - ord('a')) + ((8 - f) * 8))

# CASTLE = 255,255
game = [ alg('e', 2),alg('e', 4), alg('e', 7),alg('e', 5),
  alg('g', 1),alg('f', 3), alg('b', 8),alg('c', 6),
  alg('f', 1),alg('b', 5), alg('a', 7),alg('a', 6),
  alg('b', 5),alg('a', 4), alg('g', 8),alg('f', 6),
  alg('d', 1),alg('e', 2), alg('b', 7),alg('b', 5),
  alg('a', 4),alg('b', 3), alg('f', 8),alg('e', 7),
  alg('c', 2),alg('c', 3), 255        , 255,
  255        ,255        , alg('d', 7),alg('d', 5),
  alg('e', 4),alg('d', 5), alg('f', 6),alg('d', 5),
  alg('f', 3),alg('e', 5), alg('d', 5),alg('f', 4),
  alg('e', 2),alg('e', 4), alg('c', 6),alg('e', 5),
  alg('e', 4),alg('a', 8), alg('d', 8),alg('d', 3),
  alg('b', 3),alg('d', 1), alg('c', 8),alg('h', 3),
  alg('a', 8),alg('a', 6), alg('h', 3),alg('g', 2),
  alg('f', 1),alg('e', 1), alg('d', 3),alg('f', 3) ]

def putalg( x, y, a ):
	gd.wr(atxy(x, y), ord('a') + (a & 7))
	gd.wr(atxy(x+1, y), ord('8') - ((a >> 3) & 7))


# === Setup ====================================================================
print( 'ascii init...' )
gd.ascii();
gd.putstr(0, 0, "Chess board");
print( 'charging ressource...' )
gd.copybin( 'Wood32_chr.bin'    , RAM_CHR )
gd.copybin( 'Wood32_pal.bin'    , RAM_PAL )
gd.copybin( 'staunton_img.bin'  , RAM_SPRIMG )
gd.copybin( 'staunton_white.bin', RAM_SPRPAL )
gd.copybin( 'staunton_black.bin', RAM_SPRPAL + 512 )

gd.copybin( 'digits_img.bin', RAM_SPRIMG + (digits() << 8) )
gd.copybin( 'digits_pal.bin', RAM_SPRPAL + 2 * 512       )
for i in range( 256 ):
	b = gd.rd16(RAM_SPRPAL + 2 * 512 + 2 * i) # unsigned int
	gd.wr16( RAM_SPRPAL + 3 * 512 + 2 * i, b ^ 0x7fff )

print( 'Drawing board...' )
#Draw the 64 squares of the board
for i in range( 8 ):
	for j in range( 8 ):
		square(1 + (i << 2), 3 + (j << 2), (i ^ j) & 1)
# Done with square... so we can release the ressource
f_woodpic.close()

# Draw the rank and file markers 1-8 a-h
for i in range( 8 ):
	gd.wr(atxy(3 + (i << 2), 2) , ord('a') + i)
	gd.wr(atxy(3 + (i << 2), 35), ord('a') + i)
	gd.wr(atxy(0, 5 + (i << 2)) , ord('8') - i)
	gd.wr(atxy(33, 5 + (i << 2)), ord('8') - i)

print( 'Starting board...')
startboard()
drawboard()

# === Loop =====================================================================
while True:
	# Random pause
	iRand    = urandom.randrange(25)
	idxClock = (1 & turn) ^ 1 # select the right clock to update (1 or 0)
	for i in range( iRand ):
		clock[ idxClock ] = clock[ idxClock ] + 1
		gd.waitvblank()
		showclock(0)
		showclock(1)
		sleep_ms(100) # Increase time from 20ms to 100ms

	if (turn < (len(game) / 2)):
		yy = 8 + (turn >> 1);
		xx =  44 if (turn & 1) else 38
		i = 1 + (turn >> 1)
		if (i >= 10):
			gd.wr(atxy(35, yy), int(ord('0') + i / 10) )
		gd.wr(atxy(36, yy), ord('0') + i % 10)
		gd.wr(atxy(37, yy), ord('.'))

		_from = game[2 * turn]
		_to = game[2 * turn + 1]
		if (_from != 255):
			putalg(xx, yy, _from)
			gd.wr( atxy(xx + 2, yy), ord('x') if movepiece(find(_from), _to) else ord('-') )
			putalg(xx + 3, yy, _to)
		else:
			rank = 8 if (turn & 1) else 1
			movepiece(find(alg('e', rank)), alg('g', rank))
			movepiece(find(alg('h', rank)), alg('f', rank))
			gd.putstr(xx, yy, "O-O")
		turn += 1
	else:
		break;
		#sleep(4)
		#setup()
		#turn = 0
		#clock[0] = 0
		#clock[1] = 0

# Finally
print( "That's all folks" )
