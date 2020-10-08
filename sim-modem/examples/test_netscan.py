# Scan operator networks available around the SIMCom
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
m.debug = False
print( 'debug: %s' % m.debug )
m.activate() # Activate / reinit the Modem
for i in range( 5 ):
	print( '-- Scan %i/5 ---------------------------------------------------' % (i+1) )
	print( 'Scaning can takes up to 45s')
	networks = m.scan_networks()
	for network in networks:
		print( network )

# Pump the message during 10 seconds
print( "That's all folks" )
