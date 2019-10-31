[This file also exists in ENGLISH here](readme_ENG.md)

# ..: VERSION ALPHA :..
__Ce projet est encore en cours de modélisation et évolue rapidement.__

__D'autres informations seront publiées prochainement.__

# Connecteur compatible Arduino UNO R3 pour Pyboard

Voici une proposition de raccordement (et brochage) pour brancher un shield Arduino R3 sur une carte PyBoard.

![Breakout Arduino R3 Shield sur Pyboard](docs/_static/Uno-R3-Pyboard-breakout.jpg)

# Qu'est ce que l'écosystème Arduino ?

TO DO - TO DO - TO DO - TO DO - TO DO - TO DO - TO DO - TO DO -

Logique 3V et logique 5V sur Arduino UNI

# Connecteur UNO R3
Pour connecter an shield Arduino sur votre Pyboard, vous aurez besoin de savoir quel bus (SPI, I2C, GPIO) cette extension exploite. Dans la plupart des cas, c'est le bus I2C (avec 3.3V et la masse) ou le bus SPI (ex TFT).

Cette interface est prévue pour les produits compatibles 3.3V (voir broche IORef sur extension Arduino R3)

Le raccordement proposé ci-dessous couvre toutes les broches de la spécification R3!. __Le mapping est compatible avec UEXT, NCD, QWIIC déjà proposés sur ce dépôt__.

![Connecteur UNO R3](doc/arduino/Shield_Pinout.png)


# brochage
Le brochage proposé provient, en grande partie, du projet UPPY (_Universal Prototyping Pyboard_) visant à offrir un maximum de connectivité à votre carte Pyboard.

Les détails du branchement sont disponibles ici dans le projet [Pin-Mapping-table.pdf](../UPPY/docs/Pin-Mapping-table.pdf)


# Bus I2C, SPI, UART
Voici les instructions permettant de créer une instance du bus I2C sur le connecteur NCD.

```
from machine import I2C
i2c = I2C(2)

from machine import SPI
spi = SPI(2)

from machine import UART
uart = UART(6, 9600) # UART à 9600 bauds
```

# Où trouver des pilotes MicroPython

Tous nos pilotes MicroPython sont stockés sur le GitHub [pyboard-driver](https://github.com/mchobby/pyboard-driver) ET le GitHub [esp8266-upy](https://github.com/mchobby/esp8266-upy). Les pilotes MicroPython fonctionnant sur ESP8266 fonctionneront aussi avec des Pyboard :-)

Les pilotes MicroPython pour les cartes exposants un facteur de forme FeatherWing sont stockes dans des répertoires commençant avec "__feather-__" (ex: feather-motor, etc).

* GitHub __esp8266-upy__ propose une liste des pilotes pour [interface FeatherWing sur __esp8266-upy__](https://github.com/mchobby/esp8266-upy/blob/master/docs/indexes/drv_by_intf_FEATHERWING.md).

# Liste d'achat
* [Carte prototypage Pyboard](https://shop.mchobby.be/fr/micropython/598-plaque-de-prototypage-pour-pyboard-3232100005983.html)
* [Carte de prototypage Arduino](https://shop.mchobby.be/fr/shields/12-shield-de-prototypage-pour-arduino-3232100000124-adafruit.html)
* [Cartes MicroPython Pyboard](https://shop.mchobby.be/fr/56-micropython)
* [Gamme Arduino @ MCHobby](https://shop.mchobby.be/fr/5-arduino).
