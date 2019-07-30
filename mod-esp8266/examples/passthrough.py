import pyb
import select

CR = 13 # Carriage Return \r
LF = 10 # Line Feed \n

def pass_through(usb, uart, debug=False, enforce_crlf=True):
	""" Forward any USB char to Serial (vice-versa) """
	print( "Activating UART<->USB passthrough..." )
	print( "  debug        = %s" % debug )
	print( "  enforce_crlf = %s" % enforce_crlf ) # Send CrLf on serial when Cr received on USB
	print( "press USR button while sending a byte to EXIT")
	print( "Ready!" )
	button = pyb.Switch()
	usb.setinterrupt(-1)
	while not button():
		select.select([usb, uart], [], [])
		if usb.any():
			data = usb.read(256)
			if debug:
				print( 'USB >>> UART: %s' % data )
			uart.write( data )
			if enforce_crlf and (data[len(data)-1] == CR):
				data = b'\n'
				if debug:
					print( 'USB >>> UART: %s' % data )
				uart.write( data )
		if uart.any():
			data = uart.read(256)
			if debug:
				print( 'USB <<< UART: %s' % data )
			usb.write( data )
	print( 'USR exit!' )


# Pyboard's UEXT connector wired the RX/TX on UART(1)
pass_through(pyb.USB_VCP(), pyb.UART(1, 115200), debug=False)
