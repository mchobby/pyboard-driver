"""
unoextra.py - Pyboard-UNO-R3 extra miscellaneous features like OLED and charger.

* Author(s): Meurisse D. from MCHobby (shop.mchobby.be).

See project source @ https://github.com/mchobby/pyboard-driver/tree/master/UNO-R3

"""
#
# The MIT License (MIT)
#
# Copyright (c) 2019 Meurisse D. for MC Hobby
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

__version__ = "0.0.1"

from machine import I2C, Pin
from ssd1306 import SSD1306_I2C
from math import ceil

__i2c = None
def get_i2c():
	""" Retreive reference to the software I2C bus for extra features (OLED,Charger,...)"""
	global __i2c
	if not(__i2c):
		__i2c = I2C( sda=Pin("Y4"), scl=Pin("Y3") )
	return __i2c

# --- OLED ---------------------------------------------------------------------
LINE_HEIGHT = 10 # Height of a character line (in pixels)

class Point():
	__slot__ = ['x','y']

	def set(self, xy ):
		self.x = xy[0]
		self.y = xy[1]

	def get( self ):
		return self.x, self.y

	def __repr__(self):
		return "<%s %i,%i>" % (self.__class__.__name__, self.x, self.y )

class Unoled( SSD1306_I2C ):
	""" Inherit of FrameBuffer drawing functions. see following link for examples:
		https://wiki.mchobby.be/index.php?title=FEATHER-MICROPYTHON-OLED#Tester_la_biblioth.C3.A8que

		font-size is 8x8
	"""
	def __init__(self):
		super().__init__( 128,64,get_i2c() )
		self.__cursor = Point()
		self.clear()

	def clear(self):
		self.fill(0)
		self.show()
		self.__cursor.set( (0,0) ) # Inner text position (top,left - in pixel)

	def cursor( self ):
		""" Return the (line,col) position (0 based) of the cursor in characters """
		x,y = self.__cursor.get()
		return y//LINE_HEIGHT, x//8 # Line, Column

	def set_cursor( self, line_col ):
		""" set the cursor position with (line, col) tuple. 0 based value """
		self.__cursor.x = line_col[1]*8
		self.__cursor.y = line_col[0]*LINE_HEIGHT

	def println( self, text, wrap=False ):
		""" Print a line and scroll the screen if necessary (before drawing the text)"""
		if wrap:
			if self.__cursor.x != 0:
				raise Exception('Cursor must be at column 0')
			_chars_per_line = self.width//8
			for i in range( ceil(len(text)/_chars_per_line) ):
				self.println( text[i*_chars_per_line:(i+1)*_chars_per_line]  )
			return # not going further

		# Do we have to vertical scroll before we display text?
		if self.__cursor.y + LINE_HEIGHT > self.height:
			self.scroll(0, -1*LINE_HEIGHT) # Scroll content UP
			self.fill_rect(0,self.__cursor.y-1*LINE_HEIGHT,self.width, self.height-(self.__cursor.y-1*LINE_HEIGHT),0) # Clean up before drawing next text
			self.__cursor.y -= LINE_HEIGHT
		# clear the zone under drawing text
		self.fill_rect( self.__cursor.x,self.__cursor.y, len(text)*8, LINE_HEIGHT, 0 )
		self.text(text, self.__cursor.x,self.__cursor.y, 1)
		self.__cursor.y += LINE_HEIGHT
		self.__cursor.x = 0
		self.show()

	def print( self, text ):
		""" Just print on the same line """
		self.fill_rect( self.__cursor.x,self.__cursor.y, len(text)*8, LINE_HEIGHT, 0 )
		self.text( text, self.__cursor.x,self.__cursor.y, 1 )
		self.__cursor.x += len(text)*8
		self.show()
