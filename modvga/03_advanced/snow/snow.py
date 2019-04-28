""""
 Gameduino MicroPython examples (Pyboard) for Olimex MOD-VGA board.
 Wired using the UEXT pinout proposal @ https://github.com/mchobby/pyboard-driver/tree/master/UEXT

 snow.py is the porting of snow.ino

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

# os.chdir( '/sd' )

# === Toolbox ==================================================================
# readn() has been added to the gameduino library
# void readn(byte *dst, unsigned int addr, int c)

# Ported from random.h - MicroCode for the VGA controler
random_code = [ 0x81,0x15,
	0x00,0x80,
	0xED,0xFF,
	0x00,0x66,
	0x00,0x60,
	0x00,0x6C,
	0x81,0x61,
	0x23,0x60,
	0x03,0x61,
	0x00,0x6A,
	0xFF,0x9F,
	0x03,0x63,
	0x82,0x15,
	0x0C,0x70
	]

# === Setup ====================================================================
print( 'Setup...' )

# gd.copybin( 'stone_wall_texture_chr.bin', RAM_CHR )
for i in range( 256 ):
	gd.wr16( RAM_PAL + (4 * i + 0) * 2, rgb(0,0,0))
	gd.wr16( RAM_PAL + (4 * i + 1) * 2, rgb(0x20,0x20,0x20))
	gd.wr16( RAM_PAL + (4 * i + 2) * 2, rgb(0x40,0x40,0x40))
	gd.wr16( RAM_PAL + (4 * i + 3) * 2, rgb(0xff,0xff,0xff))

# Inform the VGA controler of the code to execute
gd.microcode( random_code )

# === Loop =====================================================================
print( 'MicroCode will run standalone on the co-processor')

# Finally
print( "That's all folks" )
