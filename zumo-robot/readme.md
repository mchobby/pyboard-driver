[This file also exists in ENGLISH here](readme_ENG.md)

# ROBOT ZUMO V1.2 sous MicroPython avec la Pyboard originale

Ce portage MicroPython concerne le [Robot Zumo de Pololu](https://www.pololu.com/product/2510). Ce robot peut être acheté en pièce détachées ou en version pré-assemblé (comme sur la photo). Ce robot est conçu pour un carte Arduino Uno __MAIS NOUS ALLONS LE FAIRE FONCTIONNER avec une carte MicroPython Pyboard__.

Le Zumo robot est composé d'un châssis, deux moteurs, un shield pour Arduino, une lame en acier inoxydable de 0,9mm d'épaisseur montée à l'avant du châssis lui permettant ainsi de pousser les objets et adversaires aux alentours, d'une matrice de capteurs infrarouge spécialement conçue pour le suivi de lignes.

Vous pouvez consulter les liens suivants pour plus de détails à propos du robot Zumo: [Robot Zumo @ MCHOBBY](https://shop.mchobby.be/fr/prototypage-robotique-roue/448-robot-zumo-pour-arduino-assemble-moteurs-3232100004481-pololu.html) ou [Robot Zumo @ Pololu](https://www.pololu.com/product/2510)

![ROBOT ZUMO](docs/_static/robotzumo2.jpg)

Ce robot Zumo est initialement programmé à l'aide d'un Arduino Uno ou d'un Arduino Leonardo.
Dans ce projet le robot Zumo est programmé grâce à un [adaptateur Pyboard vers Zumo](https://shop.mchobby.be/product.php?id_product=2040).

Toutes les bibliothèques et exemples en Arduino fournis par [Pololu](https://www.pololu.com) ont été portés sous Micropython.

# Brancher

## Adaptateur Pyboard vers Zumo

L'adaptateur [Pyboard-Zumo](https://shop.mchobby.be/product.php?id_product=2040) permet de connecter directement un carte MicroPython Pyboard sur le Zumo Robot de Pololu.

![Carte Pyboard Zumo](docs/_static/pyboard-zumo.jpg)

L'adaptateur Pyboard-Zumo propose également:
* un réplicat du bouton Reset
* un réplicat du bouton Utilisateur
* deux connecteurs Servo-Moteur disponibles (GND, 7.45V, Signal)
* deux connecteurs Servo supplémentaires (si vous n'utilisez pas le capteur de ligne)
* un connecteur UEXT (IDC 10 broches, 2.54mm) avec:
 * Alimentation 3.3V
 * bus SPI(2)
 * bus I2C(2)
 * UART(1)
 * Voir la gamme [UEXT @ Olimex](https://www.olimex.com/Products/Modules/) et [UEXT @ MCHobby](https://shop.mchobby.be/fr/138-uext) .
* Un régulateur de tension 5V (optionnel) renvoyée vers la broche 5V du Zumo.

__ALIMENTATION DES SERVOS:__ la broche d'alimentation sur les connecteurs Servo correspond à la tension VIN produite par le régulateur boost du Zumo Robot. Cette tension est d'environ 7.45V. Il faut donc utiliser des Servo-moteurs 8V qui ne charge pas trop le régulateur (pas question de soulever du poids).

Le [schéma de l'adaptateur est disponible ici](docs/_static/schematic.jpg)

## Connexions DIY
Vous pouvez aussi réaliser les connexions grâce [au schéma de l'adaptateur](docs/_static/schematic.jpg). Ce n'est peut être pas la plus belle réalisation mais reste pleinement fonctionnel.

![ROBOT ZUMO](docs/_static/robotzumo.jpg)

Avec raccordement DIY, vous aurez besoin d'utiliser un [régulateur 5V S7V7F5 de Pololu](https://www.pololu.com/product/2119) pour générer 5V à partir de la tension VIN obtenue depuis les piles du shield Zumo robot. Suivez ce [schéma de distribution d'alimentation](https://github.com/mchobby/pyboard-driver/blob/master/UNO-R3/docs/_static/power-distribution.jpg) repris du projet PYBOARD-UNO-R3. La carte PYBOARD-UNO-R3 dispose, elle, de son propre convertisseur de type buck.

Voyez le schéma de raccordement [Pyboard vers Zumo](docs/_static/schematic.jpg) ou du project [PYBOARD-UNO-R3](https://github.com/mchobby/pyboard-driver/tree/master/UNO-R3) pour les raccordements des broches-pyboard vers les broches-arduino.

# Bibliothèques

Les bibliothèque MicroPython nécessaire doivent être copiées sur la carte MicroPython avant de tester l'adapteur Pyboard-Zumo (ou votre propre adaptateur).

Les bibliothèques ont été portées depuis le code source Arduino produit par Pololu. __Les fonctions/méthodes ont conservées les conventions de nommage C pour faciliter la transition des utilisateurs Arduino vers MicroPython__.

* [zumoshield.py](lib/zumoshield.py) : commande moteur et suiveur de ligne du Zumo
* [pushbutton.py](lib/pushbutton.py) : outil de manipulation de bouton
* [zumobuzzer.py](lib/zumobuzzer.py) : Support du Zumo buzzer
* [lsm303.py](lib/lsm303.py) : Support de l'accéléromètre/magnétomètre 3 axes
* [L3G.py](lib/L3G.py) : Support Gyroscope 3 axes
* [qtrsensors.py](lib/qtrsensors.py) : support général des suiveurs de ligne de Pololu

# Tester

## Etat par défaut du Zumo

Lors de la mise en route de la Pyboard, les broches sont configurées en entrées, ce qui a pour effet de faire tourner le deux moteurs.

Cas qui risque de se présenter lorsque l'on branche la Pyboard sur un ordinateur puis que l'on mette le Zumo sous tension.

Il faut donc initialiser les sorties de Pyboard le plus vite possible pour éviter aux moteurs de se mettre en route. Cela peu se faire à l'aide des deux lignes suivantes saisie sur le session REPL (ou placée au début du fichier `main.py`).

``` python
from zumoshield import ZumoMotor
motors = ZumoMotor()
```

Voyez le script [examples/main.py](examples/main.py) qui contient le code minimaliste pour initialiser rapidement le Zumo.

## Piloter les moteurs

Placer des piles dans le Zumo puis placer le commutateur en position "ON".

Les LEDs a l'arrière du Zumo doivent s'allumer.

![Moteurs du Zumo](docs/_static/motors.jpg)

Saisir le code suivant dans une session REPL:

``` python
from zumoshield import ZumoMotor
motors=ZumoMotor()
# Marche avant
motors.setSpeeds( 200, 200 ) # -400..0..400
# Stop
motors.setSpeeds( 0, 0 ) # -400..0..400
# Marche arrière
motors.setSpeeds( -100, -100 ) # -400..0..400
motors.setSpeeds( 0, 0 ) # -400..0..400
```

L'exemple suivant montre comment inverser le sens de rotation du moteur droit pour faire tourner le Zumo à droite.

``` python
from zumoshield import ZumoMotor
from time import sleep
motors=ZumoMotor()
# Marche avant
motors.setSpeeds( 100, 100 ) # -400..0..400
# Tourner à droite
motors.flipRightMotor( True )
motors.setSpeeds( 100, 100 ) # Indiquer la vitesse de rotation
# Attendre une seconde
sleep( 1 )
# Reprendre la marche avant (en indiquer la vitesse)
motors.flipRightMotor( False )
motors.setSpeeds( 100, 100 )
sleep( 1 )
# Stop
motors.setSpeeds( 0, 0 ) # -400..0..400
```

La classe `ZumoShield` permet également d'accéder directement aux moteurs.

``` python
from zumoshield import ZumoShield
zumo = ZumoShield()
zumo.motors.setSpeeds( 100, 100 ) # -400..0..400
zumo.motors.stop()
```

## Buzzer

Voici quelques exemples extraient de [mazesolver.py](examples/mazesolver.py) pour jouer une suite de notes.

La syntaxe est décrite dans document de Pololu pour la méthode [Zumo32U4Buzzer::play()](https://pololu.github.io/zumo-32u4-arduino-library/class_zumo32_u4_buzzer.html)

``` python
from zumobuzzer import PololuBuzzer
from time import sleep

buzzer=PololuBuzzer()
buzzer.play("c8")
sleep(2)
buzzer.play(">g32>>c32")
sleep(2)
buzzer.play("l16 cdegreg4")
sleep(2)
buzzer.play(">>a32")
sleep(2)
buzzer.play(">>a32")
```
Il est également possible de jouer directement de notes avec `playNote()` en précisant la Note, sa durée en ms et le volume (0-15) de celle-ci.

Exemple issus de [borderdetect.py](examples/borderdetect.py) .

``` python
from zumobuzzer import PololuBuzzer, NOTE_G
buzzer = PololuBuzzer()

for x in range(3):
		time.sleep(1)
		# Note(octave), Durée, Volume
		buzzer.playNote(NOTE_G(3),200,15)
time.sleep(1)
buzzer.playNote(NOTE_G(4),500,15)
time.sleep(1)
```

Pour finir, la classe `ZumoShield` permet d'accéder directement au buzzer.

``` python
from zumoshield import ZumoShield
zumo = Zumoshield()
zumo.buzzer.play(">g32>>c32")
```

## LED du Zumo

Le Zumo est équipé d'une LED utilisateur orange marquée "LED 13".

![LED du Zumo](docs/_static/LEDs.jpg)

Cette LED est visible sur le côté droit du Zumo.

``` python
from machine import Pin
from zumoshield import LED_PIN
from time import sleep

led = Pin(LED_PIN, Pin.OUT) # Y6

# Allume la LED sur le côté droit du Zumo
led.value(1)
sleep(2)
led.value(0)
```

La classe `ZumoShield` permet également d'accéder directement à la LED.

``` python
from zumoshield import ZumoShield
zumo = ZumoShield()
zumo.led.on()
zumo.led.off()
```

## Bouton poussoir pyboard

La carte Pyboard-to-Zumo dispose d'un bouton utilisateur qui est monté en parallèle sur le bouton utilisateur de la pyboard.

``` python
import pyb
sw = pyb.Switch()
while True:
	if sw.value():
		print( "Pressed" )
	else:
		print( "..." )
```

pour plus d'information sur la classe `Switch`, référez vous à la [documentation MicroPython officielle](https://docs.micropython.org/en/latest/pyboard/tutorial/switch.html) .

## Bouton poussoir Zumo

Le bouton poussoir du Zumo (à côté de l'interrupteur On/OFF) est raccordé sur la broche "Y7" de la Pyboard. L'entrée est branchée à la masse lorsque ce bouton est pressé.

![Zumo button](docs/_static/zumo_button.jpg)

Le bouton poussoir peut être lu directement avec l'aide des classes `Pin` et `Signal`.

La classe `Signal` sert a inverser la logique du signal.

``` python
from machine import Pin, Signal
from zumoshield import BUTTON_PIN
pin = Pin( BUTTON_PIN, Pin.IN, Pin.PULL_UP )
btn = Signal( pin, invert=True )
while True:
	if btn.value():
		print( "Pressed" )
	else:
		print( "..." )
```

La bibliothèque [pushbutton.py](lib/pushbutton.py) propose la classe `Pushbutton` permettant de détecter l'état enfoncé ou relâché d'un bouton.

``` python
from pushbutton import Pushbutton
from zumoshield import BUTTON_PIN

# Bouton sur le Zumo
btn = Pushbutton( BUTTON_PIN )

print( "Presser et relacher le bouton Zumo" )
btn.waitForButton()
print( "c est fait" )
```

Il est aussi capable d'accéder au bouton par l'intermédiaire de la classe `ZumoShield` (de la bibliothèque [lib/zumoshield.py](lib/zumoshield.py)).

``` python
from zumoshield import ZumoShield

zumo = ZumoShield()
print( "Presser et relacher le bouton Zumo" )
zumo.button.waitForButton()
print( "c est fait" )
```
## Suiveur de ligne

Le suiveur de ligne présent à l'avant du Zumo permet de détecter la présente d'une ligne noir (largeur de 15mm).

Le script suivant active les LEDs infrarouges puis effectue une lecture récurrente des récepteurs Infrarouge.

![position de la ligne](docs/_static/readLine.jpg)

``` python
# Arrêter les moteurs
from zumoshield import ZumoMotor
mot = ZumoMotor()

# Tester le capteur infrarouge
#
import time
from zumoshield import ZumoReflectanceSensorArray
ir = ZumoReflectanceSensorArray()

# déplacer le zumo au dessus de la ligne durant
# cette calibration en 10 étapes. Permet d'évaluer le
# contraste noir/blanc.
#
for i in range(10):
	print( "Calibrate %i / 10" % (i+1) )
	ir.calibrate()
	time.sleep(0.5)

# Lecture de la position de la ligne
#
while True:
    sensors = [0 for i in range(6)]
    # Avec le Zumo dirigé vers l'avant
    #   Valeur de 500 à 4500 : ligne de gauche à droite.
    #   valeur 2500 : ligne pile au centre
    #   valeur 0 : ligne hors capteur à gauche
    #   valeur 5000 : ligne hors capteur à droite
    position = ir.readLine( sensors )
    print( 'Line position: ', position )
    time.sleep( 1 )
```

La classe `ZumoShield` permet également d'accéder directement aux capteurs infrarouges. Le code peut être réécrit comme suit:

``` python
# Arrêter les moteurs
from zumoshield import ZumoShield
zumo = ZumoShield()

# Calibration
for i in range(10):
	print( "Calibrate %i / 10" % (i+1) )
	zumo.ir.calibrate()
	time.sleep(0.5)

# Lecture position ligne
while True:
    sensors = [0 for i in range(6)]
    position = zumo.ir.readLine( sensors )
    print( 'Line position: ', position )
    time.sleep( 1 )
```

## Lecture du magnétomètre

Le code de [test_mag.py](examples/test_mag.py), repris ci-dessous, effectue une lecture basique du magnétomètre. Il est extrait de l'exemple [compass.py](examples/compass.py) qui permet de calculer une orientation et faire tourner le Zumo en carré.

``` python
from zumoshield import ZumoShield
from machine import I2C
from lsm303 import LSM303,MAGGAIN_2,MAGRATE_100
import time

zumo = ZumoShield() # Will stop motors
i2c = I2C(2)

lsm = LSM303(i2c)
lsm.enableDefault()
lsm.mag_gain = MAGGAIN_2  # Magnetometer gauss avec high resolution
lsm.mag_rate = MAGRATE_100 # magnetometre data rates

while True:
	# read magnetic and accelerometer
	lsm.read()
	# Access the mangnetic vector.
	print( 'x', lsm.m.x, 'y', lsm.m.y )
	time.sleep( 0.300 )
```

Ce qui produit les résultats suivants:

```
MicroPython v1.16-92-g98c570302-dirty on 2021-07-16; PYBv1.1 with STM32F405RG
Type "help()" for more information.
>>>
>>> import test_mag
x 16107 y -9128
x 16099 y -9124
x 16095 y -9131
x 16093 y -9148
x 16086 y -9134
x 16082 y -9122
x 16097 y -9145
x 16087 y -9145
x 16095 y -9153
....
x 13808 y -7192
x 13804 y -7186
x 13829 y -7193
x 13811 y -7187
x 13788 y -7193
x 13795 y -7207
x 13773 y -7193
x 13807 y -7197
```

Qui peuvent être mis en corrélation avec les axes X,Y du Zumo (l'axe Z peut être ignoré à cause de la masse des piles).

![Zumo Axis](docs/_static/zumo-axis.jpg)

__Note:__ Il est également possible d'accéder aux données du magnétomètre (en microtesla) via la propriété `magnetic`. Voyez l'exemple [examples/test_mag2.py](examples/test_mag2.py) .

``` python
lsm = LSM303(i2c)
lsm.enableDefault()
lsm.mag_gain = MAGGAIN_2
lsm.mag_rate = MAGRATE_100

while True:
	print( 'x: %f, y: %f, z: %f in MicroTesla' % lsm.magnetic )
	time.sleep( 0.300 )
```

__Note:__ Etant donné les gammes de valeurs, il est préférable de faire une calibration du capteur en faisant tourner la Zumo sur lui-même. Cela permet de détecter les minima et maxima pour chaque axe et de pouvoir normaliser les valeurs lues sur le capteur (ex: entre -100 et +100). Voyez l'exemple [compass.py](examples/compass.py).

## Acceléromètre

La lecture de l'accéléromètre selon Pololu est abordé dans l'exemple [test_acc.py](examples/test_acc.py). Ces données ont permis de créer [test_knock.py](examples/test_knock.py) pour détecter les chocs sur le Zumo (que l'on peut produire en frappant dessus). __Cependant__, prenez le temps de parcourir le second exemple dans cette section qui produit un résultat plus "naturel".

``` python
from zumoshield import ZumoShield
from machine import I2C
from lsm303 import LSM303
import time

zumo = ZumoShield() # Will stop motors
i2c = I2C(2)
lsm = LSM303(i2c)
lsm.enableDefault()

while True:
	# read magnetic and accelerometer
	lsm.read()
	# Access the accelerometer vector.
	print( 'x', lsm.a.x, 'y', lsm.a.y )
	time.sleep( 0.300 )
```

ce qui produit le résultat suivant:

```
MicroPython v1.16-92-g98c570302-dirty on 2021-07-16; PYBv1.1 with STM32F405RG
Type "help()" for more information.
>>>
>>> import test_acc
x -241 y -23
x -236 y -16
x -233 y -68
x -223 y -81
x 1110 y -7073 <--- Knocked on the right side
x -309 y -35
x -242 y -69

```

L'exemple [test_acc2.py](examples/test_acc2.py) permet de relever l'accélération en m/s^2.

``` python
from zumoshield import ZumoShield
from machine import I2C
from lsm303 import LSM303
import time

zumo = ZumoShield() # Will stop motors
i2c = I2C(2)

lsm = LSM303(i2c)
lsm.enableDefault()

while True:
	print( 'x: %f, y: %f, z: %f in m/s^2' % lsm.acceleration )
	time.sleep( 0.300 )
```

Ce qui produit avec le résultat suivant dans la session REPL lorsque le Zumo est a plat sur un bureau.

La valeur 10 pour l'axe Z correspond au vecteur G de l'attraction terrestre (9.81 m/s^2).

```
MicroPython v1.16-92-g98c570302-dirty on 2021-07-16; PYBv1.1 with STM32F405RG
Type "help()" for more information.
>>>
>>> import test_acc2
x: -0.176520, y: -0.039227, z: 10.689249 in m/s^2
x: -0.176520, y: -0.029420, z: 10.689249 in m/s^2
x: -0.166713, y: -0.058840, z: 10.699056 in m/s^2
x: -0.166713, y: -0.039227, z: 10.689249 in m/s^2
```
En orientant le Zumo dans différentes positions, il est possible de constater la présence des effets de l'attraction terrestres sur les autres axes x et y.

Donner des chocs dans dans les axes X et Y permet de constater des soubresauts dans les lectures d'accélération des axes X et Y.  

# Les exemples ZUMO de Pololu en MicroPython

Les exemples proposés ci-dessous ont étés portés depuis le code Arduino de Pololu.

## Détection des bords

L'exemple [examples/borderdetect.py](examples/borderdetect.py) est un programme ou le robot Zumo ne sors jamais d'un ring. Le ring est une surface blanche un contour noir.

Le capteur infrarouge détecte la différence de couleurs à l'aide de la bibliothèque [qtrsensors.py](lib/qtrsensors.py). Le noir est peu réfléchissant et le blanc est fortement réfléchissant. En fonction de ces informations les moteurs vont avancer, reculer ou tourner.

![PHOTO RING ZUMO](docs/_static/zumo_robot_ring.jpg)

## Suiveur de ligne LineFollower

Le script [examples/line_follower.py](examples/line_follower.py) permet au Zumo de suivre une ligne noir de 15 à 20mm de large (meilleurs résultats pour 20mm)

Cet exemple exploite les classes [QTRsensors](https://github.com/mchobby/pyboard-driver/tree/master/Zumo-Robot/lib/qtrsensors.py) et [ZumoMotor](https://github.com/mchobby/pyboard-driver/tree/master/Zumo-Robot/lib/zumoshield.py).

Voir cette [vidéo réalisée à la Maker Fair Paris 2019](https://youtu.be/VHN83aYCH8Q) (YouTube)

## Boussole

L'exemple [examples/compass.py](examples/compass.py) fait tourner le robot Zumo en carré.

Grâce au magnétomètre du LSM303 le robot Zumo tourne 4 fois de 90 degrés en utilisant le champs magnétique terrestre pour se repérer.

## Résolution de labyrinthe

![Maze solvering](docs/_static/maze.jpg)

L'exemple [examples/mazesolver.py](examples/mazesolver.py) permet de résoudre un labyrinthe. Ce script n'est pas infaillible mais fonctionne plutôt bien.

## Gyroscope

L'exemple [examples/gyroscope.py](examples/gyroscope.py) permet de tester le gyroscope.

Cet exemple est n'est pas encore certifié.

# Liste d'achat
* [Zumo Robot pour Arduino](https://www.pololu.com/product/2510) @ MCHobby
* [Zumo Robot pour Arduino](https://shop.mchobby.be/product.php?id_product=448) @ Pololu
* [__Adaptateur Pyboard vers Zumo__](https://shop.mchobby.be/product.php?id_product=2040) @ MCHobby
* [MicroPython Pyboard](https://shop.mchobby.be/product.php?id_product=570) @ MCHobby
