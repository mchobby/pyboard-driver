""" MicroPython driver for the DS2482-100, 1Wire Master over I2C.

	Dominique Meurisse for MCHobby.be - initial portage

	Ported from https://github.com/cybergibbons/DS2482_OneWire/blob/master/OneWire.cpp
	Keep same license than initial portage

"""

import time

__author__ = 'Meurisse D.'
__version__ = '0.0.1'
__license__ = 'MIT'

# Chose between a table based CRC (flash expensive, fast) or a computed CRC (smaller, slow)
ONEWIRE_CRC8_TABLE 		=	1

DS2482_COMMAND_RESET	=	0xF0	# Device reset

DS2482_COMMAND_SRP		=	0xE1 	# Set read pointer
DS2482_POINTER_STATUS	=	0xF0
DS2482_STATUS_BUSY		=	(1<<0)
DS2482_STATUS_PPD		=	(1<<1)
DS2482_STATUS_SD		=	(1<<2)
DS2482_STATUS_LL		=	(1<<3)
DS2482_STATUS_RST 		=	(1<<4)
DS2482_STATUS_SBR		=	(1<<5)
DS2482_STATUS_TSB 		=	(1<<6)
DS2482_STATUS_DIR 		=	(1<<7)

DS2482_POINTER_DATA		=	0xE1
DS2482_POINTER_CONFIG	=	0xC3
DS2482_CONFIG_APU		=	(1<<0)
DS2482_CONFIG_SPU		=	(1<<2)
DS2482_CONFIG_1WS		=	(1<<3)

DS2482_COMMAND_WRITECONFIG=	0xD2
DS2482_COMMAND_RESETWIRE=	0xB4
DS2482_COMMAND_WRITEBYTE=	0xA5
DS2482_COMMAND_READBYTE	=	0x96
DS2482_COMMAND_SINGLEBIT=	0x87
DS2482_COMMAND_TRIPLET	=	0x78

WIRE_COMMAND_SKIP		=	0xCC
WIRE_COMMAND_SELECT		=	0x55
WIRE_COMMAND_SEARCH		=	0xF0

DS2482_ERROR_TIMEOUT	=	(1<<0)
DS2482_ERROR_SHORT		=	(1<<1)
DS2482_ERROR_CONFIG		=	(1<<2)

