"""
 Gameduino MicroPython tool (Pyboard) for Olimex MOD-VGA board.
 Wired using the UEXT pinout proposal @ https://github.com/mchobby/pyboard-driver/tree/master/UEXT

 ramtoh.py for Pyboard reads the RAM_CHR, RAM_PAL, RAM_PIC and
 generates a header file (.h) on the REPL output.

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
# Do not initialize when reading ram state
# gd.begin()

def print_header( name ):
	print( 'static flash_uint8_t %s[] = {' % name )

def print_trailer( ):
	print( '};' )

def print_data( addr, length ):
	_d = []
	for i in range( length ):
		_d.append( gd.rd( addr+i ) )
		if (i % 16) == 15:
			gen = [ hex(s).replace('0x','') for s in _d ]
			print( ''.join( [ '0x%s, '%sHex if len(sHex)>1 else '0x0%s, '%sHex for sHex in gen] ) )
			_d = []
	if len( _d )>0:
		gen = [ hex(s).replace('0x','') for s in _d ]
		print( ''.join( [ '0x%s, '%sHex if len(sHex)>1 else '0x0%s, '%sHex for sHex in gen] ) )

def export_addr( name, addr, length ):
	print_header( name )
	print_data( addr, length )
	print_trailer()

# Export the memory data to console output
export_addr( 'ram_chr', RAM_CHR, 4096 )
export_addr( 'ram_pal', RAM_PAL, 4096 )
export_addr( 'ram_pic', RAM_PIC, 2048 )
