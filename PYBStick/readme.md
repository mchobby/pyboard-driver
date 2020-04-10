[This file also exists in ENGLISH here](readme_ENG.md)

# PYBStick 26 : La carte MicroPython d'entrée de gamme pour tous les projets

TODO : description

![Caractéristiques de la PYBStick 26](docs/_static/pybstick-features.jpg)

## Modèles de PYBStick

La PYBStick 26 existe en 3 modèle: Lite, Standard et Pro

![Modèles de PYBStick 26](docs/_static/PYBStick-models-list.png)

# Information technique

## PYBStick Lite 26

![Brochage de la PYBStick Lite 26](docs/_static/PYBStick-LITE-26.jpg)

Aussi disponible en haute définition sur le lien [PYBStick-LITE-26.png](docs/_static/PYBStick-LITE-26.png)

## Schéma
* Schéma [PYBStick Lite 26.pdf](docs/_static/Schematic_V1.0-PYBStick26Lite.pdf)
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

![Bouton utilisateur](docs/_static/pybstick-user-button.jpg)

Le bouton A correspond au bouton USR présent sur la carte Pyboard. Il est donc possible d'utiliser la classe `Switch`.

La classe `Switch` permet de lire l'état du bouton.

```
>>> from pyb import Switch
>>> sw = Switch()
>>> # Bouton non pressé
>>> sw.value()
False
>>> # Presser le bouton
>>> sw.value()
True
```

La classe `Switch` permet aussi d'assigner une fonction de rappel qui sera invoquée chaque fois que le bouton USB sera relâché.

```
>>> from pyb import Switch
>>>
>>> definir fonction de rappel
def rappel():
    print("Hello")
>>>
>>> sw = Switch()
>>> sw.callback( rappel )
>>>
>>> # Presser le bouton USR
>>> Hello
Hello
Hello
Hello
```

## Broche Numérique - en entrée

La lecture de l'état d'une entrée se fait à l'aide de la classe Pin configurée en entrée.

* Lorsque le bouton est pressé, le potentiel de la broche S3 est placé/connecté à la masse.
* Lorsque le bouton est relâché, la broche S3 est rappelée à +3.3V par la résistance de 10 KOhms.

![Bouton en entrée](docs/_static/pybstick-input.jpg)

L'exemple ci-dessous permet de lire l'état de la broche d'entrée. A noter que la lecture de l'état retourne False lorsque le bouton est pressé. Nous sommes donc dans une logique inversée.

```
>>> from machine import Pin
>>> p = Pin( "S3", Pin.IN )
>>> # Ne pas presser le bouton
>>> p.value()
True
>>> # Presser le bouton
>>> p.value()
False
```

La microcontrôleur peut également activer une résistance pull-up interne, ce qui permet d'éviter le montage de la résistance de 10 KOhms.

![Bouton en entrée](docs/_static/pybstick-input-pullup.jpg)

Le script suivant affiche l'état du bouton toutes les demi-secondes.
Presser Ctrl+C pour stopper le script.

```
>>> from machine import Pin
>>> from time import sleep
>>> p = Pin( "S3", Pin.IN, Pin.PULL_UP  )
>>> while True:
>>>     s = "..." if p.value() else "Pressé"
>>>     print( s )
>>>     sleep( 0.5 )
>>>
```

## Broche Numérique - en sortie

Une broche en sortie permet au script de contrôler l'état de la broche (niveau haut ou nouveau bas). Cela se fait également par l'intermédiaire de la classe Pin.

La broche du microcontrôleur peut donc commander un périphérique externe uniquement si celui-ci consomme un faible courant (par exemple, une LED ou une carte breakout).

__Attention:__ Pour commander un périphérique énergivore comme un moteur ou un relais, il est impératif de passer par une interface d'amplification appropriée.  

Le montage suivant permet de contrôler une LED par l'intermédiaire d'une résistance de  1K Ohms. Cette résistance permet de limiter le courant lorsque la LED devient conductrice et émet de la lumière. Sans cette résistance, le courant tendra vers l'infini (ce qui détruira le microcontrôleur).

