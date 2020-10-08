# Connect the Network and read every received SMS
#
# Debug may be activated to see all messages exchanges with the modem
#
# See Project: https://github.com/mchobby/pyboard-driver/tree/master/sim-modem
#
from machine import UART, Pin
from smodem import SimModem, AS_READY
import time

PIN_CODE = '1234'  # <<<<< MODIFIER ICI !

# UART and PowerPin to SIM Module
# Will be reconfigured by SimModem
uart = UART(1) # X9, X10 on Pyboard
pwr = Pin('Y3') # Power On Pin, use "S18" for PYBStick

m = SimModem( uart, pwr_pin = pwr, pin_code=PIN_CODE )
m.debug = True

r = m.activate() # Activate / reinit the Modem
print( 'Modem initialized!' )

# Wait Modem to be ready
m.wait_for_ready()

# Sometime SMS are still stored in the SIM memory OR received by the SIM800 while
#   your software was offline (so you did not catch the "Unsollicited Result Code")
#
# Here is the way to read then and drop them before overflowing the SMS slot memory
print( '==[ Display stored SMS ]=============================================' )
print( '' )
stored = m.stored_sms
for id in stored:
	sms = m.read_sms( id, delete=False ) # Must be deleted separately because they are not received
	m.delete_sms( id )
	print( 'Sender : %s' % sms.sender )
	print( 'Time   : %s' % sms.send_date )
	for line in sms.lines:
		print( line )
	print( '-'*40 )


# Here how to wait for SMS and read them
print( '' )
print( '==[ Wait for SMS ]===================================================' )
print( '' )
while True:
	m.update()
	if m.has_sms:
		for id in m.rec_sms:
			sms = m.read_sms( id, delete=True ) # Delete it from the SMS Store
			print( 'Sender : %s' % sms.sender )
			print( 'Time   : %s' % sms.send_date )
			for line in sms.lines:
				print( line )
			print( '-'*40 )


print( "That's all folks" )
