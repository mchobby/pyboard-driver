# Connect the Network and sens a SMS to the destinatory
#
# Debug may be activated to see all messages exchanges with the modem
#
# See Project: https://github.com/mchobby/pyboard-driver/tree/master/sim-modem
#
from machine import UART, Pin
from smodem import SimModem, AS_READY
import time

PIN_CODE = '1234'      # <<<<< MODIFIER ICI !
PHONE = '+3249692xxxx' # Phone to send the SMS to

# UART and PowerPin to SIM Module
# Will be reconfigured by SimModem
uart = UART(1) # X9, X10 on Pyboard
pwr = Pin('Y3') # Power On Pin

m = SimModem( uart, pwr_pin = pwr, pin_code=PIN_CODE )
m.debug = False

r = m.activate() # Activate / reinit the Modem
print( 'Modem initialized!' )

# Wait Modem to be ready
m.wait_for_ready()

mr = m.send_sms( PHONE, 'Hello world!\r\nFrom MicroPython' )
if mr:
	print( "Message sent. Message_reference: %i" % mr )
else:
	print( "Message not sent (or Message_reference not captured)" )

# Using Latin chars
mr = m.send_sms( PHONE, 'Bénédicte est la maîtresse à demeure :-)\r\nMerci MicroPython & NADHAT-GSM' )
if mr:
	print( "Message sent. Message_reference: %i" % mr )
else:
	print( "Message not sent (or Message_reference not captured)" )

# Pump the message during 10 seconds
print( "That's all folks" )
