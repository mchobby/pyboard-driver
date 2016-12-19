""" ENG: Doggy is a Robot built with 4 paws of 2 servo each.
    FR: Doggy est un Robot constitué de 4 pattes ayant 2 servo chacune.

    See our tutorial - voyez notre tutoriel
        https://wiki.mchobby.be/index.php?title=Hack-micropython-ServoRobot
    WebShop 
        on https://shop.mchobby.be
"""
from servorobot import *
from pyb import I2C
from pyb import delay


# List of possible movements class (see forward in the code for initialisation ) 
MovementsCls = []

class Doggy( RobotBase ):
	""" Doggy is a SerboRobot using 4 members having 2 servo each (2 Degree of Free each).
	    The members are wired to a PCA9685 PWM Controler wired to I2C(2) at address 0x40 

	    See the mchobby.be for the tutorial """

	# members[0] - front right (avant droit)  - Shoulder on #0, Wrist on #1
	# members[1] - front left (avant gauche)  - Shoulder on #2, Wrist on #3
	# members[2] - rear right (arriere droit) - Shoulder on #6, Wrist on #7
	# members[3] - rear left  (arrière gauche)- Shoulder on #4, Wrist on #5
	
	def __init__( self, movementscls=MovementsCls ):
		""":Params movementscls: list of Movement classes available to the robot."""

		self.i2c = I2C( 2, I2C.MASTER )
		RobotBase.__init__( self, controlers=[(self.i2c,0x40)], movementscls=MovementsCls ) # PCA9685 is wired on I2C 2

		self.members.append( Member2DF( self, 0, 1) ) # Front right
		self.members.append( Member2DF( self, 2, 3) ) # Front left
		self.members.append( Member2DF( self, 6, 7) ) # Rear  right
		self.members.append( Member2DF( self, 4, 5) ) # Rear  left
		self.members[1].shoulder.inverted(True) # Invert control on member 1 shoulder
		self.members[3].shoulder.inverted(True)
		self.members[1].wrist.inverted(True) # Invert control on member 2 wrist
		self.members[3].wrist.inverted(True)

		self.reset()

	@property
	def fr(self): # Front Right (english) - Avant droit (francais)
		return self.members[0]

	@property
	def fl(self): # Front Left (english) - Avant gauche (francais)
		return self.members[1]

	@property
	def rr(self): # Rear Right (english) - Arriere droit (francais)
		return self.members[2]

	@property
	def rl(self): # Rear Left (english) - Arriere gauche (francais)
		return self.members[3]

	def standup(self, wdegree=90, step=2, sdelay=25):
		""" Move all wrists to the target wdegree for stand up. Do not touch the shoulders """
		while any( [ m.wrist.angle != wdegree for m in self.members ] ):
			for m in self.members:
				# target = wdegree
				# current = m.wrist.angle
				step_mult = 1
				if wdegree < m.wrist.angle: # Negative movement
					step_mult = -1 
				if abs(wdegree - m.wrist.angle) > step:
					m.wrist.set( m.wrist.angle+(step*step_mult) )
					#print( 'set-angle %i' % (m.wrist.angle+step) )
				else:
					m.wrist.set( wdegree )
					#print( 'set-final-angle %i' % (wdegree) )
			delay( sdelay )

	def align(self, sdegree=0, step=2, sdelay=25, asymetric=False ):
		""" Align all shoulder in the same angle. Good to fix initial position. 
		    Avoid over 60 degree """
		paws = { self.fr : sdegree, self.fl : sdegree, self.rr : -1*sdegree if asymetric else sdegree, self.rl : -1*sdegree if asymetric else sdegree }
		while( any([ m.shoulder.angle != deg for m,deg in paws.items() ]) ):
			for m,deg in paws.items():
				step_mult = 1
				if deg < m.shoulder.angle: # Negative movement
					step_mult = -1
				if abs(deg - m.shoulder.angle) > step:
					m.shoulder.set( m.shoulder.angle+(step*step_mult) )
				else:
					m.shoulder.set( deg )
			delay( sdelay )

	def place_paw( self, member, sdegree, wdegree=90 ):
		""" sdegree: target shoulder degree """
		if member.shoulder.angle != sdegree:
			# print( 'place_paw at %i' % sdegree )
			member.wrist.set( wdegree-25 )  # Lift off the floor
			delay(100)
			member.shoulder.set( sdegree ) # Move
			delay(100)
			member.wrist.set( wdegree ) # Place on the floor


