from servoctrl import ServoCtrl

class EValueError( Exception ):
	pass 

class ServoJoint:
	angle = None # Current angle of the servo (from -90 to +90)
	def __init__( self, owner, servoindex, ctrlindex=0):
		self.owner = owner # must be a RobotBase to get access to ctrls (controlers)
		self.ctrlindex = ctrlindex # 0 for the first PCA9685's Servo Controler declared in the owner, 1 for the second one
		self.servoindex = servoindex # from 0 to 15 (for each output of the PCA9685)
		self._degmult = 1 # degree multiplier (to invert control)
		self.angle = None # Unknown until first set() call

	def inverted( self, value=True ):
		self._degmult = -1 if value else 1 


	def set( self, degree=0 ):
		if -90 <= degree <= +90:
			self.owner.ctrls[self.ctrlindex].position(self.servoindex, (self._degmult*degree)+90 ) # ServoCtrl.position is from 0 to 180
			self.angle = degree
		else:
			raise EValueError( 'invalid %s' % degree )

class Member2DF():
	shoulder = None
	wrist = None 

	def __init__( self, owner, shoulderindex, wristindex, ctrlindex=0 ):
		""" see ServoJoint for parameters """
		self.shoulder = ServoJoint( owner, shoulderindex, ctrlindex ) 
		self.wrist = ServoJoint( owner, wristindex, ctrlindex )

	def reset( self ):
		""" place all servos to 0° """
		self.shoulder.set(0)
		self.wrist.set(0)

class RobotBase:
	ctrls = [] # List of PCA9685 servo controlers
	members = [] # List of Members (added by descandent)

	def __init__( self, controlers, movementscls ):
		for ctrl_data in controlers:
			self.ctrls.append( ServoCtrl( i2c=ctrl_data[0], address=ctrl_data[1] ))

		self.__movementscls = movementscls # List of Movement class
		self.__movements = {} # List of instanciated Movement

	def reset( self ):
		for m in self.members:
			m.reset()

	def release( self ):
		# Release all servos
		for ctrl in self.ctrls:
			ctrl.release()

	def movement( self, name ):		
		# Call it is already created
		if name in self.__movements: 
			return self.__movements[ name ] 
		else:
			# Look for class et create it
			for cls in self.__movementscls:
				mov_names = cls.name() # Can be a string or a tuple of string
				if ((type(mov_names) is tuple) and (name in mov_names)) or (mov_names == name):
					# Create the Movement object with the robot as Owner
					m = cls( self )
					self.__movements[name] = m
					return m 

	def prepare( self, name, **kw ):
		self.movement( name ).prepare( **kw )

	def move( self, name, prepare=False, repeat=None, **kw ):
		if prepare:
			self.prepare( name, **kw )
		if repeat:
			if callable( repeat ):
				iter = 0
				while repeat( self, name, iter ):
					self.movement( name ).do( **kw )
					iter += 1 
			else:
				for i in range(repeat):
					self.movement( name ).do( **kw )
		else:
			self.movement( name ).do( **kw )


class Movement:
	def __init__( self, robot ):
		self.robot = robot

	def name():
		return 'UNDEFINED'

	def prepare( self, **kw ):
		pass

	def do( self, **kw ):
		pass
