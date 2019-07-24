[This file also exists in ENGLISH here](readme_ENG.md)

# Connecteur QWIIC sur Pyboard

Voici une proposition de raccordement (et brochage) pour brancher un connecteur QWIIC sur une carte PyBoard.

![Breakout QWIIC sur Pyboard](QWIIC-Pyboard.jpg)

# Qu'est ce que l'écosystème QWIIC ?

([SparkFun Electronic](https://www.sparkfun.com)) a créé de nombreuses cartes capteurs I2C nommée "_QWIIC Board_" exploitant un connecteur standardisé à 4 broches avec __alimentation 3.3V__ et utilisant des signaux en __logique 3.3V__.

![Quelques cartes QWIIC de Sparkfun](QWIIC-example.jpg)

Utiliser une interface standardisée sur une __grande variété de carte__ (comme Arduino, Raspberry, Feather, WiPy, LoPy, etc) et carte capteur est absolument génial! Cela facilite le prototypage et le développement de solutions personnalisées sans la difficulté d'avoir à disposer de connaissances en électronique ou en soudure.

# Connecteur QWIIC
Pour connecter une carte I2C de SparkFun, vous aurez besoin d'un connecteur QWIIC  ou fils de raccordement QWIIC.

![Connecteur QWIIC](QWIIC_conn.jpg)

Sparkfun propose de nombreuses cartes adaptateurs [disponibles ici](https://www.sparkfun.com/qwiic) mais nous pouvons également créer nos propres branchement vers d'autres cartes de développement (comme suggéré ci-avant).

# Bus I2C
Voici les instructions permettant de créer une instance du bus I2C sur le connecteur QWIIC.

```
from machine import I2C

i2c = I2C(2)
```

# Où trouver des pilotes MicroPython pour cartes QWIIC

Tous nos pilotes MicroPython sont stockés sur le GitHub [pyboard-driver](https://github.com/mchobby/pyboard-driver) ET le GitHub [esp8266-upy](https://github.com/mchobby/esp8266-upy). Les pilotes MicroPython fonctionnant sur ESP8266 fonctionneront aussi avec des Pyboard :-)

Les pilotes MicroPython pour les capteurs I2C populaires (ex: BMP280, BME280, TSL2591, etc) fonctionneront également avec les connecteurs QWIIC, il suffit de créer l'instance du bus I2C de façon adéquate.

Les pilotes MicroPython pour les cartes exposants un connecteur QWIIC sont stockés dans des répertoires commençant par "__qwiic-__" (ex: qwiic-mpl115-a2, etc).

# Liste d'achat
* [Carte prototypage Pyboard](https://shop.mchobby.be/fr/micropython/598-plaque-de-prototypage-pour-pyboard-3232100005983.html)
* Connecteur QWIIC mâle: [disponible sur SparkFun.com](https://www.sparkfun.com/products/14417)
* Extension QWIIC: [vaste gamme disponible chez SparkFun](//https://www.sparkfun.com/qwiic/).
* [Cartes MicroPython Pyboard](https://shop.mchobby.be/fr/56-micropython)
