# Establish a Raw Communication with the SIMCom module throught the UART
#
# See Project: https://github.com/mchobby/pyboard-driver/tree/master/sim-modem
#

from machine import UART, Pin
import time

p = Pin( 'Y3', Pin.OUT, value=True )
# Pyboard (TX=X9, RX=X10)
uart = UART( 1, baudrate=9600, timeout=3000)

# Start SIM800 module by pulsing PWRKEY low for for 1 sec
print( 'POWER UP' )
p.value( False )
time.sleep(1)
p.value( True )
time.sleep(3)

# Send 3 AT command to stuluate autobaud detection
print( 'Training auto-baud detect' )
for i in range(3):
	uart.write( "AT"+chr(13)+chr(10) )
	time.sleep_ms(300) # Wait for OK
# Pump the OK response
s = uart.readline()
while s:
	s = uart.readline()


def send_command( uart, command ):
	print( '--> %s' % command )
	uart.write( command )
	uart.write( chr(13) )
	uart.write( chr(10) )

def read_result( uart ):
	""" read from uart until timeout or until OK """
	s = uart.readline()
	while s:
		print( '<-- %s' % s )
		if 'OK' in s:
			return True # OK received
		s = uart.readline()
	return False # Timeout received

def send_then_read( command ):
	global uart
	send_command( uart, command )
	r = read_result( uart )
	if r:
		print( 'OK received :-)' )

send_then_read( 'AT+CGMI' )
send_then_read( 'AT+CGMM' )
send_then_read( 'AT+CPIN=1427' )
send_then_read( 'AT+CNET' )
