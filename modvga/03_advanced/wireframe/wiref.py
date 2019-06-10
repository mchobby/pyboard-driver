from machine import Pin, SPI
from gdtls import HLoader
from gd import *
from math import sin, cos #sqrt
import time


BLACK = rgb(0,0,0)
WHITE = rgb(255,255,255)

def replicate(color): # Byte
	return (color << 6) | (color << 4) | (color << 2) | color

# === PlotterClass =============================================================

class PlotterClass():
	def __init__( self, gameduino ):
		self.gd = gameduino # Gameduino instance
		self.flip = 0 # byte
		self.plotting = 0 # byte

		# Loading Eraser_code MicroCode from eraser.h
		hl = HLoader( 'eraser.h' )
		self.eraser_code = [ int(value) for value in hl.get('eraser_code') ] # Extract from: static flash_uint8_t eraser_code[] = [
		del( hl )
		# Loading Wireframe_code MicroCode from wireframe.h
		hl = HLoader( 'wireframe.h' )
		self.wireframe_code = [ int(value) for value in hl.get('wireframe_code') ]
		del( hl )

	def _erase( self ):
		color = 1 if self.flip>0 else 2
		self.plotting = 0
		self.gd.wr(J1_RESET, 1)
		self.gd.wr(COMM+7, 1)
		self.gd.wr(COMM+8, replicate(color ^ 3))
		self.gd.microcode(self.eraser_code)

	def _waitready( self ):
		while( self.gd.rd(COMM+7) ):
			time.sleep( 0.001 ) # Wait 1 ms

	def begin( self ):
		# Draw 256 sprites left to right, top to bottom, all in 4-color
		# palette mode.  By doing them in column-wise order, the address
		# calculation in setpixel is made simpler.
		# First 64 use bits 0-1, next 64 use bits 2-4, etc.
		# This gives a 256 x 256 4-color bitmap.

		#unsigned int i;
		for i in range( 256 ):
			x =     72 + 16 * ((i >> 4) & 15)  #    int x =     72 + 16 * ((i >> 4) & 15);
			y =     22 + 16 * (i & 15)         #    int y =     22 + 16 * (i & 15);
			image = i & 63         #  image 0-63
			pal   =   3 - (i >> 6) #  palettes bits in columns 3,2,1,0
			self.gd.sprite(i, x, y, image, 0x8 | (pal << 1), 0)
		self.flip = 0
		self.plotting = 0
		self._erase()
		self.show()

	def show( self ):
		self._waitready()
		if (self.flip == 1):
			self.gd.wr16(PALETTE4A, BLACK)
			self.gd.wr16(PALETTE4A + 2, WHITE)
			self.gd.wr16(PALETTE4A + 4, BLACK)
			self.gd.wr16(PALETTE4A + 6, WHITE)
		else:
			self.gd.wr16(PALETTE4A, BLACK)
			self.gd.wr16(PALETTE4A + 2, BLACK)
			self.gd.wr16(PALETTE4A + 4, WHITE)
			self.gd.wr16(PALETTE4A + 6, WHITE)
		self.flip = 1 if self.flip==0 else 0
		self._erase()


	def line( self, x0, y0, x1, y1): # Byte
		swap = 0 # Byte
		steep = abs(y1 - y0) > abs(x1 - x0)
		if steep :
			x0, y0 = y0, x0
			x1, y1 = y1, x1
			steep = 1
		else:
			steep = 0
		if x0 > x1:
			x0, x1 = x1, x0
			y0, y1 = y1, y0
		deltax = x1 - x0
		deltay = abs(y1 - y0)
		error = int( deltax / 2 )
		if y0 < y1:
			ystep = 1
		else:
			# ystep est un byte (0..255). Il faut donc utiliser un complément à deux
			# ystep = -1
			# >>> bin( -1 & 0b11111111 )
			# '0b11111111'
			ystep = 255

		x = 0
		y = y0

		self._waitready()
		if self.plotting==0 : # if( !plotting )
			self.gd.microcode( self.wireframe_code )
			self.plotting = 1
			color = 1 if self.flip == 1 else 2
			self.gd.wr(COMM+8, color << 6)

		self.gd.__wstart( COMM+0 )
		self.gd.spi.write( bytes( [x0,y0,x1,y1,steep,deltax,deltay,ystep] ) )
		self.gd.__end()

# === 3D Projection ============================================================
hl = HLoader( 'eliteships.h' )
# List of ships Pythonized from eliteships.h, static struct ship eliteships[]
# which list the available ships
eliteships = hl.get('eliteships')
NSHIP = len( eliteships )
# Name, VerticeCount, vertices_res_name, EdgesCount, edges_res_name
# eliteships = [
#	[ "ADDER", 18, "ADDER_vertices", 29, "ADDER_edges" ],
#	[ "ANACONDA", 15, "ANACONDA_vertices", 25, "ANACONDA_edges" ],



class ShipDataFacade():
	""" Small facade to gain easy access to a ship data """
	def __init__( self, eliteships, hl, ship_index ):
		self.eliteships = eliteships
		self.hl = hl # HLoader - header loader
		self.ship_index = ship_index

	@property
	def name( self ):
		return self.eliteships[self.ship_index][0]

	@property
	def vertice_count( self ):
		return int(self.eliteships[self.ship_index][1])

	@property
	def edge_count( self ):
		return int(self.eliteships[self.ship_index][3])

	@property
	def vertices( self ):
		""" Vertices data as a list """
		return self.hl.get( self.eliteships[self.ship_index][2] )

	@property
	def edges( self ):
		""" Edges data as a list """
		return self.hl.get( self.eliteships[self.ship_index][4] )


