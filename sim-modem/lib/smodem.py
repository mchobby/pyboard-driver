# Manage a SIMCom (SIM800) module under MicroPython
#    Modem in auto-baud detect, UART at 9600 bauds (50ms transmission/100bytes)
#
# See Lib: https://github.com/mchobby/pyboard-driver/tree/master/sim-modem
#
from machine import Pin
import time
from micropython import const

READLINE_TIMEOUT = 150 # 52 ms is enough to receive a line of 100 bytes
OK_BUFF    = b'OK\r\n'
ERROR_BUFF = b'ERROR\r\n'
EMPTY_BUFF = b'\r\n'
SMS_PROMPT_BUFF = b'> '

# Activity Status
AS_READY   = const(0)
AS_UNKNOWN = const(2)
AS_RINGING = const(3)
AS_CALL    = const(4) # Call un progress

# Network Registration Status.
REG_STATUS_NONE    = const(0) # Not registered, Not searching a new operator
REG_STATUS_DONE    = const(1) # Registered, Home network
REG_STATUS_SEARCH  = const(2) # Not registered, Searching new operator to register to
REG_STATUS_DENIED  = const(3) # Registration Denied
REG_STATUS_UNKNOWN = const(4) # Unknown
REG_STATUS_ROAMING = const(5) # Registered, Roaming

# Unsollicited Result Code Status (URC Status)
URC_STATUS_DISABLE = const(0) # Disable Unsollicited Result Code
URC_STATUS_ENABLE  = const(1) # Enable Unsollicited Result Code (stat only)
URC_STATUS_EXTENED = const(2) # Enable Unsollicited Result Code (stat[,lac,ci] )

class ModemError( Exception ):
	pass

class CommandError( Exception ):
	pass

class NetworkScan:
	__slots__ = ['operator','mcc','mnc','rxlev','cellid','arfcn']

	def __init__( self ):
		self.operator = ''
		self.mcc = ''
		self.mnc = ''
		self.rxlev = 0
		self.cellid = ''
		self.arfcn = ''

	def load( self, dico ):
		self.operator = dico['Operator']
		self.mcc = dico['MCC'] # Mocule Country Code, Europe starts with 2. see https://fr.wikipedia.org/wiki/Mobile_country_code
		self.mnc = dico['MNC'] # Mobile Network Code, see https://fr.wikipedia.org/wiki/Mobile_Network_Code
		self.rxlev = int(dico['Rxlev']) # Receive level in decimal
		self.cellid = dico['Cellid']    # in hexadecimal format
		self.arfcn  = dico['Arfcn']     # Absolute radio frequency channel number, in decimal format

	def __repr__( self ):
		return '<NetworkScan operator:%s, rxlev:%s, cellid:%s, arfcn:%s>' % (self.operator,self.rxlev,self.cellid,self.arfcn)

class SMS:
	__slots__ = ['sender','send_date','lines']

	def __init__( self ):
		self.sender = ''
		self.send_date = '' # We do not convert it to time
		self.lines = []

