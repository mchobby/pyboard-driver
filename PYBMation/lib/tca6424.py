"""  Micropython driver for I2C GPIO Expander TCA6424

	The 24 bits are distributed between Port P0 (P01 to P07), P1 (P10 to P17),
	P2 (P20 to P27).

	The driver use a continuous numbering from 0 to 23"""
from machine import Pin

INPUT_P0 = 0x00
INPUT_P1 = 0x00+1
INPUT_P2 = 0x00+2

OUTPUT_P0  = 0x04
OUTPUT_P1  = 0x04+1
OUTPUT_P2  = 0x04+2

POLINV_P0 = 0x08
POLINV_P1 = 0x08+1
POLINV_P2 = 0x08+2

CONFIG_P0 = 0x0C
CONFIG_P1 = 0x0C + 1
CONFIG_P2 = 0x0C + 2

AUTOINCR_ON  = 0x80
AUTOINCR_OFF = 0x00

class TCA6424:
	""" Manage the I2C 24 bits GPIO expander """

	def __init__(self, i2c, addr=0x23):
		self.i2c = i2c
		self.addr = addr

		self.config = [0xFF,0xFF,0xFF] # Config port P0, P1, P2
		self.inputs = [0x00,0x00,0x00] # Last pin state readed from TCA
		self.pols   = [0x00,0x00,0x00] # Invert input polarity on TCA
		self.outputs= [0x00,0x00,0x00] # Last pin state written to TCA
		self.buf1   = bytearray(1)

	def validate( self, pin ):
		if 0 <= pin <= 23:
			return True
		raise EValueError( 'Invalid %s pin number' % pin )

	def setup( self, pin, mode=None, inversion=False, value=None ):
		""" Define the mode Pin.IN/OUT for a pin 0..23 (P0..7 + P10..7 + P20..27).
			Inversion allows to do a polarity inversion for Input and output.
			value can old initial pin value for OUT pin."""
		assert mode in (Pin.IN, Pin.OUT, None)
		self.validate( pin )
		reg_offset = pin//8
		bit_offset = pin%8

		if mode == None:
			# Return the current Pin configuration
			if ( self.config[reg_offset] & (1<<bit_offset) ) >0 :
				return Pin.IN
			else:
				return Pin.OUT
		elif mode == Pin.IN:
			# Change the Pin configuration to INPUT
			self.config[reg_offset] |= (1<<bit_offset)            # Activate bit
		else:
			# Change the Pin configuration to OUTPUT
			self.config[reg_offset] &= (0xFF^(1<<bit_offset))    # Deactivate bit

		if inversion:
			self.pols[reg_offset] |= (1<<bit_offset)
		else:
			self.pols[reg_offset]  &= (0xFF^(1<<bit_offset))

		if (value!=None) and (mode==Pin.OUT):
			# Initial Pin Value (for output only)
			if inversion:
				value = not(value)
			if value:
				self.outputs[reg_offset] |= (1<<bit_offset) # set the bit
			else:
				self.outputs[reg_offset] &= 0xFF ^ (1<<bit_offset) # clear the bit

	def apply_setup( self ):
		""" Send the Pin Setup in one operation """
		# Initial pin states
		for reg_offset in range(3):
			self.buf1[0] = self.outputs[reg_offset]
			self.i2c.writeto_mem( self.addr, OUTPUT_P0+reg_offset, self.buf1 )

		# Inversion is handled on the TCA for INPUT only
		# Output inversion MUST be managed by the driver
		for reg_offset in range(3):
			self.buf1[0] = self.config[reg_offset]
			self.i2c.writeto_mem( self.addr, CONFIG_P0+reg_offset, self.buf1 )

			self.buf1[0] = self.pols[reg_offset]
			self.i2c.writeto_mem( self.addr, POLINV_P0+reg_offset, self.buf1 )

	def input( self, pin, refresh=True ):
		""" read the input value from the TCA then returns it.
			With refresh=False will not force TCA reading """
		self.validate( pin )
		if self.setup(pin) != Pin.IN:
			raise Exception( 'Pin %s is not in input' % pin )
		reg_offset = pin//8
		bit_offset = pin%8

		if refresh:
			self.i2c.readfrom_mem_into( self.addr, INPUT_P0+reg_offset, self.buf1 )
			self.inputs[reg_offset] = self.buf1[0]

		return ( self.inputs[reg_offset] & (1<<bit_offset) )>0

	def all_inputs( self ):
		""" Read all entries @ once """
		for reg_offset in range(3):
			self.i2c.readfrom_mem_into( self.addr, INPUT_P0+reg_offset, self.buf1 )
			self.inputs[reg_offset] = self.buf1[0]

	def output( self, pin, value=None, refresh=False ):
		""" Write or read the output value of the TCA then returns it.
			With refresh=True will not force re-reading from the TCA """
		self.validate( pin )
		if self.setup(pin) != Pin.OUT:
			raise Exception( 'Pin %s is not in output' % pin )
		reg_offset = pin//8
		bit_offset = pin%8

		# Force the ourpt status re-read
		if refresh:
			self.i2c.readfrom_mem_into( self.addr, OUTPUT_P0+reg_offset, self.buf1 )
			self.outputs[reg_offset] = self.buf1[0]

		# Manage Inversion flag for output
		inversion = (self.pols[reg_offset] & (0xFF^(1<<bit_offset))) > 0

		# Return the current output state ?
		if value==None :
			val = ( self.outputs[reg_offset] & (1<<bit_offset) )>0
			return val if not inversion else not(val) # manage inversion

		# Update the state (manage inversion)
		if inversion:
			value = not(value)
		if value:
			self.outputs[reg_offset] |= (1<<bit_offset) # set the bit
		else:
			self.outputs[reg_offset] &= 0xFF ^ (1<<bit_offset) # clear the bit
		self.buf1[0] = self.outputs[reg_offset]
		self.i2c.writeto_mem( self.addr, OUTPUT_P0+reg_offset, self.buf1 )
