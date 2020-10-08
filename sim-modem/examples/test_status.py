# Just read the MODEM status and line status
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
REG_STATUS_TEXT = { REG_STATUS_NONE : 'Not registered, Not searching a new operator',
					REG_STATUS_DONE : 'Registered, Home network',
					REG_STATUS_SEARCH : 'Not registered, Searching new operator to register to',
					REG_STATUS_DENIED : 'Registration Denied',
					REG_STATUS_UNKNOWN : 'Unknown',
					REG_STATUS_ROAMING : 'Registered, Roaming' }

URC_STATUS_TEXT = { URC_STATUS_DISABLE : 'Disable Unsollicited Result Code',
					URC_STATUS_ENABLE  : 'Enable Unsollicited Result Code (stat only)',
					URC_STATUS_EXTENED : 'Enable Unsollicited Result Code (stat[,lac,ci] )' }

iter = 0
print( "Status: %s" % AS_TEXT[m.activity_status] )
print( "Activating....")
m.activate() # Activate / reinit the Modem
while True:
	print( '----[Iteration %4i]--------------------------------' % iter )
	print( "Status: %s, callee: %s" % ( AS_TEXT[m.activity_status], m.callee) )
	print( "Mode: %i, format: %i, operator: %s" % m.operator ) # Return a tuple(mode_int,format_int,operator_string)
	print( "Signal Quality: %i dBm" % m.rssi )
	reg_status, urc_status = m.network_registration
	print( "Network Registration Status: %s" % REG_STATUS_TEXT[reg_status] )
	print( "Unsollicited Result Code status: %s" % URC_STATUS_TEXT[urc_status] )
	print( "SIM Serial : %s" % m.sim_serial )
	print( "IMEI serial : %s" % m.imei )
	iter += 1
	time.sleep(5)
