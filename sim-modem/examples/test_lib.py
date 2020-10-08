# Establish a Communication with the SIMCom module via the smodem lib
#
# Debug is activated to see all messages exchanges with the modem
#
# See Project: https://github.com/mchobby/pyboard-driver/tree/master/sim-modem
#
from machine import UART, Pin
from smodem import SimModem
import time

PIN_CODE = '1234'  # <<<<< MODIFIER ICI !

# UART and PowerPin to SIM Module
# Will be reconfigured by SimModem
uart = UART(1) # X9, X10 on Pyboard
pwr = Pin('Y3') # Power On Pin

m = SimModem( uart, pwr_pin = pwr, pin_code=PIN_CODE )
m.debug = True
try:
	r = m.activate() # Activate / reinit the Modem
	if r:
		print( 'Modem initialized!' )
	else:
		print( 'Modem initialization FAILURE!' )
except Exception as err:
	print( "[ERROR] Unexcpected exception on activate()" )
	print( "[ERROR] %s" % err )


def pump( timeout_ms=5000 ):
	""" HELPER: Just pump the messages during timeout_ms """
	global m
	t = time.ticks_ms()
	while time.ticks_diff( time.ticks_ms(), t ) < timeout_ms :
		m.update() # As we are in debug mode, pumped message will be displayed

def send( s, timeout_ms = 3000 ):
	""" HELPER: Send the command to the modem and pump messages until timeout_ms """
	global m
	m.send_then_read( s, timeout_ms )

# Pump the message during 10 seconds
pump()
pump()
print( "That's all folks" )
print( "  Do not hesitate to call send() and pump() for your own AT tests")
