import time
import pyb

acc = pyb.Accel()
while True:
	print( 'x: %3i | y: %3i | z: %3i' % (acc.x(), acc.y(), acc.z()) )
	time.sleep(0.5)
