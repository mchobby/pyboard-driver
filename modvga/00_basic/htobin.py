#!/usr/bin/env python3
# coding: utf-8
help = """*** GameDuino .h file compiler ***

Inspect a gameduino h file (eg:01_basic/sprite256/sprites256.h) and creates various binary files from it.
The files contains the data as encoded within the .h file.

The entry like "static flash_uint8_t sprites256_pic[] = {"
in the h file will generates a "sprites256_pic.bin" file.

Usage:
  htobin.py <h_filename>

Options:
  -h --help          This help file.

Made for the Gameduino MicroPython Driver @ https://github.com/mchobby/pyboard-driver/tree/master/modvga
By shop.mchobby.be !
"""

from docopt import docopt
import os
import re

re_array_decl = re.compile( "static\s*\S*\s(\w*)\[\]\s*=\s*{\s*") # extract sprites256_pal from "static flash_uint8_t sprites256_pal[] = {"
re_hex_line   = re.compile( "(0x[0-9a-fA-F][0-9a-fA-F]\s*,\s*)*" ) # Try to match 0xYY hexadecimal series of value
re_hex        = re.compile( "\s*(0x[0-9a-fA-F][0-9a-fA-F])\s*"   ) # Extract 0xFF
re_array_end  = re.compile( "\s*}\s*;\s*" ) # End of array, typically };

def decode_line( s ):
	""" decode a line of '0x00, ...' values and returns an list of int values """
	r = []
	values = s.split(',')
	for value in values:
		m = re_hex.match(value)
		if m:
			r.append( int(m.groups()[0], 16) )
	return r if len(r)>0 else None

def compile_file( f, path ):
	""" Read the f source file and generates bin files in the target path """
	f_target = None # target file created
	w_count  = 0    # Number of bytes written to f_target
	line = f.readline()
	while line:
		#print( line )
		r = re_array_decl.match( line )
		if r: # Great, we have an static flash_uint8_t sprites256_pal[] = ... entry
			if f_target:
				f_target.close()
			# Open the new file
			s_target = os.path.join( path, '%s.bin' % r.groups()[0] )
			print( "Writing %s ..." % os.path.split(s_target)[1] )
			f_target = open( s_target, 'wb' )
			w_count  = 0

		# Read the source --> write content to the target
		line = f.readline()
		m = re_hex_line.match( line ) # Detect line of HEX values
		if m and (m.groups()[0] != None):
			# Great, we have a list of HEX to write to the file :-)
			if not(f_target):
				raise Exception( 'Outch, we have a line of hex values without target file open for %s' % line )
			# Great, lets decode the line and write it to the file
			data = decode_line( line )
			if data:
				w_count += len( data )
				f_target.write( bytes(data) )

		m = re_array_end.match( line )
		if m:
			print( '%i bytes written' % w_count )
			f_target.close()
			f_target = None

	if f_target:
		print( '%i bytes written' % w_count )
		f_target.close()

if __name__ == "__main__":
	arguments = docopt(help)
	path, file = os.path.split( os.path.abspath( arguments['<h_filename>'] ))
	print( 'Openning %s ...' % file )
	# print( path, '-', file )
	with open( arguments['<h_filename>'], 'r' ) as f:
		 compile_file( f, path )
	print( 'Done!' )
