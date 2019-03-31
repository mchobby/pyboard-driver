"""
 Gameduino MicroPython examples (Pyboard) for Olimex MOD-VGA board.
 Wired using the UEXT pinout proposal @ https://github.com/mchobby/pyboard-driver/tree/master/UEXT

 GAMEDUINO ASCII DUMP demo

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
from gd import Gameduino, RAM_CHR, RAM_PAL

# Initialize the SPI Bus (on Pyboard)
spi = SPI(2) # MOSI=Y8, MISO=Y7, SCK=Y6, SS=Y5
spi.init( SPI.MASTER, baudrate=2000000, phase=0, polarity=0 )
# We must manage the SS signal ourself
sel = Pin( Pin.board.Y5, Pin.OUT )

# Gameduino Lib
gd = Gameduino( spi, sel )
print( "Initializing...")
gd.begin()
print( "Initializing ASCII...")
gd.ascii()

# Print a string
gd.putstr( 5 ,  0, "  *** DEMOs ***" )
gd.putstr( 5 ,  1, "04_demo/ascii/dump.py" )
gd.putstr( 10, 10, "MicroPython goes VGA !" )

print( 'read and dump the char map' )
base_addr = RAM_CHR
for ichar in range( 0x20, 0x80 ):
	print( '--(%3s)%s' % (ichar,'-'*20) )
	for iRow in range( 8 ):
		addr = base_addr+ ichar*16 + iRow*2
		r = gd.rd16( addr )
		print ( '%s : %s' %(addr, '0b'+('%16s'%bin(r).replace('0b','').replace('0','.')).replace(' ','.') ))
#        continue
#        l = []
#        for iShift in range( 8 ):
#            mask = 0b11 << (2*iShift)
#            val  = (r & mask) >> (2*iShift) # Should be 0..3
#            l.append( str(val) if val>0 else ' ' )
#        print( ",".join(l) )

print( "that's the end Folks")
