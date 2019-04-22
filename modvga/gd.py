"""
Gameduino / MOD-VGA board library for MicroPython.

Based on the GameDuino library @ http://excamera.com/sphinx/gameduino/
See also the Memory Mapping poster reference @ https://excamera.com/files/gameduino/synth/doc/gen/poster.pdf
"""
from time import sleep_ms, sleep_us
import ustruct
__version__ = '0.0.1' #Python version

TRANSPARENT = (1 << 15) # transparent for chars and sprites

RAM_PIC     = 0x0000  # Define screen content. Screen Picture, 64 x 64 = 4096 bytes
RAM_CHR     = 0x1000  # Define characters.     Screen Characters, 256 x 16 = 4096 bytes
RAM_PAL     = 0x2000  # Screen Character Palette, 256 x 8 = 2048 bytes

# --- REGISTERS (general) ---
IDENT       = 0x2800
REV         = 0x2801
FRAME       = 0x2802
VBLANK      = 0x2803
SCROLL_X    = 0x2804
SCROLL_Y    = 0x2806
JK_MODE     = 0x2808
J1_RESET    = 0x2809
SPR_DISABLE = 0x280a
SPR_PAGE    = 0x280b
IOMODE      = 0x280c

BG_COLOR    = 0x280e
SAMPLE_L    = 0x2810
SAMPLE_R    = 0x2812

MODULATOR   = 0x2814
VIDEO_MODE  = 0x2815

MODE_800x600_72  = 0 # Video Mode value
MODE_800x600_60  = 1 # Video Mode value

SCREENSHOT_Y     = 0x281e

# --- REGISTERS (Palette) ---
PALETTE16A = 0x2840   # 16-color palette RAM A, 32 bytes
PALETTE16B = 0x2860   # 16-color palette RAM B, 32 bytes
PALETTE4A  = 0x2880   # 4-color palette RAM A, 8 bytes
PALETTE4B  = 0x2888   # 4-color palette RAM A, 8 bytes
COMM       = 0x2890   # Communication buffer
COLLISION  = 0x2900   # Collision detection RAM, 256 bytes
VOICES     = 0x2a00   # Voice controls
J1_CODE    = 0x2b00   # J1 coprocessor microcode RAM
SCREENSHOT = 0x2c00   # screenshot line RAM

# --- MEMORY MAP (Sprite)
RAM_SPR    = 0x3000   # Sprite Control, 512 x 4 = 2048 bytes
RAM_SPRPAL = 0x3800   # Sprite Palettes, 4 x 256 = 2048 bytes
RAM_SPRIMG = 0x4000   # Sprite Image, 64 x 256 = 16384 bytes

def rgb( r, g, b ):
	return ((((r) >> 3) << 10) | (((g) >> 3) << 5) | ((b) >> 3))

class GDFlashBits():
	"""
	Class used to read bit-by-bit the 'GameDuino data bits' compressed
	in a continuous bit stream
	"""
	def __init__( self ):
		self.src  = None
		self.index= 0 # Index in the source
		self.mask = 0x01

	def begin( self, src ):
		""" src is the source of data, a bytes() type. See cp437 sample. """
		self.src   = src
		self.index = 0 # pointer to the current data byte
		self.mask  = 0x01

	def get1( self ):
		""" Get/Extract next bit from the source """
		r = ((self.src[self.index] & self.mask) != 0)
		r = 1 if r else 0 # Convert True/False to 1/0
		self.mask <<= 1
		if self.mask > 128: # mask is over the 8th bit
			self.mask  = 0x01
			self.index += 1
		#print( 'get1: %s' % (1 if r else 0) )
		return r

	def getn( self, bit_count ):
		""" Get/Extract Nth bits from the source. Can return up to 16bit (unsigned short, 0..65535) """
		r = 0x00
		while bit_count > 0:
			r <<= 1
			r = r | self.get1()
			bit_count -= 1
		#print( 'getn(%s): %s' % (_bit_count, r) )
		return r