def ship_data( ship_index ):
	""" return the eliteships[x] entry but with the array of data instead of the
	 	zzz_vertices and zzz_edges name.  Returns a tuple ( Name, Vertices_count, Vertices_list, Edges_count, Edges_list )"""
	global eliteships
	global hl

	return ShipDataFacade( eliteships, hl, ship_index  )

# Transformation matrice for the vertex projection
mat = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ] # static float mat[9]

def rotation( phi ): # float
	""" Calculate the transformation matrice.

		Taken from glRotate()"""
	x = 0.57735026918962573
	y = 0.57735026918962573
	z = 0.57735026918962573

	s = sin(phi)
	c = cos(phi)

	mat = []
	mat.append( x*x*(1-c)+c   ) # mat[0]
	mat.append( x*y*(1-c)-z*s ) # mat[1]
	mat.append( x*z*(1-c)+y*s ) # mat[2]

	mat.append( y*x*(1-c)+z*s  ) # mat[3]
	mat.append( y*y*(1-c)+c    ) # mat[4]
	mat.append( y*z*(1-c)-x*s  ) # mat[5]

	mat.append( x*z*(1-c)-y*s ) # mat[6]
	mat.append( y*z*(1-c)+x*s ) # mat[7]
	mat.append( z*z*(1-c)+c   ) # mat[8]
	return mat

projected = list( (0,) * 40 * 2 ) # static byte projected[40 * 2];

def project( ship, distance ): # eliteships[x], float
	""" Make a Projection of a given ship with the projection matrix

		ship is a ShipDataFacade """
	vx = 0 # byte
	pm = ship.vertices
	pm_e = ship.edges #pm_e = pm + (s->nvertices * 3);
  	#byte *dst = projected;
	global projected
	projected_idx = 0
	x, y, z = 0, 0, 0 # Byte

	global mat
	for i in range( 0, ship.vertice_count*3,  3 ): # count from 0 to vertice_count by step of 3
		x = int( pm[i] )
		y = int( pm[i+1] )
		z = int( pm[i+2] )
		xx = x * mat[0] + y * mat[3] + z * mat[6] # float
		yy = x * mat[1] + y * mat[4] + z * mat[7]
		zz = x * mat[2] + y * mat[5] + z * mat[8] + distance
		q = 140 / (140 + zz) # float
		projected[projected_idx] = int(128 + xx * q) # *dst++ = byte(128 + xx * q);
		projected_idx += 1
		projected[projected_idx] = int(128 + yy * q)
		projected_idx += 1

def draw( ship, plotter, distance ): # distance as float
	""" draw a given ship on the screen

	ship is a ShipDataFacade """

	# project the ship to a flat screen (will update projected)
	project( ship, distance )

	pe = ship.edges
	# flash_uint8_t *pe_e = pe + (s->nedges * 2);
	# while (pe < pe_e) {
	global projected
	for i in range( 0, (ship.edge_count)*2, 2 ):
		v0 =  int(pe[i]) << 1
		v1 =  int(pe[i+1]) << 1
		#Plotter.line(v0[0], v0[1], v1[0], v1[1]);
		plotter.line( projected[v0], projected[v0+1], projected[v1], projected[v1+1] )


# === Setup ====================================================================
print( 'Setup...' )

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
gd.ascii()
gd.putstr(0, 0, "Accelerated wireframe");

plotter = PlotterClass( gd )
plotter.begin()

# === Loop =====================================================================
print( 'Loop...')

sn = 0    # Ship number, 0-NSHIPS
phi = 0.0 # Current rotation angle
every = 0 # byte
tprev = time.ticks_ms() # time

def cycle( ship, distance ):
	""" Draw one frame of ship """
	global gd
	global plotter
	global mat
	global phi
	global tprev
	mat = rotation( phi ) # Transformation matrice
	phi += 0.02

	draw( ship, plotter, distance);

	# GD.waitvblank(); // uncomment this to sync to 72Hz frame rate
	plotter.show()

	# Update the FPS statistic (every 4 iteration)
	global every
	every += 1
	if every == 4:
		t = time.ticks_ms()
		every = 0

		fps = 4 * 1000/(t-tprev)
		gd.putstr(36, 0, "%.3f fps  " % fps )
		tprev = t

# -- effective loop --
# print( hl.indexes )
while True:
	_ship = ship_data( sn ) # sn: Ship Number
	name = "%s - ship %s of %s" % (_ship.name, sn+1, NSHIP )

	print( name )

	gd.putstr(0, 36, "                                                  ")
	gd.putstr(25 - int(len(name)/2), 36, name)

	# Zoom in + rotate
	for d in range( 100 ):
		cycle( _ship, 1000 - 10*d ) # Variation of distance
	# Stay in front + rotate
	for d in range( 76*2 ):
		cycle( _ship, 0.0 )
	# Zoom out + rotate
	for d in range( 100 ):
		cycle( _ship, 10 * d )

	# Next SHIP
	sn = (sn + 1) % NSHIP

# Finally
print( "That's all folks" )
