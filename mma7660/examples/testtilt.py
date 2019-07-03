import time
import pyb

acc = pyb.Accel()
while True:
	tilt = acc.tilt()
	shake = 'SHAKE' if tilt & (1<<7) else ''
	alert = 'Alert' if tilt & (1<<6) else ''
	tap   = 'TAP'   if tilt & (1<<5) else ''
	# Lying on Back or Front
	_BaFro = tilt & 0b11
	if _BaFro == 1:
		bafro = 'lying on FRONT'
	elif _BaFro == 2:
		bafro = 'lying on BACK'
	else:
		bafro = '' # Undetermined state
	# Position
	_PoLa = (tilt & 0b11100) >> 2
	if _PoLa == 1:
		pola = 'Landscape (to left)'
	elif _PoLa == 2:
		pola = 'Landscape (to right)'
	elif _PoLa == 5:
		pola = 'Vertical position (inverted)'
	elif _PoLa == 6:
		pola = 'Vertical position (normal)'
	else:
		pola = '' # undetermined
	print( ', '.join([shake,alert,tap,bafro,pola]) )
	time.sleep(0.1)
