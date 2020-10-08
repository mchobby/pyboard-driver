# Check the activity status (ready, ready ringing, phone call) and
# MAKE A PHONE CALL, wait 20 secs, then Hang-up and exit example
# IF the callee hangs-up prematurely THEN we restart phone call!
#
# set debug=True to see all messages exchanges with the modem
#
# See Project: https://github.com/mchobby/pyboard-driver/tree/master/sim-modem
#
from machine import UART, Pin
from smodem import *
import time

PIN_CODE = '1234'		  # <<<<< MODIFIER ICI !
PHONE    = '+3249692xxxx' # Phone number to call

# UART and PowerPin to SIM Module
# Will be reconfigured by SimModem
uart = UART(1) # X9, X10 on Pyboard
pwr = Pin('Y3') # Power On Pin

m = SimModem( uart, pwr_pin = pwr, pin_code=PIN_CODE )
m.debug = False
print( 'debug: %s' % m.debug )

# activity status as TEXT
AS_TEXT = {AS_READY : 'Ready', AS_UNKNOWN : 'Unknown', AS_RINGING : 'Ringing', AS_CALL : 'Call in progress' }

iter = 0
t_calling = None # Time when the phone has been picked up
print( "Status: %s" % AS_TEXT[m.activity_status] )
print( "Activating....")
m.activate() # Activate / reinit the Modem
while True:
	status = m.activity_status
	print( "Iteration %4i, Status: %s" % ( iter, AS_TEXT[status]) )

	if (t_calling == None) and (status == AS_READY):
		print( "Calling %s (will ends in 60 secs)" % PHONE )
		m.call( PHONE )         # make voice call
		t_calling = time.time() # record start of call time

	# If the Callee HANGS, the SIM will takes 40 secs to return to AS_READY

	if t_calling and (status == AS_CALL): # can also test m.has_call
		# wait 60 seconds before hangup
		if (time.time()-t_calling) > 60:
			print( "Hangup call!")
			m.hangup() # Hangup voice call
			break # Exit the loop

	# IF callee hangs up THEN activity returns to Zero (will takes about 40 sec)
	if (t_calling) and (status==AS_READY):
		print( 'Hey the callee did hang-up! I wonna call it again...' )
		if (time.time() - t_calling) > 80: # Wait a 40 sec before recalling
			t_calling = None # Set it to 0 to restart a call
	iter += 1
	time.sleep(0.5)

print( "That's all Folks!")
