[This file also exists in ENGLISH here](readme_ENG.md)

# PYBStick 26 : La carte MicroPython d'entrée de gamme pour tous les projets

TODO : description

![Caractéristiques de la PYBStick 26](docs/_static/PYBStick-feature.jpg)

## Modèles de PYBStick

La PYBStick 26 existe en 3 modèle: Lite, Standard et Pro

![Modèles de PYBStick 26](docs/_static/PYBStick-models.png)

# Information technique

## PYBStick 26 Lite

![Brochage de la PYBStick 26 Lite](docs/_static/PYBStick-LITE-26.jpg)

Aussi disponible en haute définition sur le lien [PYBStick-LITE-26.png](docs/_static/PYBStick-LITE-26.png)

## Schéma
* Schéma [PYBStick 26 Lite.pdf](docs/_static/Schematic_V1.0-PYBStick26Lite.pdf)
* Assignation des broches [PYBStick-pinout.ods](docs/_static/PYBStick-pinout.ods) (_LibreOffice Calc_)

## Logique 3.3V

TODO

# Bibliothèque

## Dépendances
TODO : a revoir

Les bibliothèques suivantes sont nécessaires pour exploiter toutes les fonctionnalités de la carte. Les bibliothèques doivent être accessibles dans le système de fichiers de la carte MicroPython (à la racine ou dans un sous-répertoire `lib`).

* ws2812.py : contrôler des NeoPixels avec le bus SPI [disponible ici (esp8266-upy GitHub)](https://github.com/mchobby/esp8266-upy/tree/master/neopixel)

## Bibliothèque "pwm"
La bibliothèque `pwm.py` contient des définitions et fonctions permettant de facilement contrôler les différentes broches PWM d'une PYBStick.

L'utilisation de cette bibliothèque est décrite plus bas dans la section "Sorties PWM".


# Prise en main
Cette section reprend l'utilisation des différents éléments de la carte.

## Bouton utilisateur (A)

TODO

Le bouton A correspond au bouton USR présent sur la carte Pyboard. Il est donc possible d'utiliser la classe `Switch`.

## Broche Numérique - en entrée

TODO

La lecture de l'état d'une entrée se fait à l'aide de la classe Pin.

## Broche Numérique - en sortie

TODO

Il est possible de contrôler l'état d'une broche en sortie à l'aide de la classe Pin.

Cela permet de piloter un périphérique externe comme une LED (via une résistance de 1K Ohms).

## Entrée Analogique (3.3 V max)

TODO

La carte est équipée de de plusieurs entrée analogiques (xxxxx à xxxxx) mais aussi sur les broches xxxx à xxxx.

Celle-cis peuvent être utilisés pour lire une tension entre 0 et 3.3V.

## Sortie Analogique (DAC)

La PYBStick Lite ne dispose pas de sortie analogique (DAC).


## Sortie PWM

TODO

La carte PYBStick 26 expose de nombreuses broches PWM (Pulse Modulation Width = Modulation de largeur d'impulsion) qu'il est très facile de piloter à l'aide de la bibliothèque `pwm.py`.

## NeoPixel

TODO - Revoir et corriger

La carte est équipée d'une LED WS2812b (également appelée [NéoPixel dans les produits Adafruit Industries](https://shop.mchobby.be/fr/55-neopixels-et-dotstar)). Il s'agit de LED RVB intelligentes pouvant être chaînée. La carte PYBOARD-UNO-R3 dispose d'un convertisseur de niveau logique pour commander cette LED sous 5V afin d'avoir un maximum de luminosité et des couleurs vives. La carte dispose également d'une sortie permettant d'ajouter d'autres LEDs.

__Dépendance:__ la bibliothèque `ws2812` doit être présente sur la carte. Voir la section dépendance pour localiser la bibliothèque.

Voir le fichier d'exemple [`test_led.py`](examples/test_led.py) et sa [vidéo sur YouTube](https://youtu.be/NBv3lBmyQYc)

## Buzzer

La carte PYBStick peu être équipé d'un buzzer pour produire produire des sons et des notes.

TODO - s'insiprer de Pyboard-UNO-R3

## Servo

TODO - a revoir et compléter

Il y a 4 sorties Servo prêt à l'emploi sur la PYBOARD-UNO-R3 pour commander un Servo.

Les servo sont positionnés entre -90 et +90 degrés. A l'initialisation, le servo moteur est positionné à 0 degrés.

Voir le fichier d'exemple [`test_servo.py`](examples/test_servo.py) et sa [vidéo sur YouTube](https://youtu.be/0a2VYjg0XG8).

Brancher deux servo-moteurs sur les sorties SERVO1 et SERVO2 puis saisir le code suivant:

## Bus I2C, SPI, UART

TODO - a revoir complètement

La carte expose les bus standard d'un Arduino ainsi que de nombreux bus en extra.
Les notes ci-dessous expliquent comment créer les différents bus nécessaires.

__Connecteur:__ créer les bus standards

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

# Port série sur 0 et 1 (totalement libre d'usage)
from machine import UART
uart = UART(6, 9600) # UART à 9600 bauds
```

# Où trouver des pilotes MicroPython

Tous nos pilotes MicroPython sont stockés sur le GitHub [pyboard-driver](https://github.com/mchobby/pyboard-driver) ET le GitHub [esp8266-upy](https://github.com/mchobby/esp8266-upy). Les pilotes MicroPython fonctionnant sur ESP8266 fonctionneront aussi avec des Pyboard :-)

# Liste d'achat

TODO

* [Cartes MicroPython](https://shop.mchobby.be/fr/56-micropython)
