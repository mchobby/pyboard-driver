##
# Console de pilotage de la plateforme robotique 2 roues avec un Motor-Skin et STDIN (entrée standard)
# Ce logiciel est concu pour ETRE DEMARRE DEPUIS UNE SESSION REPL (Repl via USB ou via Bluetooth ou via port série). 
# Voyez plus loin pour installer un REPL via une connexion série (a Bluetooht serial for instance)
#
# Control console a 2 wheel robotic plateform with a Motor-Skin and the STDIN (standard input) 
# This software is defigned TO BE STARTED FROM an REPL SESSION (Repl over Bluetooth serial, over USB, over Serial. 
# See further how to install the REPL over a serial connexion (a Bluetooht serial for instance)
#
#   http://shop.mchobby.be/product.php?id_product=918
#   http://shop.mchobby.be/product.php?id_product=561
#   http://shop.mchobby.be/product.php?id_product=570
# 
# Voir Tutoriel - See our french and english tutorial
#   https://wiki.mchobby.be/index.php?title=Hack-MotorSkin
#   https://wiki.mchobby.be/index.php?title=Hack-ENG-MotorSkin (coming soon)
#
# Voyez comment brancher un module Bluetooth serie sur votre PyBoard dans le tutoriel suivant
# See how to wire a Serial Bluetooth Module on your Pyboard on the following tutorial
#   https://wiki.mchobby.be/index.php?title=MicroPython-bluetooth 
#
# Copyright 2016 - Dominique Meurisse for MC Hobby SPRL <info (at) mchobby (dot) be>
#
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##
import pyb
import sys
from ultrasonic import Ultrasonic

from pyb import delay, LED
from r2wheel import Robot2Wheel                                             

def speed_control( r2, speed, increment ):
	""" Just control the robot speed between -100 and 100 by increment of -10 or +10 """
	# Going forward or Backward
	# Speed are -100...-50, 0 , +50...+100			
	if (speed+increment) == 0:
		speed = 0
		r2.halt()
	elif -50 <= (speed+increment) < 0:
		if increment > 0:
			speed = 0
			r2.halt()
		else:
			speed = -50
			r2.backward( abs(speed) )
	elif -100 <= (speed+increment) < -50:
		speed = speed + increment 
		r2.backward( abs(speed) )
	elif (speed+increment) < -100:
		speed = -100
		r2.backward( abs(speed))
	elif 0 < (speed+increment) <= 50:
		if increment < 0:
			speed = 0
			r2.halt()
		else:
			speed = 50
			r2.forward( speed )
	elif 50 < (speed+increment) <= 100:
		speed = speed + increment
		r2.forward( speed )
	elif (speed+increment) > 100:
		speed = 100
		r2.forward( speed )

	return speed

def speed_delta_control( r2, speed, speed_delta, increment ):
	""" Control the delta speed between the motors, used for BEND TURNING """
	if abs( speed_delta + increment ) > 50:
		return speed_delta

	if (speed_delta + increment) == 0:
		if speed > 0:
			r2.forward( speed )
		else:
			r2.backward( abs(speed) )
		speed_delta = 0
	elif (speed_delta+increment) > 0: # bending on the right
		r2.turn( Robot2Wheel.RIGHT_BEND, speed=speed, speed2=speed-abs(speed_delta+increment))
		speed_delta = speed_delta + increment
	else: # <0 bending on left
		r2.turn( Robot2Wheel.LEFT_BEND, speed=speed, speed2=speed-abs(speed_delta+increment))
		speed_delta = speed_delta + increment
	return speed_delta


def console( derivative_fix=0 ):
	print( '-'*20 )
	print( 'MotorSkin Interactive Console')
	print( 'q: quit to REPL   - quitter vers REPL')
	print( '')
	print( '8: increase speed - accelerer' )
	print( '2: decrease speed - ralentir' )
	print( '7: going left     - aller a gauche')
	print( '9: going right    - aller a droite')
	print( '4: turn left      - tourner à gauche')
	print( '6: turn right     - tourner à droite')
	print( '5: HALT           - ARRET')
	print( '-'*20)
	print( 'INIT MOTORSKIN')
	l = LED(4)   # LED Bleue / Blue LED
	l.off()
	r2 = Robot2Wheel( derivative_fix=derivative_fix ) 
	r2.halt()

	print( 'READY')
	l.on()
	
	# User standard input to read instruction via the REPL connection.
	# Utiliser l'entrée standard pout lire les insctruction via la connexion REPL
	stdin = sys.stdin
	cmd = ''
	speed = 0
	# Difference of speed between wheel - to have a bend turning
	# Difference de vitesse entre les roues - pour prendre un virage 
	speed_delta = 0  
	while cmd!='q':
		# Blocking read 1 char from stdin
		# Lecture bloquante de 1 caractere sur stdin 
		cmd = stdin.read(1)

		if cmd == 'q':
			pass
		elif cmd == '5': # Halt
			r2.halt()
			speed = 0
			speed_delta = 0
			print('halted')

		elif cmd == '8': # Increase Speed
			if abs(speed_delta)>0: # abort bending
				speed_delta = 0
				speed = speed_control( r2, speed, +0 )
			if r2.state in [Robot2Wheel.RIGHT_ROTATE, Robot2Wheel.LEFT_ROTATE]:
				# stop the rotation... keep current speed
				speed = speed_control( r2, speed, +0 )
			else:
				speed = speed_control( r2, speed, +10 )
			print( 'speed:%i' % speed )

		elif cmd == '2': # Decrease speed
			if abs(speed_delta) >0: # abord bending
				speed_delta = 0
				speed = speed_control( r2, speed, 0 )
			else:
				speed = speed_control( r2, speed, -10 )
			print( 'speed:%i' % speed )

		elif cmd == '9': # Bending (turning) on right
			if speed<50:
				print( 'bending:speed-too-low!')
			else:
				speed_delta = speed_delta_control( r2, speed, speed_delta, +10 )
				print( 'bending:%i @ %i' %(speed, speed_delta) )

		elif cmd == '7': # Bending (turning) on left
			if speed<50:
				print( 'bending:speed-too-low!')
			else:
				speed_delta = speed_delta_control( r2, speed, speed_delta, -10 )
				print( 'bending:%i @ %i' %(speed, speed_delta) )

		elif cmd == '6': # Turning right
			r2.right( speed )
			print( 'right:%i' % speed )

		elif cmd == '4': # turning left
		    r2.left( speed )
		    print( 'left:%i' % speed )



	# End of software
	r2.halt()
	l.off()
	del(r2)
	print( 'BYE' )

