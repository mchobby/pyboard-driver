# Check the activity status (ready, ready ringing, phone call) and
# PICKUP VOICE CALL for 10 seconds then hang up call
#
# set debug=True to see all messages exchanges with the modem
#
# See Project: https://github.com/mchobby/pyboard-driver/tree/master/sim-modem
#
from machine import UART, Pin
from smodem import *
import time

PIN_CODE = '1234'  # <<<<< MODIFIER ICI !

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
t_pickup = None # Time when the phone has been picked up
print( "Status: %s" % AS_TEXT[m.activity_status] )
print( "Activating....")
m.activate() # Activate / reinit the Modem
while True:
	print( "Iteration %4i, Status: %s, callee: %s" % ( iter, AS_TEXT[m.activity_status], m.callee) )
	if m.is_ringing:
		print( "Pickup phone (will ends in 10 secs)")
		time.sleep( 1 ) # Wait the SIM ressource to be ready
		m.pickup()      # pickup voice call
		t_pickup = time.time() # record start of call time

	if t_pickup: # can also test m.has_call
		# wait 10 seconds before hangup
		if (time.time()-t_pickup) > 10:
			print( "Hangup call!")
			m.hangup() # Hangup voice call
			t_pickup = None # ready for next call

	iter += 1
	time.sleep(0.5)