class Forward( Movement ):
	""" Make a forward movement for the Robot """
	def name():
		""" Return names applying for the movement """
		return ('FORWARD','F')

	def prepare( self, sdegree_min=10, sdegree_max=65, wdegree=90, **kw ):
		""" wdegree: desired wrist degree """
		d = self.robot
		d.standup( wdegree=wdegree )
		interval = (sdegree_max - sdegree_min)//4 # All paws must be at a different move position
		d.place_paw( d.fl, sdegree_max, wdegree )
		d.place_paw( d.fr, sdegree_max-(1*interval), wdegree )
		delay(100)
		# Asymetric move
		d.place_paw( d.rl, -1*(sdegree_max-(2*interval)), wdegree  )
		d.place_paw( d.rr, -1*(sdegree_max-(3*interval)), wdegree )
		delay(100)

	def do( self, sdegree_min=10, sdegree_max=65, wdegree=90, step_angle=5, **kw ):
		d = self.robot
		for m in [d.fl,d.fr,d.rl,d.rr]:
			#names={self.fl:'fl',self.rr:'rr',self.fr:'fr',self.rl:'rl'}
			#print( '--- paw %s ---' % names[m] )
			# Asymetric move for rear paws
			if m in [d.rl, d.rr]:
				smin = -1*sdegree_min
				smax = -1*sdegree_max
			else:
				smin = sdegree_min
				smax = sdegree_max
			#print( 'min %i, max %i - angle %i' % (smin, smax, m.shoulder.angle) )
			m.shoulder.set( m.shoulder.angle-step_angle )

		delay( 2 )	
		for m in [d.fl,d.rr,d.fr,d.rl]:
			if m in [d.rl, d.rr]:
				smin = -1*sdegree_min
				smax = -1*sdegree_max
			else:
				smin = sdegree_min
				smax = sdegree_max

			if m in [d.rl,d.rr]:
				if m.shoulder.angle <= smax:
					d.place_paw( m, smin, wdegree )
			else:
				if m.shoulder.angle <= smin:
					d.place_paw( m, smax, wdegree )

class Backward( Forward ):
	""" Make a Backward movement for the Robot """
	def name():
		""" Return names applying for the movement """
		return ('BACKWARD','BACK', 'B')

	#def prepare() ) same as ancestor

	def do( self, sdegree_min=10, sdegree_max=65, wdegree=90, step_angle=-5, **kw ):
		d = self.robot
		for m in [d.fl,d.fr,d.rl,d.rr]:
			#names={d.fl:'fl',d.rr:'rr',d.fr:'fr',d.rl:'rl'}
			#print( '--- paw %s ---' % names[m] )
			# Asymetric move for rear paws
			if m in [d.rl, d.rr]:
				smin = -1*sdegree_min
				smax = -1*sdegree_max
			else:
				smin = sdegree_min
				smax = sdegree_max
			#print( 'min %i, max %i - angle %i' % (smin, smax, m.shoulder.angle) )
			m.shoulder.set( m.shoulder.angle-step_angle )

		delay( 2 )	
		for m in [d.fl,d.rr,d.fr,d.rl]:
			if m in [d.rl, d.rr]:
				smin = -1*sdegree_min
				smax = -1*sdegree_max
			else:
				smin = sdegree_min
				smax = sdegree_max

			if m in [d.rl,d.rr]:
				if m.shoulder.angle >= smin: # <= smax:
					d.place_paw( m, smax, wdegree )
			else:
				if m.shoulder.angle >= smax: # m.shoulder.angle <= smin
					d.place_paw( m, smin, wdegree )

class Left( Movement ):
	""" Make a turning on the left for the Robot """
	def name():
		""" Return names applying for the movement """
		return ('LEFT','L')

	def prepare( self, sdegree_max=60, wdegree=90, **kw ):
		""" sdegree_max: max amplitude for the movement
		    wdegree: desired wrist degree. """
		d = self.robot
		d.standup( wdegree=wdegree )
		d.place_paw( d.fl, 0, wdegree )
		d.place_paw( d.fr, sdegree_max, wdegree )
		delay(100)
		# Asymetric move
		d.place_paw( d.rr, 0, wdegree )
		d.place_paw( d.rl, -1*sdegree_max, wdegree  )
		delay(100)

	def do( self, sdegree=90, sdegree_max=60, wdegree=90, step_angle=2, **kw ):
		""" Make a movement on the left of sdegree. sdegree_max is the max amplitude for the movement """ 
		d = self.robot
		scurrent = 0 # current position of the full movement of sdegree
		while scurrent < sdegree:
			if ( abs( d.rr.shoulder.angle ) > sdegree_max ) or ( d.fl.shoulder.angle > sdegree_max ) or ( d.fr.shoulder.angle < 0 ) or ( d.rl.shoulder.angle > 0 ):
				self.prepare( sdegree_max=sdegree_max, wdegree=wdegree )
			scurrent += step_angle

			for m in [d.fl,d.rr,d.fr,d.rl]:
				if m in [d.fr, d.rr]:
					m.shoulder.set( m.shoulder.angle - step_angle )
				else:
					m.shoulder.set( m.shoulder.angle + step_angle )

			delay( 10 )

