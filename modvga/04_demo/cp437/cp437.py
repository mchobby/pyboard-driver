"""
 Gameduino MicroPython examples (Pyboard) for Olimex MOD-VGA board.
 Wired using the UEXT pinout proposal @ https://github.com/mchobby/pyboard-driver/tree/master/UEXT

 GAMEDUINO Code Page demo

 Using this tool font, every charaters is coded on 2x(8x8 pixels). So instead of
 ascii.py (8x8 pixels fonts), we have a 16x8 pixels font. As a result, a custom
 drawstr() method must be used.


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
import gc
from machine import Pin, SPI
from codepage import cp437_chr, cp437_pal, cp437_pic
from gd import Gameduino, RAM_CHR, RAM_PAL


# See the Gameduino General test for all MicroPython plateform support
spi = SPI(2) # MOSI=Y8, MISO=Y7, SCK=Y6, SS=Y5
spi.init( baudrate=2000000, phase=0, polarity=0 )
# We must manage the SS signal ourself
ss = Pin( Pin.board.Y5, Pin.OUT )

# Gameduino Lib
gd = Gameduino( spi, ss )
print( "Initializing...")
gd.begin()
print( "Uncompressing to RAM_CHR")
gd.uncompress( RAM_CHR, cp437_chr )
print( "Uncompressing to RAM_PAL")
gd.uncompress( RAM_PAL, cp437_pal )


def atxy( x, y ):
	""" Memory offset corresponding to a cursor position """
	return (y<<7)+x

def drawstr( addr, s ):
	""" Draw a string at a given position. use atxy() to calculate address """
	for idx in range( len(s) ):
		ch = ord( s[idx] ) # Ordinal value of char. A --> 65
		# RAM_CHR (char pictt) OFFSET to read. A=65 --> offset = 115!
		offset = cp437_pic[ ch*2 ] # Char picture is available @ 115 & 116
		gd.wr( addr    , cp437_pic[ ch*2 ] ) # 8x8 upper pixels GD.wr(addr, lowByte(w));
		gd.wr( addr+64 , cp437_pic[ (ch*2)+1 ] ) # 8x8 lower pixels GD.wr(addr + 64, highByte(w));
		#print( '%s : %s' % (addr, byte1) )
		#print( '%s : %s' % (addr+64, byte2) )
		addr += 1

print( "Drawing strings")
drawstr( atxy(5, 0), "  *** DEMOs ***" )
drawstr( atxy(5, 1), " 04_demo/cp437/cp437.py " )
drawstr( atxy(5, 3), "This is the cp437 font");
drawstr( atxy(5, 4), "ABCDEFGHIJKLMNOPQRSTUVWXYZ" )
drawstr( atxy(5, 5), "abcdefghijklmnopqrstuvwxyz" )
drawstr( atxy(5, 6), "1234567890" )

# Display all the available chars on the screen
print( "Display charmap" )
drawstr( atxy(0,9), "  = Character Map from chr(0) to chr(127) =" )
ORD_MAX = 127 # chr(127) is the last character we can have with cp437
for idx in range(ORD_MAX+1):
	x = idx % 47
	y = idx // 47
	drawstr( atxy(x,y+11), chr(idx) )

# read and dump the char map
print( "Dumping RAM_CHR")
addr = RAM_CHR
for ichar in range( 0, 255 ):
	print( '--(%3s)%s' % (ichar,'-'*20) )
	for iRow in range( 8 ):
		r = gd.rd16( addr+ ichar*16 + iRow*2)
		l = []
		for iShift in range( 8 ):
			mask = 0b11 << (2*iShift)
			val  = (r & mask) >> (2*iShift) # Should be 0..3
			l.append( str(val) if val>0 else '.' )
		# Address - Value
		print( '0x%x : %s' % (addr+ ichar*16 + iRow*2, "".join(l)) )

print( "that's the end Folks")
