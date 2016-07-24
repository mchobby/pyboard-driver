Motor-Skin 
==========
![Motor-Skin](https://github.com/mchobby/pyboard-driver/blob/master/motorskin/MOTOR-SKIN-V1.0-04.JPG "Motor-skin")

Chers amis Francophone, une version Frnaçaise de ce fichier est disponible dans readme-fr.md

Dear english friends, this file is here for you.

About
-----
Here I'll put some libraries that can be useful to drive motor skin.

The aim of motor-skin is to place wheels on a PyBoard to make it move around. 

Please support us, our free translations and projects (freely available on wiki.mchobby.be) by buying your material on shop.mchobby.be 

You can redistribute it and/or modify the code found in this repository
under the terms of the GNU GPLv3 license detailed above.

Wiki, Wiring, Shop
------------------
Project information, wiring, recommandation are available on our wiki
* __TODO__

The material list and link to the shop (France & Belgium)
* https://shop.mchobby.be/micro-python/918-pyboard-motor-skin-3232100009189.html
* https://shop.mchobby.be/micro-python/919-pyboard-a-roulette-3232100009196.html

Installing a library:
---------------------
simply copy the '.py' files listed under the "motorskin" folder into the root directory of your PYFLASH PyBoard drive.

Once done, you can use the regular python import statement to use the library into your own scripts.

Libraries
----------
All the libraries are stored under the libraries directory which is subdivided depending on the peripherals/sensors you need to handle.

* __motorskin\hbridge.py__ : Library HBridge for a single H-Bridge (1 motor control) and DualHBridge (2 motors control).
 * Quite good to manage a L293D
 * Both classes contains basic move method (forward, backward, halt) with speed management.
 * DualHBridge class already manage path derivation due to the motors not being exactly identicals 
* __motorskin\motorskin.py__ : Library with MotorSkin extending DualHBridge class to control a 2 dual hbridge and the Ultrasonic sensor 
* __motorskin\r2wheel.py__ : Library with Robot2Wheel extending MotorSkin class to control a 2 wheel (dc motor) robot plateform.
 * Implement turn() method with RIGHT_ROTATE, LEFT_ROTATE, RIGHT_BEND, LEFT_BEND
 * Implement the more convenient right() and left()
 * Can switch forward/backward by code for each motor (manage from code instead of re-wiring the motor)
 * Can switch right/left motor by code (instead of re-wiring the motors)
* __motorskin\ultrasonic.py__ : Library for the HC-SR04 Ultrasonic distance sensor (by Sergio Conde Gómez, GPL V3, see the file header for more details)

History
-------
The motor-skin is the result of the "PyBoard-à-roulette" project that you can find [here](https://wiki.mchobby.be/index.php?title=MicroPython-Accueil#PyBoard_.C3.A0_roulette)

The initial project was conducted in several steps depending on request, contribution and implemented ideas.

License: GPL v3
---------------
Copyright 2016 - Meurisse D <info[at]mchobby[dot]com> - http://shop.mchobby.be

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