class Right( Movement ):
	""" Make a turning on the right for the Robot """
	def name():
		""" Return names applying for the movement """
		return ('RIGHT','R')

	def prepare( self, sdegree_max=60, wdegree=90, **kw ):
		""" sdegree_max: max amplitude for the movement
		    wdegree: desired wrist degree. """
		d = self.robot
		d.standup( wdegree=wdegree )
		d.place_paw( d.fl, sdegree_max, wdegree )
		d.place_paw( d.fr, 0, wdegree )
		delay(100)
		# Asymetric move
		d.place_paw( d.rr, -1*sdegree_max, wdegree  )
		d.place_paw( d.rl, 0, wdegree )
		delay(100)

	def do( self, sdegree=90, sdegree_max=60, wdegree=90, step_angle=2, **kw ):
		""" Make a movement on the left of sdegree. sdegree_max is the max amplitude for the movement """ 
		d = self.robot
		scurrent = 0 # current position of the full movement of sdegree
		while scurrent < sdegree:
			if ( abs( d.rl.shoulder.angle ) > sdegree_max ) or ( d.fr.shoulder.angle > sdegree_max ) or ( d.fl.shoulder.angle < 0 ) or ( d.rr.shoulder.angle > 0 ):
				self.prepare( sdegree_max=sdegree_max, wdegree=wdegree )
			scurrent += step_angle

			for m in [d.fl,d.rr,d.fr,d.rl]:
				if m in [d.fl, d.rl]:
					m.shoulder.set( m.shoulder.angle - step_angle )
				else:
					m.shoulder.set( m.shoulder.angle + step_angle )

			delay( 10 )

class Hello( Movement ):
	""" Make a Hello sign with the Robot """
	def name():
		""" Return names applying for the movement """
		return ('HELLO','H')

	def prepare( self, sdegree_max=60, wdegree=90, right=False, **kw ):
		""" sdegree_max: max amplitude for front paw that will stabilize the robot
		    wdegree: desired wrist degree for all paw. 
		    right: hello with the right paw... otherwise the left one
		    hello_wdegree: wdegree of the Hello Paw (negative for UP movement)"""
		d = self.robot
		d.standup( wdegree=wdegree )
		if right:
			d.place_paw( d.fl, sdegree_max, wdegree )
			d.place_paw( d.fr, 0, wdegree )
		else:
			d.place_paw( d.fr, sdegree_max, wdegree )
			d.place_paw( d.fl, 0, wdegree )

		delay(100)

	def do( self, sdegree_min=-40, sdegree_max=85, right=False, hello_wdegree=-60, step_angle=2, **kw ):
		""" Make the hello movement from sdegree_max to sdegreee_min """ 
		d = self.robot
		p = None # The hello paw
		if right:
			p = d.fr
		else:
			p =  d.fl

		initial_sdegree = p.shoulder.angle # Remember it
		initial_wdegree = p.wrist.angle 
		p.wrist.set( hello_wdegree )
		delay( 100 )
		for i in range( p.shoulder.angle, sdegree_max, step_angle ):
			p.shoulder.set( i )
			delay( 10 )
		for i in range( sdegree_max, sdegree_min, -1*step_angle ):
			p.shoulder.set( i )
			delay( 10 )
		for i in range( sdegree_min, sdegree_max, step_angle ):
			p.shoulder.set( i )
			delay( 10 )
		for i in range( sdegree_max, initial_sdegree, -1*step_angle ):
			p.shoulder.set( i )
			delay( 10 )

		p.wrist.set( initial_wdegree )

# Defining the list of movements
MovementsCls.append( Forward )
MovementsCls.append( Backward )
MovementsCls.append( Left )
MovementsCls.append( Right )
MovementsCls.append( Hello )