![Bouton en entrée](docs/_static/pybstick-output-led.jpg)

Pour contrôler la sortie (et la LED), il suffit de saisir les quelques instructions suivantes

```
>>> from machine import Pin
>>> p = Pin( "S8", Pin.OUT )
>>>
>>> # Sortie au Niveau Haut (3.3V) -> Allume LED
>>> p.value( 1 )
>>>
>>> # Sortie au Niveau Bas (0V) -> LED éteinte
>>> p.value( 0 )
```

Le script suivant produit effet de battement de coeur.

```
>>> from time import sleep_ms
>>> from machine import Pin
>>> p = Pin( "S8", Pin.OUT )
>>> while True:
>>>     sleep_ms( 1300 ) # Attendre 1100 millisecondes
>>>     p.value( 1 ) # Allume LED
>>>     sleep_ms( 80 )
>>>     p.value( 0 ) # Eteindre LED
>>>     sleep_ms( 80 )
>>>     p.value( 1 ) # Allume LED
>>>     sleep_ms( 80 )
>>>     p.value( 0 ) # Eteindre LED
>>>
```

## Entrée Analogique (3.3 V max)

La carte est équipée de de plusieurs entrée analogiques (S8, S10, S12, S19, S23, S26).

__Attention: en aucun cas la tension appliquée sur l'entrée analogique ne peut être supérieure à 3.3V__ au risque de détruire le microcontrôleur.

Celle-cis peuvent être utilisés pour lire une tension entre 0 et 3.3V avec un résolution de 12 bits.

Le convertisseur Analogique Digital (appelé ADC) retourne donc une valeur entre 0 et 4095 (soit 4096 valeurs possibles).

Le graphique suivant utilise un potentiomètre de 10 KOhms linéaire pour générer une tension entre 0 et 3.3V sur l'entrée S26).

![Entrée analogique](docs/_static/pybstick-analog-input.jpg)

En tournant le potentiomètre, la tension varie sur l'entrée analogique et le résultat est visible sur l'information retournée par le convertisseur analogique digital.

Le script suivant affiche la valeur du convertisseur toutes les 300ms
```
>>> from pyb import ADC
>>> from time import sleep
>>> adc26 = ADC("S26")
>>> while True:
>>>     print( adc26.read() )
>>>     sleep( 0.3 )

```

Quelques exemples complémentaires fournissent de nombreuses autres informations sur le convertisseur ADC:
* [`adc_all.py`](examples/adc_all.py) effectue une lecture de toutes les entrées analogiques (affiche valeur ADC et Tension correspondante)
* [`adc_10bits.py`](examples/adc_10bits.py) effectue une lecture en retrogradant la précision à 10 bits (valeurs entre 0 et 1024)
* [`adc_sampling.py`](examples/adc_sampling.py) effectue un échantillonnage 8 bits sur une entrée.
* Plus d'information sur [la page ADC de MicroPython.org](https://docs.micropython.org/en/latest/library/pyb.ADC.html)

__Parasites:__ un potentiomètre étant constitué d'un curseur se déplaçant le long d'une résistance, il n'est pas rare d'avoir des faux-contact et effet transitoire. Si ceux-ci sont faible et très court, ils peuvent néanmoins planter un convertisseur ADC (démontré sur un ADC1115). Si vous expérimentez ce type de désagrément, placez alors une capacité de 10nF entre la sortie du signal et la masse :-)

## Sortie Analogique (DAC)

La PYBStick Lite ne dispose pas de sortie analogique (DAC).


## Sortie PWM

