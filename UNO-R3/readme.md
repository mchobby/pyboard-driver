[This file also exists in ENGLISH here](readme_ENG.md)

# ..: VERSION ALPHA :..

__Ce projet est encore en cours de modélisation et évolue rapidement.__

__D'autres informations seront publiées prochainement.__

# Adaptateur Pyboard vers UNO-R3

Voici une proposition de raccordement, brochage et adaptateur pour Arduino R3 sur une carte PyBoard.

![Caractéristique de l'adaptateur](docs/_static/UNO-R3-description.jpg)

L'intérêt d'un adaptateur UNO-R3 c'est qu'il permet de brancher des shields Arduino (ex: shield moteur Adafruit) que l'on peut contrôler à partir d'une Pyboard et de scripts Python.

Par ailleurs, la carte contient de nombreuses fonctionnalités intéressantes permettant de transformer rapidement une Pyboard en environnement de prototypage/apprentissage très facile à prendre en main (voir graphique ci-dessus).

# Information technique
Pour connecter an shield Arduino sur votre Pyboard, vous aurez besoin de savoir quel bus (SPI, I2C, GPIO) cette extension exploite. Dans la plupart des cas, c'est le bus I2C (avec 3.3V et la masse) ou le bus SPI (ex TFT).

![Brochage de l'adaptateur Pyboard-UNO-R3](docs/_static/UNO-R3-Pyboard-mapping-(1500px).jpg)

Cette interface est prévue pour les produits compatibles 3.3V (voir broche IORef sur extension Arduino R3)

Le raccordement proposé ci-dessous couvre toutes les broches de la spécification R3!. __Le mapping est compatible avec UEXT, NCD, QWIIC déjà proposés sur ce dépôt__.

## Schéma
* [PYBV11_to_ARDUINO_UNO_R3.pdf](docs/_static/Schematic_V1.0-_PYBV11_to_ARDUINO_UNO_R3.pdf) brochage
* [Assignation des broches Pyboard](docs/_static/pyboard-pin-assignation.jpg) encore 8 broches de libres + 4 broches des LEDs rouge, vert, bleu, jaune



## Logique 3.3V
Bien que la Pyboard soit globalement (__mais pas complètement__) tolérante 5V, il est important de considérer cet adaptateur UNO R3 comme fonctionnant en logique 3V.

Cet adapteur indique donc un niveau logique de 3.3V sur la broche IOREF afin que les shields que vous y brancherez soient averti du niveau logique à employer.

## Parenté UPPY
Le brochage proposé provient, en grande partie, du projet UPPY (_Universal Prototyping Pyboard_) visant à offrir un maximum de connectivité à votre carte Pyboard.

Les détails du branchement sont disponibles ici dans le projet [Pin-Mapping-table.pdf](../UPPY/docs/Pin-Mapping-table.pdf)

# Bibliothèque

## Bibliothèque "uno"
La bibliothèque `uno.py` contient des définitions et fonctions permettant de facilement passer du brochage Arduino au brochage Pyboard de manière assez transparente.

* Il est possible d'utiliser le nom de la broche Pyboard comme `"X10"`, correspondant à la broche Arduino 9.
* La constante `PIN_9` (correspondant à la broche Arduino 9) de la bibliothèque `uno.py` permet d'atteindre le même but mais une numérotation plus proche d'Arduino.

Les deux codes suivant sont donc rigoureusement identiques:
``` python
from machine import Pin
p = Pin( "X10", Pin.IN ) # broche Arduino 9
print( p.value() )       # Affiche 1 ou 0
```
La version avec brochage type "UNO" devient:
``` python
from uno import *
from machine import Pin
p = Pin( PIN_9, Pin.IN ) # broche Arduino 9
print( p.value() )       # Affiche 1 ou 0
```

__Fonctions utilitaires:__

La bibliothèque `uno.py` propose également des fonctions pour créer rapidement les bus I2C, SPI, UART correspondant à la carte UNO R3.

``` python
from uno import *
# Returns the I2C bus placed over the Arduino pin 13.
i2c = i2c_bus( freq=20000 )

# Returns a Bit-Banging I2C bus placed on the Arduino Pin A4, A5.
i2c = i2c_analog_bus( freq=10000 )

# Returns the UART initialized on Arduino pin 0 & 1.
serial = uart_bus( baudrate=9600 )

# Returns the SPI bus and SS control Pin for Arduino pins 10,11,12,13.
spi, ss = spi_bus( baudrate=20000 )

```

Toutes ces fonctions acceptent les paramètres complémentaires supportés par l'API machine de MicroPython.

## Dépendances
Les bibliothèques suivantes sont nécessaires pour exploiter toutes les fonctionnalités de la carte. Les bibliothèques doivent être disponibles dans le système de fichiers de la carte Pyboard (à la racine ou dans un sous répertoire `lib`).

TODO : a compléter

* xxx.py : description [disponible ici (esp8266-upy GitHub)](url)
* yyy.py : description [disponible ici (esp8266-upy GitHub)](url)


# Prise en main
Cette section reprend l'utilisation des différents éléments de la carte.

## Bouton utilisateur (A)

TODO

## Broche Numérique

TODO

## Entrée Analogique

TODO

## Sortie PWM

TODO

## Sortie Analogique (DAC)

TODO

## Neopixel

TODO

## Buzzer

TODO

## Servo

TODO

## Chargeur LIPO
Le chargeur Lipo dispose d'une entrée I2C.

## Bus I2C, SPI, UART
La carte expose les bus standard d'un Arduino ainsi que de nombreux bus en extra.
Les notes ci-dessous expliquent comment créer les différents bus nécessaires.

__Connecteur R3:__ créer les bus standards

La bibliothèque `uno.py` décrite ci-avant permet de créer simplement les bus Arduino à l'aide des fonctions utilitaires `i2c_bus()`,  `i2c_analog_bus()`, `uart_bus()` ou `spi_bus`.

Il reste néanmoins possible de créer les différents bus à l'aide de l'API machine et les noms de broche de la Pyboard (voir graphique du brochage) comme indiqué ci-dessous.

``` python
# I2C côté broche 13 (I2C matériel)
from machine import I2C
i2c = I2C(2)

# Sur broche A4, A5 (I2C logiciel, Bit-Banging)
from machine import I2C
i2c = I2C( sda=Pin("X5"), scl=Pin("X6") )

# Broche 10,11,12,13
from machine import SPI
spi = SPI(2)

# Broches 1 et 2 (indépendant)
from machine import UART
uart = UART(6, 9600) # UART à 9600 bauds
```

__Connecteur UEXT:__ créer les bus
``` python
from machine import I2C
i2c = I2C(2)

from machine import SPI, Pin
spi = SPI(2)
ss = Pin( "X8", Pin.OUT, value=1 )

from machine import UART
uart = UART(1, 9600) # UART à 9600 bauds
```

__Connecteur RAPIDO:__ créer le bus
``` python
from machine import I2C
i2c = I2C(2)
```

## Serial.print()
Besoin d'insérer des messages de débogages dans vos scripts?

Sous MicroPython on fait un `print("mon message")` et celui-ci est visible dans la session REPL (connexion série via USB). Pas besoin de `Serial.print()`!

Cela signifie que le port USB sur les broche Arduino 0 et 1 est __totalement libre d'usage__ pour votre propre usage (ce qui change beaucoup d'une carte Arduino UNO). Ce n'est d'ailleurs pas le seul port série (UART) matériel disponible!

## Exemple UEXT
Le connecteur UEXT transporte plusieurs bus (I2C,SPI,UART) et de nombreux [modules UEXT sont disponibles chez Olimex Ltd](https://www.olimex.com/Products/Modules/) (et son réseau de revendeur)

TODO

## Exemple RAPIDO
Ce connecteur est compatible [Qwiic de Sparkfun](https://www.sparkfun.com/qwiic) ou [Stemma d'Adafruit](https://learn.adafruit.com/introducing-adafruit-stemma-qt/what-is-stemma) .

TODO

# Où trouver des pilotes MicroPython

Tous nos pilotes MicroPython sont stockés sur le GitHub [pyboard-driver](https://github.com/mchobby/pyboard-driver) ET le GitHub [esp8266-upy](https://github.com/mchobby/esp8266-upy). Les pilotes MicroPython fonctionnant sur ESP8266 fonctionneront aussi avec des Pyboard :-)

# Liste d'achat
* Adaptateur Pyboard-UNO-R3 @ MCHobby (bientôt disponible)
* [Cartes MicroPython Pyboard](https://shop.mchobby.be/fr/56-micropython)
* [Carte prototypage Pyboard](https://shop.mchobby.be/fr/micropython/598-plaque-de-prototypage-pour-pyboard-3232100005983.html)
* [Carte de prototypage Arduino](https://shop.mchobby.be/fr/shields/12-shield-de-prototypage-pour-arduino-3232100000124-adafruit.html)
* [Gamme Arduino @ MCHobby](https://shop.mchobby.be/fr/5-arduino).