class SimModem:
	def __init__( self, uart, pwr_pin, pin_code = None ):
		self.uart = uart
		self.pwr_pin = pwr_pin
		self.pin_code = pin_code
		self._debug = False
		self._active = False # GSM Modem has been activated
		self._callee = ''    # Callee Phone Number ( capture in Unsollicited_Result_Code )
		self._sms_mode = False # Flag to check if SMS mode is configured
		self.rec_sms = [] # List of slot initialized with a received SMS
		self.buf1 = bytearray(1) # Needed for proper SMS sending

		# Unsollicited_Result_Code
		self._urc_cpin_ready = None # URC: Card Pin returned ready

		uart.init( baudrate=9600, timeout=READLINE_TIMEOUT ) # readline timeout 150ms
		if self.pwr_pin:
			self.pwr_pin.init( mode=Pin.OUT, value=True )

	# --- DEBUGGING TOOL -------------------------------------------------------
	@property
	def debug( self ):
		return self._debug

	@debug.setter
	def debug( self, value ):
		self._debug = value

	def dmesg( self, msg, prefix='debug' ):
		if self._debug:
			print( '%5s: %s'%(prefix,msg) )

	# --- PRIVATE METHOD -------------------------------------------------------
	def is_empty_buff( self, buff ):
		if (buff==None) or (buff==EMPTY_BUFF):
			return True
		for ch in buff:
			if ch!=0x00: # All nulls
				return False
		return True

	def _write_cmd( self, cmd ):
		""" Write a command to the modem.
		    :param cmd: command string (will be encoded to ASCII) or already encoded bytes() array."""
		self.dmesg( cmd, prefix='-->>' )
		if type(cmd) is str:
			self.uart.write( cmd.encode('ASCII') )
		else:
			self.uart.write( cmd ) # Send the byte array

		#self.uart.write( chr(13) )
		self.uart.write( chr(10) )

	def _process_URC( self, msg ):
		""" Process Unsollicited_Result_Code then set objet property accordingly.
			Return: None when nothing has to be done by the callee; ERROR_BUFF when URC must turn into an error; OK_BUFF when URC is same as OK message
			may also raise Exception when appropriate
		"""
		if b'+CPIN: ' in msg:
			scode = msg.decode( 'ASCII' ).split( ': ' )[1].replace( '\r\n', '' ) # extract code from b'+CPIN: READY\r\n'
			if scode=='READY':
				self._urc_cpin_ready = True
				return OK_BUFF # We have handled it!
			elif scode=='SIM PIN':
				self._urc_cpin_ready = False
			else:
				raise CommandError( 'Requires special %s unlocking' % scode )

		if b'+CLIP: ' in msg: # Calling Line Identification '+CLIP: "+32496928320",145,"",0,"",0\r\n'
			sdata = msg.decode( 'ASCII' ).split( ': ' )[1].replace( '\r\n', '' )
			self._callee = sdata.split(',')[0].strip( '"' )

		if b'NO CARRIER' in msg:
			self._callee = ''

		if b'+CMTI: ' in msg: # SMS Message reception '+CMTI: "SM",1\r\n'
			sdata = msg.decode( 'ASCII' ).split( ': ' )[1].replace( '\r\n', '' )
			self.rec_sms.append( int(sdata.split(',')[1]) ) # Add storage slot to received_sms



	def _read_response( self, ref, timeout_ms=None, callback=None, wait_buff=None ):
		""" Read the response for OK or ERROR or TimeOut.
			Return True if OK is received before timeout else return false when timeout is reached.
			An ERROR will raise a CommandError (with 'ref' informative string ).
			Content is also processed to detect URC (Unsollicited_Result_Code).
			:param callback: callback method will be called for all received response (if mentionned)
			:param wait_buff: may want for specific bytes() buffer (other than OK/ERROR)"""
		#self._rbuf.clear() # Clear
		t = time.ticks_ms()
		s = self.uart.readline()
		while (timeout_ms==None) or ( time.ticks_diff( time.ticks_ms(), t ) < timeout_ms ) :
			self.dmesg( s, prefix='<<--' )
			if self.is_empty_buff(s):
				# Tru tu read next line -> restart processing loop
				s = self.uart.readline()
				continue

			# Want a specific response?
			if wait_buff and (wait_buff in s):
				return True
			# Wait for standard buffer responses (Error/OK)
			if s == OK_BUFF:
				return True # OK received
			if s == ERROR_BUFF:
				raise CommandError( ref )
			# process Unsollicited_Result_Code
			s_urc = self._process_URC( s ) # May returns NULL, ERROR_BUFF or OK_BUFF
			if s_urc:
				# s_URC returned OK_BUFF it means that it managed somthing
				if s_urc == OK_BUFF:
					# Abord processing here and prepare to process the next read
					s = self.uart.readline()
					continue
				else:
					# process the response as the next buffer line
					s = s_urc
					continue
			# if callback --> call it
			if callback:
				callback( s )
			else:
				# Accumulate response in the buffer
				pass
			# Process Next buffer line
			s = self.uart.readline()
		return False # Timeout received

	def _configure_modem( self ):
		""" Send the needed AT Command to initialize the modem """
		self.dmesg('Configure modem')
		self.send_then_read( 'ATZ', timeout_ms=3000 )
		self.send_then_read( 'ATE0' ) # Echo Off
		if self.is_pin_required:
			self.dmesg('Pin required')
			if self.pin_code:
				self.send_then_read( 'AT+CPIN=%s' % self.pin_code )
			else:
				raise ModemError( 'Pin missing!')
		#self.send_then_read( 'AT+CMGF=1' ) # Text Mode SMS
		self.send_then_read( 'AT+CLIP=1' )  # Calling Line Identification
		self.dmesg('Modem configured!')
		return True

	def send_then_read( self, cmd, timeout_ms = 1000, callback=None, wait_buff=None ):
		""" Send a command and store the response in reception buffer.
		    the final OK is expected within the timeout_ms delay.

			:param cmd: a command STRING (will be encoded to ASCII)
			:param callback: will receive Bytes response. Empty lines are skipped.
			:param wait_buff: specific bytes() buffer we want to wait for """
		self._write_cmd( cmd )
		return self._read_response( cmd, timeout_ms, callback, wait_buff )

	# --- PUBLIC METHOD --------------------------------------------------------
	def update( self, timeout_ms=1000 ):
		""" Pumping message loop, will display message in debug """
		return self._read_response( '', timeout_ms )

	def activate( self ):
		""" Activate the GSM module """
		# Check if the module is already up and running
		self._active = False
		# Send an escape before Ping! If modem is power-up and locked down in SMS editing, we will exit SMS editing
		time.sleep_ms( 300 )
		self.uart.write( bytes([27]) ) #
		if self.ping():
			self.dmesg('Modem already running')
			self._active = self._configure_modem()
			return self._active

		# Ask power up
		if not self.pwr_pin:
			raise ModemError( 'cannot activate modem without pwr_pin!')
		self.dmesg('Power Up')
		self.pwr_pin.value( False ) # Pulse Low to startup
		time.sleep_ms( 50 )
		self.pwr_pin.value( True )
		# Wait for power_up
		self.dmesg('Wait booting')
		time.sleep( 5 )
		self.dmesg('training auto-baud')
		# Send 3 AT command to stimulate autobaud detection
		for i in range(5):
			if self.ping():
				self._active = self._configure_modem()
				return self._active
		raise ModemError( 'Modem not responding' )

	def wait_for_ready( self ):
		""" Wait for the registered modem to enter in READY state.
		 	so can send SMS and make calls """
		while not self.activity_status==AS_READY:
			time.sleep_ms(300)
		return True

	@property
	def active( self ):
		""" Is the modem Activated and initialized ? """
		return self._active

	def shutdown( self ):
		self._write_cmd( 'AT+CPOWD=1' ) # Normal power off

	def ping( self ):
		""" Check if the modem respond to AT Command """
		return self.send_then_read( 'AT' ) # We expect an OK for the AT command

	def scan_networks( self ):
		""" Scan the available networks and return a list """
		r = list()

		def __scan_response( s ):
			# s is a buffer
			self.dmesg( s, prefix='ScanNetwork')
			# Validate buffer before loading
			if not (b'Operator' in s) or not (b'Arfcn' in s):
				return
			# Convert response to dictionnary
			d = {}
			for pair in s.decode('utf8').replace('\r\n','').split(','):
				k,v = pair.split(':')
				d[k]=v.strip('"')
			item = NetworkScan()
			item.load( d )
			r.append( item )

		# Can take up to 45 sec accordingly to documentation
		self.send_then_read( 'AT+CNETSCAN', timeout_ms=45000, callback=__scan_response )
		return r

	@property
	def activity_status( self ):
		""" Phone activity status (CPAS). Returns a AS_xx constant """
		_r = AS_UNKNOWN
		def __scan_response( _b ):
			nonlocal _r
			if b'+CPAS:' in _b:
				_r = int(_b.decode('ASCII').split(' ')[1]) # ['+CPAS:', '0']
			return -1

		self.send_then_read( 'AT+CPAS', callback=__scan_response )
		return _r

	@property
	def is_ringing( self ):
		""" Phone is ringing """
		return self.activity_status == AS_RINGING

	@property
	def has_call( self ):
		""" Currently under call """
		return self.activity_status == AS_CALL

	@property
	def is_pin_required( self ):
		""" Check if a standard PIN code is required. Non standard PIN (like PUK will raise error) """
		# IF status not yet received via Unsollicited_Result_Code THEN stimulate it with an AT command
		# Any invalid case SIM PUK, PH_SIM xxx (antithief) will cause exception
		if self._urc_cpin_ready == None:
			self.send_then_read( 'AT+CPIN?' )
		return not self._urc_cpin_ready

	@property
	def callee( self ):
		""" Caller phone number (for voice calls) """
		return self._callee

	def pickup( self ):
		""" Pickup the voice call """
		self.send_then_read( 'ATA' )

	def hangup( self ):
		""" Hangup the voice call """
		self._callee = '' # Clear it (in case of URE will fail to capture it)
		self.send_then_read( 'ATH' ) # May also consider AT+CHUP

	def call( self, number ):
		""" Dial the target phone number (string)"""
		if self.activity_status != AS_READY:
			raise EModemError( 'Not READY to call' )
		self.send_then_read( 'ATD%s;' % number )

	@property
	def operator( self ):
		""" Return the selected operator (COPS) as a tuple of (mode_int,format_int,operator_string) """
		_r = None
		def __scan_response( _b ):
			nonlocal _r
			if b'+COPS:' in _b:
				_r = _b.decode('ASCII').split(' ')[1] # +COPS: 0,0,"Orange B"
				_r = _r.split(',')
				_r[2] = _r[2].strip('"')
				_r = ( int(_r[0]), int(_r[1]), _r[2] )
			return -1

		self.send_then_read( 'AT+COPS?', callback=__scan_response )
		return _r

	@property
	def rssi( self ):
		""" Quality of connexion in dBm """
		_r = None
		def __scan_response( _b ):
			nonlocal _r
			if b'+CSQ: ' in _b:
				_r = _b.decode('ASCII').split(' ')[1] # +CSQ: 12,0 RSSI,Bit_Error_Rate percent
				_r = _r.split(',')
				_r = int(_r[0])
			return -1

		self.send_then_read( 'AT+CSQ', callback=__scan_response )
		# Transform the RSSI response in dBm
		if _r == 0:
			return -115 # -115 dBm or less
		elif _r == 1:
			return -111 # -111 dBm
		elif 2 <= _r <= 30:
			return  -110+2*(_r-2) # -110 dBm to -54 dBm
		elif _r == -31:
			return -52 # -52 dBm or Higher
		elif _r == 99:
			return -999 # value unknown or not detectable

		raise EModemError('Invalid CSQ %i value' % _r )

	@property
	def network_registration( self ):
		""" Return the status about Network registration as a tuple ( REG_STATUS_xxx, URC_STATUS_xxx ) from CREG.
			REG_STATUS_xxx is network_registration_status.
			URC_STATUS_xxx is unsollicited_result_code_status. """
		_r = None
		def __scan_response( _b ):
			nonlocal _r
			if b'+CREG: ' in _b:
				_r = _b.decode('ASCII').split(' ')[1] # +CREG: 0,1 <URC_STATUS_xxx>,<REG_STATUS_xxx>
				_r = _r.split(',')
				_r = ( int(_r[1]), int(_r[0]) ) # Network registration status first, URC Status after
			return -1

		self.send_then_read( 'AT+CREG?', callback=__scan_response )
		return _r

	@property
	def sim_serial( self ):
		""" Return the IIC ID, SIM Serial number, on 19 positions """
		_r = ''
		def __scan_response( _b ):
			nonlocal _r
			v = _b.decode('ASCII').strip()
			if v.isdigit():
				_r = v
			return -1

		self.send_then_read( 'AT+CCID', callback=__scan_response )
		return _r

	@property
	def imei( self ):
		""" Return the IMEI serial - International Mobile Station Equipement """
		_r = ''
		def __scan_response( _b ):
			nonlocal _r
			v = _b.decode('ASCII').strip()
			if v.isdigit():
				_r = v
			return -1

		self.send_then_read( 'AT+GSN', callback=__scan_response )
		return _r

	@property
	def sms_service( self ):
		""" Phone number of the SMS Service Center """
		# see AT+CSCA
		raise ModemError('Not implemented')

	@sms_service.setter
	def sms_service( self, number ):
		# Change the Must be set before 1rst sms_send() attempt
		raise ModemError('Not implemented')

	def _config_sms_mode( self ):
		""" Configure the modem to send SMS. """
		# Switch SMS mode to Text if not done yet
		if not self._sms_mode:
			self.send_then_read( 'AT+CMGF=1' )
			self._sms_mode = True

	def send_sms( self, number, text ):
		""" Send a message contained in text to the phone number. Text can contains \r or \r\n.
		 	Returns the Message Reference ID (or None)"""
		_r = None
		def __scan_response( _b ):
			nonlocal _r
			if b'+CMGS: ' in _b:
				_r = int(_b.decode("ASCII").split(' ')[1]) # b'+CMGS: 244\r\n'
			return -1

		self._config_sms_mode()
		if len( text )>160:
			raise ModemError('SMS Exceed max length')
		lines = text.replace('\r\n','\r').split('\r')

		if not self.send_then_read( 'AT+CMGS="%s"' % number, timeout_ms=2000, wait_buff=SMS_PROMPT_BUFF ):
			raise ModemError( 'SMS Prompt Timeout')

		for line in lines:
			# MicroPython Unicode String is optimized such a way that it is
			# impossible to encode it to ISO-8859-1 (latin1) or ASCII property under micropython.
			# However, ord() will return the proper Latin1 ASCII code, so we can workaround
			# the issue.
			for ch in line:
				self.buf1[0] = ord(ch)
				self.uart.write( self.buf1 )
			self.uart.write( chr(10) )
			time.sleep_ms( 100 )

		# Sending SMS
		self.uart.write( bytes([13]) ) # Send CR
		self.uart.write( bytes([26]) ) # Send a Ctrl-Z
		self._read_response( '', timeout_ms=5000, callback=__scan_response )

		return _r

	@property
	def has_sms( self ):
		""" Has received SMS (return the number of SMS)"""
		return len( self.rec_sms )

	def read_sms( self, slot, delete=True ):
		""" Read a received SMS in the given slot and delete it from storage
		 	returns an initialized SMS object """
		_r = None
		def __scan_response( _b ):
			nonlocal _r
			if b'+CMGR: ' in _b:
				data =  _b.decode('ASCII').split(': ')[1].split(',') # b'+CMGR: "REC UNREAD","+32496928320","","20/10/04,00:20:15+08"\r\n'
				_r = SMS()
				_r.sender = data[1].strip('"')
				_r.send_date = "%s %s" % (data[3].strip('"'), data[4].replace('\r\n','').strip('"'))
				return -1
			if _r: # If initialized then we are receiving the message content in the callback
				_s = ''
				for byte in _b:
					if byte in (13,10):
						continue
					try:
						_s += chr(byte)
					except:
						pass
				_r.lines.append( _s )

			return -1

		self._config_sms_mode()
		self.send_then_read( 'AT+CMGR=%i' % slot, callback=__scan_response )
		if _r and delete: # If we have a message content --> Delete message in memory
			self.send_then_read( 'AT+CMGD=%i' % slot )
			# Remove it from the Received SMS list
			self.rec_sms.remove( slot )
		return _r

	@property
	def stored_sms( self ):
		""" Extract a list of slot id of SMS still stored into the SIM memory """
		_r = []
		def __scan_response( _b ):
			nonlocal _r
			if b'+CMGL: ' in _b:
				_r.append(  int( _b.decode('ASCII').split(': ')[1].split(',')[0] )  ) # b'+CMGL: 4,0,"",22\r\n'
				return -1

		self._config_sms_mode()
		self.send_then_read( 'AT+CMGL="ALL"', timeout_ms=10000, callback=__scan_response )
		return _r

	def delete_sms( self, slot ):
		""" delete a SMS from storage """
		self.send_then_read( 'AT+CMGD=%i' % slot )
