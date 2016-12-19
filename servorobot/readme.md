# Description 
## Doggy 
![Doggy Project](https://github.com/mchobby/pyboard-driver/blob/master/servorobot/images/DOGGY/Doggy-Intro.png "Doggy Project")

ENG: Doggy is a Robot built with 4 paws of 2 servo each. [This project fully documented on the mchobby wiki](https://wiki.mchobby.be/index.php?title=Hack-micropython-ServoRobot) (in french]

FR: Doggy est un Robot constitué de 4 pattes ayant 2 servo chacune. [Ce projet est completement documenté sur le wiki de MCHobby](https://wiki.mchobby.be/index.php?title=Hack-micropython-ServoRobot)

## Shopping List / Liste d'achat
* [MicroPython PyBoard](https://shop.mchobby.be/micro-python/570-micropython-pyboard-3232100005709.html)
* [PWM Driver/Controler](https://shop.mchobby.be/breakout/89-adafruit-controleur-pwm-servo-16-canaux-12-bits-i2c-interface-pca9685-3232100000896-adafruit.html)
* 4x [Patte à 2 servo / Paws with 2 servo](https://shop.mchobby.be/moteur/913-allbot-patte-2-servo-vr012-3232100009134-velleman.html)

## Building / Assembler
ENG: [Doggy building instruction are available on our wiki...](https://wiki.mchobby.be/index.php?title=Hack-micropython-ServoRobot-ASM)

FR: [Les instructions de montage de Doggy sont disponibles sur notre wiki...](https://wiki.mchobby.be/index.php?title=Hack-micropython-ServoRobot-ASM)

## Wiring / Raccordement
ENG: [The pyboard and PWM driver wiring is available on our wiki](https://wiki.mchobby.be/index.php?title=Hack-micropython-ServoRobot-Brancher)

FR: [Les raccordements de la PyBoard et du contrôleur PWM est disponible sur notre wiki](https://wiki.mchobby.be/index.php?title=Hack-micropython-ServoRobot-Brancher)

## Using / Utiliser
ENG: After the installation process (see here under), you can inspect the various samples available in this GitHub.

FR: Une fois l'installation terminée (voyez [les notes d'installation sur notre wiki](https://wiki.mchobby.be/index.php?title=Hack-micropython-ServoRobot-servorobot-installer) ), vous pourrez consulter les exemples dans les sources et [la documentation de ces exemples sur GitHub](https://wiki.mchobby.be/index.php?title=Hack-micropython-ServoRobot-Tester)

![Anatomie de Doggy](https://github.com/mchobby/pyboard-driver/blob/master/servorobot/images/DOGGY/DOGGY-4PAW-8SERVOS-ASMBETA-05c.jpg "Anatomie de Doggy")

# Install / Installation

## MicroPython 1.8+ 
ENG: You will need to upgrade your PyBoard firmware to the version 1.8 (or more recent).

FR: Il sera nécessaire de réaliser une mise-à-jour du Firmware Micropython à la version 1.8 (ou plus récent). Voyez [notre tutoriel sur la mise-à-jour du Firmware](https://wiki.mchobby.be/index.php?title=MicroPython.Pyboard.mise-a-jour).

## Libraries / bibliothèques 
ENG: You will need the following source files (from this git in pyboard-driver/pca9685/ ). 
copy them in the root path of your pyboard.

FR: Vous aurez besoin des fichiers suivants (disponibles sur ce git dans pyboard-driver/pca9685/ ).
Copiez les dans le répertoire principal de votre PyBoard

* pca9685.py
* servoctrl.py

ENG: We would also need the following files (from this git in pyboard-driver/servorbot/ ).

FR: Nous aurons également besoin des fichiers suivants (depuis ce git dans pyboard-driver/servorbot/ ).

* servobot.py
* The robot file depending on your model 
 * doggy.py - for Doggy Robot - 4 paws 2 servo each
 * spidy.py - for Spidy Robot - 6 paws 3 servo each 
