"""
 Gameduino MicroPython examples (ESP8266-EVB) for Olimex MOD-VGA board.

 READ IDCODE FROM GAMEDUINO

 based on porting reference for GameDuino @ http://excamera.com/sphinx/gameduino/

Where to buy:
* MOD-VGA: https://shop.mchobby.be/uext/1431-mod-vga-33v-gameduino-alike-board-3232100014312-olimex.html
* MOD-VGA: https://www.olimex.com/Products/Modules/Video/MOD-VGA/open-source-hardware
* Pyboard: https://shop.mchobby.be/esp8266-esp32-wifi-iot/668-module-wifi-esp8266-carte-d-evaluation-3232100006683-olimex.html

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
from time import sleep_ms

# UEXT wiring on the Pyboard.
# https://github.com/mchobby/pyboard-driver/tree/master/UEXT
spi = SPI(2) # MOSI=Y8, MISO=Y7, SCK=Y6, SS=Y5
spi.init( baudrate=5000000, phase=0, polarity=0 )
# We must manage the SS signal ourself
ss = Pin( Pin.board.Y5, Pin.OUT )
ss.value( 1 )
sleep_ms( 10 ) # Wait 10ms before new transaction!

# Start a new SPI transaction
ss.value( 0 )

print( "Read IDCode from GameDuino (0x6d expected)" )
spi.write( bytes([0x28,0x00]) )

buf = spi.read( 1 ) # read 1 byte

print( "Response:" )
print( buf ) # bytes
print( "0x%02x" % buf[0] ) # print as Hexa