class GDFileBits():
	"""
	Class used to read bit-by-bit the 'GameDuino data bits' compressed
	in a continuous BINARY FILE bit stream
	"""
	def __init__( self ):
		self.f    = None # Source file
		self.data = None # A byte read from the source
		self.index= 0 # Index in the source
		self.mask = 0x01

	def begin( self, f ):
		""" f is the source of data, a binary .bin file. """
		self.f     = f
		self.data  = self.f.read( 1 )[0] # read one byte
		self.mask  = 0x01

	def get1( self ):
		""" Get/Extract next bit from the source """
		r = ((self.data & self.mask) != 0)
		r = 1 if r else 0 # Convert True/False to 1/0
		self.mask <<= 1
		if self.mask > 128: # mask is over the 8th bit
			self.mask  = 0x01
			# read next byte (ahead in advance)
			self.data = self.f.read(1)
			if self.data: # But this may be null is we reach the end-of-file
				self.data = self.data[0]
		#print( 'get1: %s' % (1 if r else 0) )
		return r

	def getn( self, bit_count ):
		""" Get/Extract Nth bits from the source. Can return up to 16bit (unsigned short, 0..65535) """
		r = 0x00
		while bit_count > 0:
			r <<= 1
			r = r | self.get1()
			bit_count -= 1
		#print( 'getn(%s): %s' % (_bit_count, r) )
		return r