La carte PYBStick 26 expose de nombreuses broches PWM (Pulse Modulation Width = Modulation de largeur d'impulsion) qu'il est très facile de piloter à l'aide de la bibliothèque [`lib/pwm.py`](lib/pwm.py).

![LED en sortie](docs/_static/pybstick-output-led.jpg)

```
>>> from pwm import *
>>> p = pwm( "S8" )
>>> # Set 33% of duty cycle
>>> p.percent = 33
```
L'exemple suivant permet de commander l'intensité de la LED sur la broche S8 en fonction de la position du potentiomètre branché sur la S19.

![LED en PWM](docs/_static/pybstick-pwm-led.jpg)

```
from pwm import *
from pyb import ADC
from time import sleep

p = pwm("S8")
adc = ADC("S19")

while True:
	p.percent = int( adc.read()*100/4095 )
	sleep( 0.300 )
```

Ce script est disponible dans les exemples sous le nom [`pwm_led.py`](examples/pwm_led.py)

Ressources:
* L'exemple [`pwm_all.py`](examples/pwm_all.py) permet de tester une à une (en pressant le bouton USR) toutes les broches PWM de la PYBStick.
* MicroPython.org propose la page "[Hardware timer](https://docs.micropython.org/en/latest/wipy/tutorial/timer.html)".
* Le livre ["MicroPython et Pyboard" paru aux éditions Eni](https://www.editions-eni.fr/livre/micropython-et-pyboard-python-sur-microcontroleur-de-la-prise-en-main-a-l-utilisation-avancee-9782409022906) consacre une section entière à la gestion des Timers, Channel, PWM, cycle utile.

## NeoPixel

TODO - Revoir et corriger

La carte est équipée d'une LED WS2812b (également appelée [NéoPixel dans les produits Adafruit Industries](https://shop.mchobby.be/fr/55-neopixels-et-dotstar)). Il s'agit de LED RVB intelligentes pouvant être chaînée. La carte PYBOARD-UNO-R3 dispose d'un convertisseur de niveau logique pour commander cette LED sous 5V afin d'avoir un maximum de luminosité et des couleurs vives. La carte dispose également d'une sortie permettant d'ajouter d'autres LEDs.

__Dépendance:__ la bibliothèque `ws2812` doit être présente sur la carte. Voir la section dépendance pour localiser la bibliothèque.

Voir le fichier d'exemple [`test_led.py`](examples/test_led.py) et sa [vidéo sur YouTube](https://youtu.be/NBv3lBmyQYc)

## Servo

La PYBStick expose 3 sorties permettant de contrôler des [servo-moteurs modélistes](https://fr.wikipedia.org/wiki/Servomoteur).

__Alimentation:__ Il est possible d'alimenter un ou deux micro-servo par l'intermédiaire du port USB de la PYBStick (via un ordinateur). Cependant cela risque fort d'injecter pléthore de parasite sur l'alimentation de votre ordinateur et de la PYBStick sans compter qu'ils sont aussi énergivores (un courant de blocage de 500mA n'est pas une exception). Voyez la proposition d'alimentation plus bas.

![PYBStick et Servo-moteur](docs/_static/pybstick-servo.jpg)

![Servo-moteur connexion](docs/_static/motor-servo-connectors.png)

Les servos sont positionnés entre -90 et +90 degrés. A l'initialisation, le servo-moteur est positionné à 0 degrés.

```
from pyb import Servo
from time import sleep

s = Servo(1)    # initialise l angle à 0°
time.sleep( 1 ) # Attendre 1 seconde
s.angle( 90 )
time.sleep( 1 )
s.angle( -90 )
time.sleep( 1 )
s.angle( -90 )
```

Alimentation externe pour les servo-moteurs.

![Pyboard et Servo-moteur](docs/_static/pybstick-servo2.jpg)

Brancher deux servo-moteurs sur les sorties SERVO(1) et SERVO(4) puis saisir le code suivant pour coordonner le mouvement des deux servo-moteurs.

```
from pyb import Servo
from time import sleep
s1 = Servo(1)
s1.angle(+90)
s4 = Servo(4)
s4.angle(-90)
# déplacement coordonné
s1.angle(-90,4000) # Déplacement à -90 pendant 4000 ms
s4.angle(+90,4000) # Déplacement à +90 pendant 4000 ms
sleep( 4 ) # Attendre fin de déplacement
s1.angle(0)
s4.angle(0)
```

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

* [PYBStick-Lite-26](https://shop.mchobby.be/product.php?id_product=1830)
* [Cartes MicroPython](https://shop.mchobby.be/fr/56-micropython)
