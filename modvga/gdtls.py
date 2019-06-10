""""
  Additional MicroPython toolbox for Gameduino / MOD-VGA board .

  Content of this file where created to support the Gameduino arduino code portage to MicroPython.

Based on the GameDuino library @ http://excamera.com/sphinx/gameduino/
See also the Memory Mapping poster reference @ https://excamera.com/files/gameduino/synth/doc/gen/poster.pdf
"""

import re

class HLoader():
	""" Load ressource from an C Header file (.h) on the fly.
	    Note: don't try to load too much data with it, it consume RAM. Consider .bin file loading first.

		Based on structure of of 03_advanced/wireframe/eliteships.h .
		Must stricly follow the declaration of:
			static flash_uint8_t xxxx[] = {
				... data ...
				0,1, 1,3, 6,7, 6,8, 4,6, 2,8, 5,7, 2,4, 8,9, 1,5, 3,9, 2,3, 0,4, 7,9, 0,2, 3,5
				... data ...
			};
		"""

	def __init__( self, filename ):
		self.filename = filename
		self.indexes  = {}

		#self.re_array_decl = re.compile( "static\s*\S*\s(\w*)\[\]\s*=\s*{\s*") # extract sprites256_pal from "static flash_uint8_t sprites256_pal[] = {"
		# MATCH  static flash_uint8_t sprites256_pal[] = {  --> extract "sprites256_pal"
		#    OR  static struct ship eliteships[] = {        --> extract "eliteships"
		self.re_array_decl = re.compile( "static(\s*|\s*\S*\s*)\S*\s(\w*)\[\]\s*=\s*{\s*")
		self.re_array_end  = re.compile( "\s*}\s*;\s*" )
		self.re_sub_array  = re.compile( "\s*{(.*)}\s*,\s*" ) # try to catch sub-array definition : { "MISSILE", 17, MISSILE_vertices, 28, MISSILE_edges },

		self.analyse() # Analyse the file

	def analyse( self ):
		""" Analyse the file to retreive ressource name and indexes """
		with open( self.filename, "r" ) as f:
			line = 'fake'
			current_name  = None # Current Name of the ressource
			current_start = None # Data start index
			while( line ):
				sol  = f.tell() #Start Of Line
				line = f.readline()

				r = self.re_array_decl.match( line )
				if r:
					current_name  = r.group(2)
					current_start = None # Data will start at next line
					continue

				# Start of data not yet registered ?
				if current_name and not(current_start):
					current_start = sol
					continue

				r = self.re_array_end.match( line )
				if r:
					# Assert that we have the needed to store it
					assert current_name and current_start
					self.indexes[current_name] = ( current_start, sol-1 )

	def __parse_line( self, lst, line ):
		""" Parse the items in the comma-separated line and push it into the list """
		# Do we have a C array declaration into another C array declaration
		line = line.strip()
		if len( line )==0:
			return

		# { "MISSILE", 17, MISSILE_vertices, 28, MISSILE_edges },
		r = self.re_sub_array.match( line )
		if r:
			sub_list = []
			self.__parse_line( sub_list, r.group(1) )
			lst.append( sub_list )
			return

		for item in [ s.strip() for s in line.split(',') ]:
			if len(item)==0:
				continue
			# Strip double-quote from string
			if item[0]==item[-1]=='"':
				item=item[1:-1]
			# Strip simple-quote from string
			elif item[0]==item[-1]=="'":
				item=item[1:-1]
			lst.append( item )

	def get( self, res_name ):
		""" read the content of the ressource as list """
		if not res_name in self.indexes:
			raise Exception( "No %s ressource in %s" % res_name, self.filename )

		r = []
		sod, eod = self.indexes[res_name] # Start of data, end_of_data
		with open( self.filename, "r" ) as f:
			f.seek( sod )
			line = 'fake'
			while( line ):
				line = f.readline()
				self.__parse_line( r, line )
				if f.tell() >= eod:
					break
		return r