class DS2482:
	""" Driver for DS2482 : OneWire Master over I2C """
	def __init__( self, i2c, address = 0x18 ):
		self.i2c = i2c
		self.address = address
		self.merror = 0

		# Used by searchwire_search
		self.search_address = [None,None,None,None,None,None,None,None] # uint8[8]
		self.searchLastDiscrepancy = None
		self.searchLastDeviceFlag = None
		self.wire_reset_search()

		# Pre-allocate buffer for sending data
		self._data_byte = bytearray( 1 )
		self._data_2bytes=bytearray( 2 )

	@property
	def error( self ):
		return self.merror

	def check_presence( self ):
		# Try to read the Status register
		# Will raise an OSError exception with ENODEV if device is not present
		data = self.i2c.readfrom_mem( self.address, DS2482_POINTER_STATUS, 1 )
		return True

	def set_read_pointer( self, target ):
		# Sets the read pointer to the specified register. Overwrites the read pointer position of any 1-Wire communication command in progress.
		self.i2c.writeto( self.address, bytes([DS2482_COMMAND_SRP,target]) )
		return self.i2c.readfrom( self.address, 1 )[0] # Read one byte

	def write_config( self, config ):
		# Write to the config register
		data = bytes( [DS2482_COMMAND_WRITECONFIG, (config | (0x0F ^ config)<<4) ] )

		self.wait_on_busy()
		# writeByte(DS2482_COMMAND_WRITECONFIG);
		# Write the 4 bits and the complement 4 bits
		# writeByte(config | (~config)<<4)
		self.i2c.writeto( self.address, data )

		# This should return the config bits without the complement
		data = self.i2c.readfrom( self.address, 1 )[0] # Read one byte
		if (data != config):
			self.mError = DS2482_ERROR_CONFIG

	def read_byte_from( self, ds2482_pointer ):
		self.set_read_pointer( ds2482_pointer ) # DS2482_POINTER_CONFIG, DS2482_POINTER_DATA, DS2482_POINTER_STATUS
		self.i2c.readfrom_into( self.address, self._data_byte ) # Read One byte
		return self._data_byte[0]

	def read_config( self ):
		# Read the config register
		#self.set_read_pointer( DS2482_POINTER_CONFIG )
		#return self.i2c.readfrom( self.address, 1 )[0] # Read one byte
		return self.read_byte_from( DS2482_POINTER_CONFIG )

	def read_data( self ):
		# Read the data register
		#self.set_read_pointer (DS2482_POINTER_DATA )
		#return self.i2c.readfrom( self.address, 1 )[0] # Read one byte
		return self.read_byte_from( DS2482_POINTER_DATA )

	def read_status( self ):
		#self.set_read_pointer( DS2482_POINTER_STATUS )
		#return self.i2c.readfrom( self.address, 1 )[0] # Read one byte
		return self.read_byte_from( DS2482_POINTER_STATUS )

	def device_reset( self ):
		self._data_byte[0] = DS2482_COMMAND_RESET
		#self.i2c.writeto( self.address, bytes([DS2482_COMMAND_RESET]) )
		self.i2c.writeto( self.address,self._data_byte )

	def wire_reset( self ):
		self.wait_on_busy()
		# Datasheet warns that reset with SPU set can exceed max ratings
		self.clear_strong_pullup()
		self.wait_on_busy()
		#self.i2c.writeto( self.address, bytes([DS2482_COMMAND_RESETWIRE]) )
		self._data_byte[0] = DS2482_COMMAND_RESETWIRE
		self.i2c.writeto( self.address,self._data_byte )
		status = self.wait_on_busy()
		print( "wire_reset: status= %s" % (status) )
		if ((status & DS2482_STATUS_SD) == DS2482_STATUS_SD):
			self.mError = DS2482_ERROR_SHORT
		return ((status & DS2482_STATUS_PPD)==DS2482_STATUS_PPD )

	def clear_strong_pullup( self ):
		data = self.read_config()
		self.write_config( data & (0xFF ^ DS2482_CONFIG_SPU) )

	def wait_on_busy( self ):
		# Wait for 1Wire bus not being busy
		status = 0

		i=1000
		while i>0 :
			status = self.read_status()
			if not( (status & DS2482_STATUS_BUSY)==DS2482_STATUS_BUSY ):
				print( "returned 0 Status: %r" % status )
				return status
			time.sleep_us(20)
			i -= 1

		if( (status & DS2482_STATUS_BUSY)==DS2482_STATUS_BUSY ):
			self.mError = DS2482_ERROR_TIMEOUT
		# Return the status so we don t need to explicitly do it again
		print( "returned 1 Status: %r" % status )
		return status

	def wire_reset_search( self ):
		self.searchLastDiscrepancy = 0
		self.searchLastDeviceFlag  = 0

		for i in range(8):
			self.searchAddress[i] = 0


	def wire_search( self ):
		""" Return an address on 8 position or None """
		direction = None
		last_zero = 0

		if self.searchLastDeviceFlag:
			return None

		if not self.wire_reset():
			return None

		self.wait_on_busy()

		self.wire_write_byte( WIRE_COMMAND_SEARCH )

		for i in range(64):
			searchByte = i // 8
			searchBit = 1 << i % 8

			if i < self.searchLastDiscrepancy:
				direction = (self.searchAddress[searchByte] & searchBit) == searchBit
			else
				direction = (i == self.searchLastDiscrepancy)

			self.wait_on_busy()
			self._data_2bytes[0] = DS2482_COMMAND_TRIPLET
			self._data_2bytes[1] = 0x80 if direction else 0x00
			#writeByte(DS2482_COMMAND_TRIPLET);
			#writeByte(direction ? 0x80 : 0x00);
			self.i2c.writeto( self.address, self._data_2bytes )

			status = wait_on_busy()

			id = status & DS2482_STATUS_SBR
			comp_id = status & DS2482_STATUS_TSB
			direction = status & DS2482_STATUS_DIR

			if (id>0 and comp_id>0):  # id && comp_id
				return None
			else:
				if (id==0 and comp_id==0 and not(direction) ): # !id && !comp_id && !direction
					last_zero = i


			if direction:
				self.searchAddress[searchByte] = self.searchAddress[searchByte] | searchBit
			else:
				self.searchAddress[searchByte] = self.searchAddress[searchByte] & (0xFF^searchBit)

		self.searchLastDiscrepancy = last_zero

		if last_zero==0: # !last_zero
			self.searchLastDeviceFlag = 1

		# Return a copy of the list
		return list( self.searchAddress )