class Gameduino():
	"""
	Class to control Gameduino / MOD-VGA board.

	Based on the GameDuino library @ http://excamera.com/sphinx/gameduino/
	"""
	# Static GameDuino FlashBits reader
	# GDFBF = GDFlashBits() # should be created on purpose (GDFlashBits or GDFileBits)

	def __init__( self, spi_bus, ssel_pin ):
		""" SPI bus @ 2000000 max for better stability """
		self.spi   = spi_bus # Initialized SPI bus
		self.ssel  = ssel_pin # select pin

		self.spr   = 0 # sprite index

	def begin( self ):
		""" Init the Gameduino """
		self.ssel.value(1) # disable SSEL
		sleep_ms( 400 ) # wait 400ms for initialization

		self.wr( J1_RESET, 1)   # HALT coprocessor

		# Hide all sprites (move them out id the view area)
		self.__wstart(RAM_SPR)  # start Write transaction @ add = RAM_SPR
		for i in range( 512 ):
			self.xhide()
		self.__end()

		self.fill( RAM_PIC   , 0x00, 1024 * 10) # Zero all character RAM
		self.fill( RAM_SPRPAL, 0x00, 2048)      # Sprite palletes black
		self.fill( RAM_SPRIMG, 0x00, 64 * 256)  # Clear all sprite data
		self.fill( VOICES    , 0x0, 256)       # Silence
		self.fill( PALETTE16A, 0x0, 128)       # Black 16-, 4-palletes and COMM

		self.wr16( SCROLL_X   , 0)
		self.wr16( SCROLL_Y   , 0)
		self.wr  ( JK_MODE    , 0)
		self.wr  ( SPR_DISABLE, 0)
		self.wr  ( SPR_PAGE   , 0)
		self.wr  ( IOMODE     , 0)
		self.wr16( BG_COLOR   , 0)
		self.wr16( SAMPLE_L   , 0)
		self.wr16( SAMPLE_R   , 0)
		self.wr16( SCREENSHOT_Y, 0)
		self.wr  ( MODULATOR  , 64)

	def __start( self, addr ):
		""" Start a SPI transaction @ addr """
		# Start new transaction
		self.ssel.value( 1 )
		#sleep_ms( 1 ) # 1 Ms between SPI transaction seems right
		sleep_us( 10 )
		self.ssel.value( 0 )
		self.spi.write( ustruct.pack( '>H', addr) ) # Convert address in MSB and LSB

	def __wstart( self, addr ):
		""" Start a WRITE SPI transation @ addr """
		# Status: Certified!
		self.__start( 0x8000 | addr ) # Write operation are over the address 0x8000

	def __wstartspr( self, sprite_num ):
		""" Start a WRITE SPI transaction for a sprite """
		self.__start( (0x8000 | RAM_SPR) + (sprite_num<<2) )
		self.spr = 0

	def __end( self ):
		""" End of SPI transation """
		pass # self.ssel.value( 1 )

	def rd( self, addr ):
		""" read one byte @ addr """
		# Status: Certified!
		self.__start( addr )
		v = self.spi.read( 1 ) # return b'A'
		self.__end()
		return v[0]

	def wr( self, addr, byte_value ):
		""" write one byte @ addr. Value 0..254 """
		# Status: Certified!
		self.__wstart( addr )
		self.spi.write( bytes([byte_value]) )
		self.__end()

	def rd16( self, addr ):
		""" read a word (16 bits) @ addr """
		# Status: Certified!
		self.__start( addr )
		_bytes = self.spi.read( 2 ) # read 2 bytes
		self.__end()
		return ustruct.unpack( '>H', _bytes )[0] # was initialy '<H' ?

	def wr16( self, addr, word_value ):
		""" write a word (2 bytes) @ addr. Value 0..32768."""
		# Status: Certified!
		self.__wstart( addr )
		self.spi.write( ustruct.pack('<H',word_value) )
		self.__end()

	def fill( self, addr, byte_value, count ):
		""" fill a memory space with a given value """
		# Status: Certified!

		self.__wstart( addr )
		# Consume too much memory !
		#       self.spi.send( bytes([byte_value]*count) )
		# Slower but memory efficient
		data = bytes([byte_value])
		while count > 0:
			self.spi.write( data )
			count -= 1

		self.__end()

	def copy( self, addr, src, count ):
		""" Copy the ressource from arduino header (.h) to addr """
		raise Exception( "use copybin() instead" )

	def copybin( self, f, addr, len = None ):
		""" copy the content of a binary (.bin) file to addr for the whole file (of a part of it.
			:params f: an open FileIO reference to binary file -OR- the filename to open
			:params addr: the address (and following) where the file content should be copied.
			:params len: the len to copy (or whole file if None)
			
			remarks: replace the arduino's copy method. """
		# Status: Certified!
		assert len==None or len <= 256
		# if f is a filename string (instead of a FileIO) --> open it
		if type( f ) is str:
			with open( f, 'rb') as _fbin:
				self.copybin( _fbin, addr, len )
			return

		# Default behavior --> working on file
		chunck = 256 if len==None else len
		self.__wstart( addr )
		r = f.read( chunck )
		while r:
			self.spi.write( r )
			if len:
				return
			r = f.read( chunck )

	def microcode( self, src, count ):
		""" ? what the hell is microcode is doing ? """
		raise Exception( "Not Implemented" )

	def setpal( self, pal, rgb):
		""" Set a RGB value for a palette index """
		# Status: Certified!
		self.wr16(RAM_PAL + (pal << 1), rgb)

	def sprite( self, spr, x, y, image, palette, rot=0, jk=0  ):
		""" int spr, int x, int y, byte image, byte palette, byte rot, byte jk """
		# Status: certified
		self.__wstart( RAM_SPR + (spr << 2) )
		_data = [0,0,0,0]
		_data[0] = x & 255
		_data[1] = (palette << 4) | (rot << 1) | (((x & 65280)>>8) & 1)
		_data[2] = y & 255
		_data[3] = (jk << 7) | (image << 1) | (((y & 65280)>>8) & 1)
		self.spi.write( bytes(_data) )
		self.__end()

	def uncompress( self, addr, src ):
		""" Uncompress data from source and store it @ addr """
		# Status: Certified!
		_class = GDFlashBits if type(src) is bytes else GDFileBits
		gdfbf = _class()
		try:
			gdfbf.begin( src )
			b_off = gdfbf.getn( 4 ) # number of bits to store the data Offset : 4bits
			b_len = gdfbf.getn( 4 ) # number of bits to store the data Length : 4bits
			minlen= gdfbf.getn( 2 ) # Minimum Length (to append to stored data length) : 2bits
			items = gdfbf.getn( 16 )# Number of items

			while items > 0:
				if gdfbf.get1() == 0: # if first bit=0  => 8bits stored
					v = gdfbf.getn(8)
					self.wr( addr, v )
					# Normal Write operation
					addr += 1
				else: # if first bit=1 ==> compressed storage
					# Offset is negative because we will duplicate existing PREVIOUS data
					offset = -1*gdfbf.getn(b_off) - 1
					l      = gdfbf.getn(b_len) + minlen
					# print( 'COPY offset = %s, len = %s' % (offset,l) )
					while l>0 :
						v = self.rd(addr + offset)
						self.wr(addr, v) # offset is negative!!!
						# copy operation
						addr += 1
						l    -= 1
				items -= 1
		finally:
			del( gdfbf )


	def ascii( self , font_color = rgb(255,255,255), fill_char = 32 ):
		""" Initialize a list of ASCII of characters """
		# Status: Certified!
		from font8x8 import font8x8_chr, stretch
		for i in range( 768 ):
			b = font8x8_chr[i]
			h = stretch[b >> 4]
			l = stretch[b & 0xf]
			self.wr(0x1000 + (16 * ord(' ')) + (2 * i), h)
			self.wr(0x1000 + (16 * ord(' ')) + (2 * i) + 1, l)

		for i  in range( 0x20, 0x80 ):
			self.setpal(4 * i + 0, TRANSPARENT);
			self.setpal(4 * i + 3, font_color )

		self.fill(RAM_PIC, fill_char, 4096); # fill with space=32 (or A=65)

	def putstr( self, x, y, a_str ):
		""" Put a string at x,y position on the screen.

		:param x: column from left. 0 indexed. 48 chars on a line.
		:param y: line from top. 0 indexed.
		:param a_str: String to display (will be convert to ASCII)"""
		# Status: Certified
		self.__wstart( 0x0000 + (y << 6) + x )
		self.spi.write( bytes([ord(ch) for ch in a_str]) )

	def xsprite( self, ox, oy, x, y, image, palette, rot, jk=0):
		""" Send sprite data onto SPI bus (bus must already been open in current transaction """
		# int ox, int oy, char x, char y, byte image, byte palette, byte rot, byte jk
		# Status: Certified!
		if rot & 2 :
			x = -16-x
		if rot & 4 :
			y = -16-y
		if rot & 1 :
			x,y = y,x # swap values

		ox += x
		oy += y
		_data = []
		_data.append( ox & 255 ) # SPI.transfer(lowByte(ox));
		_data.append( (palette << 4) | (rot << 1) | ((ox & 65280)>>8) & 1)  # SPI.transfer((palette << 4) | (rot << 1) | (highByte(ox) & 1));
		_data.append( oy & 255 ) # SPI.transfer(lowByte(oy));
		_data.append( (jk << 7) | (image << 1) | (((oy & 65280)>>8) & 1) ) # SPI.transfer((jk << 7) | (image << 1) | (highByte(oy) & 1));
		self.spi.write( bytes(_data) )
		self.spr += 1

	def xhide( self ):
		""" Hide sprite @ memory address (move it out of the display area) """
		# Status: Certified!
		self.spi.write( bytes([1, 144]) ) # Sprite.Y @ 400
		self.spi.write( bytes([1, 144]) ) # Sprite.X @ 400
		self.spr += 1

	def waitvblank( self ):
		""" Wait for the VLANK to go from 0 to 1: this is the start of the vertical blanking interval. """
		# Status: seems OK
		while self.rd(VBLANK) == 1:
			pass
		while self.rd(VBLANK) == 0:
			pass
