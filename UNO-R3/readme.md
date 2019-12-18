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

Charger Note: Jaune fixe + Vert clignotant = No battery

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

## Dépendances
Les bibliothèques suivantes sont nécessaires pour exploiter toutes les fonctionnalités de la carte. Les bibliothèques doivent être accessibles dans le système de fichiers de la carte Pyboard (à la racine ou dans un sous-répertoire `lib`).

* ws2812.py : contrôler des NeoPixels avec le bus SPI [disponible ici (esp8266-upy GitHub)](https://github.com/mchobby/esp8266-upy/tree/master/neopixel)
* ssd1306.py : contrôle écran OLED à base de contrôleur SSD1306 [disponible ici (MicroPython GitHub)](https://github.com/micropython/micropython/tree/master/drivers/display)

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


## Bibliothèque "pwm"
La bibliothèque `pwm.py` contient des définitions et fonctions permettant de facilement contrôler les différentes broches PWM d'une Pyboard (et donc de la PYBOARD-UNO-R3).

L'utilisation de cette bibliothèque est décrite plus bas dans la section "Sorties PWM".

## Bibliothèque "unoextra"
La bibliothèque `unoextra.py` contient des classes utilitaires supplémentaires permettant de contrôler l'écran OLED ou le chargeur d'accu présent sur PYBOARD-UNO-R3.

L'utilisation de cette bibliothèque est décrite plus bas dans la section "OLED" et "Chargeur Accu".

# Prise en main
Cette section reprend l'utilisation des différents éléments de la carte.

## Bouton utilisateur (A)

Le bouton A correspond au bouton USR présent sur la carte Pyboard. Il est donc possible d'utiliser la classe `Switch`.

``` python
from pyb import Switch
sw = Switch()

def click():
    print("Clicked")

sw.callback( click )
print( "Presser le bouton A")
```
Ce qui produit le résultat suivant dans la session REPL lorsque le bouton est pressé:

```
Presser le bouton A
Clicked
Clicked
Clicked
Clicked
Clicked
Clicked
```
Pour désactiver le rappel de la fonction `click()`, il suffit de désactiver le ___callback___ à l'aide de `sw.callback( None )`

## Broche Numérique - en entrée

La lecture de l'état d'une entrée se fait à l'aide de la classe Pin.

``` python
from machine import PIN
from time import sleep
from uno import *

p = Pin( "Y2", Pin.IN )
# Equivalent à...
# p = Pin( PIN_0, Pin.IN )

while True:
    if p.value()==1:
        print("Niveau Haut")
    else:
        print("Niveau Bas")
    sleep( 0.5 ) # attendre 1/2 seconde
```

Il ne reste plus qu'a placer la broche à la masse à l'aide d'un switch (ou autre dispositif).

__Résistance pull-up interne:__

Il est également possible d'activer la résistance pull-up interne d'une entrée.
Cette-ci ramène le potentiel de la broche à 3.3V sauf si un autre procédé (ex: bouton momentané) force le potentiel à la masse.

![Utiliser un bouton](docs/_static/input-switch.jpg)

``` python
from machine import PIN
from time import sleep
from uno import *

p = Pin( "Y2", Pin.IN, Pin.PULL_UP )
# Equivalent à...
# p = Pin( PIN_0, Pin.IN )

while True:
    if p.value():
        print("Niveau Haut")
    else:
        print("Niveau Bas")
    sleep( 0.5 ) # attendre 1/2 seconde
```
## Broche Numérique - en sortie

Il est possible de contrôler l'état d'une broche en sortie à l'aide de la classe Pin.

Cela permet de piloter un périphérique externe comme une LED (via une résistance de 1K Ohms).

![Piloter une LED](docs/_static/output-led.jpg)

``` python
from machine import PIN
from time import sleep
from uno import *

p = Pin( "Y3", Pin.OUT )
# Equivalent à...
# p = Pin( PIN_0, Pin.IN )

while True:
    if p.value()==1:
        print("Niveau Haut")
    else:
        print("Niveau Bas")
    sleep( 0.5 ) # attendre 1/2 seconde
```

## Entrée Analogique (3.3 V max)
La carte est équipée de de plusieurs entrée analogiques (A0 à A5) mais aussi sur les broches 2 à 7.

Celle-cis peuvent être utilisés pour lire une tension entre 0 et 3.3V.

Il est possible d'utiliser les constantes PIN_A0..PIN_A5 ou PIN_2..PIN_7 pour identifier ces broches.
Le graphique du brochage permet également de repérer le nom des boches MicroPython d'origine (PIN_A3 = X22).

![Lecture entrée analogique](docs/_static/input-pot.jpg)

_note:_ pour une plus grande stabilité, il est parfois nécessaire d'ajouter une capacité de 10nF entre la sortie du potentiomètre et la masse.

__Lecture Analogique 12 bits:__

Par défaut, le convertisseur fonctionne en 12 bits, cela signifie qu'il retourne une valeur numérique entre 0 et 4096. La résolution est donc de 3.3/4096 = 0.0008 V (8 mV)!

Cette précision est équivalente aux Arduino Zero, Due et MKR.

``` python
from pyb import ADC
from uno import *
from time import sleep

a3 = ADC(PIN_A3) # identique à ADC("X22")
while True:
	# Lecture résolution 12 bits
	val = a3.read() # 0 à 4095
	volts = val/4096*3.3
	print( "read: %i  Volts: %3f v" % (val,volts) )
	sleep( 0.500 )
```

__Lecture Analogique 10 bits:__

Pour les habités du monde Arduino UNO ou la précision est en 10 bits (valeur de 0 à 1023), la bibliothèque `uno.py` propose la fonction `analog_read()` pour convertir la valeur en 10 bits.

``` python
from pyb import ADC
from uno import *
from time import sleep

a3 = ADC(PIN_A3) # same as ADC("X22")
while True:
	# lecture en résultion 10 bits
	val = analog_read(a3) # 0 à 1024
	volts = val/1024*3.3
	print( "read: %i  Volts: %3f v" % (val,volts) )
	sleep( 0.500 )
```

__Plus d'information:__
Le traitement des entrées analogique est un sujet relativement vaste avec des possibilités d'acquisition de signal!
Vous trouverez plus de détails sur ce sujet dans les références suivantes:
* [Livre "MicroPython et Pyboard", Meurisse D. paru aux Editions ENI](https://www.editions-eni.fr/livre/micropython-et-pyboard-python-sur-microcontroleur-de-la-prise-en-main-a-l-utilisation-avancee-9782409022906)
* [Classe ADC sur MicroPython.org](http://docs.micropython.org/en/latest/library/pyb.ADC.html) (_Anglais_)

## Sortie Analogique (DAC)

Les broches A4 et A5 peuvent également servir de sortie analogique dont il est possible de fixer la tension entre 0 et 3.3V.

__Résolution 8 bits par défaut:__

Sur 8 bit, il est possible de fixer une valeur entre 0 et 255 sur le convertiseur.

Pour produire une tension de 2.3V, il faut fournir la valeur (255/3.3)*2.6V = 201 au convertisseur DAC

``` python
from pyb import DAC
from uno import *
dac = DAC( PIN_A5 )
dac.write( 201 ) # Produit une tension de 2.6V

```
Il est également possible de convertir une valeur 8 bits arbitraire. Par exemple, la valeur 98 produirait la tension de 3.3/255*98

__Résolution 12 bits:__

Il est également possible de configurer le convertisseur DAC en résolution 12 bits (valeur de 0 à 4095).

``` python
from pyb import DAC
from uno import *
dac = DAC( PIN_A4, bits=12 )
out_v = 1.5 # Tension sortie 1.5V
dac.write( int(out_v/(3.3/4095)) )
```

__Produire une courbe:__

Le traitement des sorties analogiques couvre également la production de signaux arbitraire tels que des sinusoïdes ou autre:
* [Livre "MicroPython et Pyboard", Meurisse D. paru aux Editions ENI](https://www.editions-eni.fr/livre/micropython-et-pyboard-python-sur-microcontroleur-de-la-prise-en-main-a-l-utilisation-avancee-9782409022906)
* [Classe DAC sur MicroPython.org](https://docs.micropython.org/en/latest/library/pyb.DAC.html) (_Anglais_)

## Sortie PWM

La carte PYBOARD-UNO-R3 expose de très nombreuses broches PWM (Pulse Modulation Width = Modulation de largeur d'impulsion) qu'il est très facile de piloter à l'aide de la bibliothèque `pwm.py`.

``` python
from pwm import *
from uno import *
from time import sleep

# pwm13 = pwm("Y6") est identique
pwm13 = pwm(PIN_13)

print( "PWM de 0 à 100%")
for i in range(0,101, 5): # par pas de 5
	pwm13.percent = i  # fixer le cycle utile
	sleep(0.200)

# Mettre le signal au niveau bas
pwm13.percent = 0
```

__PWM en 8 bits__
Sur un Arduino, le contrôle PWM se fait avec un `analogWrite()` et une valeur de 0-255 (valeur 8 bits).

La bibliothèque PWM supporte la méthode `write()` qui accepte une valeur entre 0 et 255.
``` python
from pwm import *
from uno import *
from time import sleep

pwm13 = pwm(PIN_13)

# Le faire à la méthode Arduino (avec valeur 8 bits)
for i in range(0,256,3): # par pas de 3
	pwm13.write( i )
	sleep(0.050)
```

__PWM release__
Une fois une broche PWM initialisée, il est possible de mettre le signal au niveau bas avec `pwm13.percent = 0` ou au niveau haut avec `pwm13.percent=100`.

La broche reste configurée en sortie!

Il est possible d'utiliser la méthode 'pwm13.release()' pour reconfigurer la broche en entrée (donc haute impédance) et ainsi cesser toute opération PWM sur la broche.

``` python
from pwm import *
from uno import *
from time import sleep

# pwm13 = pwm("Y6") est identique
pwm13 = pwm(PIN_13)

# PWM à 40% de cycle utile
pwm13.percent = 40
sleep(2)

# Désactiver le PWM et mettre la broche en haute impédance (=entrée)
pwm13.release()
sleep( 2 )

# Besoin de réactiver le PWM sur la broche ?
# Alors réactiver la broche 13 en PWM
pwm13 = pwm(PIN_13)
pwm13.percent = 50
sleep( 2 )

# Mettre au niveau bas
pwm13.percent = 0
```

## Neopixel

La carte est équipée d'une LED WS2812b (également appelée [NéoPixel dans les produits Adafruit Industries](https://shop.mchobby.be/fr/55-neopixels-et-dotstar)). Il s'agit de LED RVB intelligentes pouvant être chaînée. La carte PYBOARD-UNO-R3 dispose d'un convertisseur de niveau logique pour commander cette LED sous 5V afin d'avoir un maximum de luminosité et des couleurs vives. La carte dispose également d'une sortie permettant d'ajouter d'autres LEDs.

__Dépendance:__ la bibliothèque `ws2812` doit être présente sur la carte. Voir la section dépendance pour localiser la bibliothèque.

Voir le fichier d'exemple [`test_led.py`](examples/test_led.py) et sa [vidéo sur YouTube](https://youtu.be/NBv3lBmyQYc)

```
from uno import pixels
from time import sleep

led = pixels() # une seule LED
rouge = (255,0,0)
vert  = (0,255,0)
bleu  = (0,0,255)
led.fill( rouge )
led.write()
sleep(1)

led.fill( vert )
led.write()
sleep(1)

led.fill( bleu )
led.write()
sleep(1)

led.fill( (255,0,255) ) # Magenta
led.write()
sleep(1)

led.fill( (0,0,0) ) # noir
led.write()
```
Il est également possible de contrôler plusieurs pixels en les chaînant sur la sortie NeoPixel et en indiquant le nombre de LEDs au moment de l'appel de la fonction `pixels()`.

Chaque pixel peut alors avoir une couleur différentes en utilisant la syntaxe suivante:
```
from uno import pixels
from time import sleep

leds = pixels(2) # deux LEDs
leds[0] = (255,0,0  ) # Rouge
leds[1] = (255,0,255) # Magenta
leds.write()
```
Voir l'exemple `test_led_stick.py` qui utilise un [Stick NeoPixel (Adafruit 1426)](https://www.adafruit.com/product/1426) de 8 pixels (soit 9 pixels au total) qu'il est possible de visaliser sur [cette vidéo YouTube](https://youtu.be/x7EwcywFcYU).


Plus d'information sur l'utilisation des LEDs RVB/NeoPixel dans le GitHub [esp8266-upy/neopixel](https://github.com/mchobby/esp8266-upy/tree/master/neopixel).

## Buzzer

La carte PYBOARD-UNO-R3 est équipé d'un buzzer magnétique capable de produire des sons et des notes.

```
from uno import Buzzer
from time import sleep

bz = Buzzer()
# Jouer la note Do à 593 Hertz
bz.tone( 523 )
sleep( 1 ) # Attendre 1 seconde
bz.tone()  # Silence
```

L'exemple [`test_buzzer_notes.py`](examples/test_buzzer_notes.py) permet de tester toutes les notes à disposition dans le dictionnaire NOTES.
``` python
from uno import Buzzer, NOTES
from time import sleep

bz = Buzzer()
tempo = 300 # Tempo
note_duration = 2 # Durée d'une note
print( ", ".join(NOTES.keys()) ) # Notes disponibles
for note in NOTES.keys():
	print( "Play note: %s " % note )
	bz.note( note, tempo*note_duration ) # 600*1000uS par note
	sleep( 0.3 ) # attendre 300ms entre chaque note
# Silent
bz.tone()
```
Ce qui produit le résultat suivant, en plus du son, où l'espace correspond à un silence:
```
g, f,  , a, c, b, C, e, d
Play note: g
Play note: f
Play note:   
Play note: a
Play note: c
Play note: b
Play note: C
Play note: e
Play note: d
```
Il est également possible de jouer des petites mélodies avec la methode `tune()` comme démontré dans l'exemple [`test_buzzer_tune.py`](examples/test_buzzer_tune.py)

``` python
from uno import Buzzer
from time import sleep

bz = Buzzer()

# Jouer une mélodie:
#   Liste de Note + Durée (séparé par des virgules)
#   Premier caractere = la note/tonalite (tel que connu par NOTES)
#   Second caractère = durée Note (defaut=1 si manquant)
tune1 = "c,c,g,g,a,a,g2,f,f,e,e,d,d,c2, 4"
tune2 = "c2,c,d3,c3,f3,e3,c2,c,d3,c3,g3,f3, 4"

bz.tune( tune1, tempo=300 ) # Plus Lent
sleep(1)
bz.tune( tune2, tempo=200 ) # Plus Rapide
```

Pour savoir comment piloter directement le Buzzer depuis MicroPython, referez vous à l'exemple [`test_buzzer_raw.py`](examples/test_buzzer_raw.py) .


## Servo

Il y a 4 sorties Servo prêt à l'emploi sur la PYBOARD-UNO-R3 pour commander un Servo.

Les servo sont positionnés entre -90 et +90 degrés. A l'initialisation, le servo moteur est positionné à 0 degrés.

Voir le fichier d'exemple [`test_servo.py`](examples/test_servo.py) et sa [vidéo sur YouTube](https://youtu.be/0a2VYjg0XG8).

Brancher deux servo-moteurs sur les sorties SERVO1 et SERVO2 puis saisir le code suivant:

``` Python
from pyb import Servo
from time import sleep
servo1 = Servo(1)
servo2 = Servo(2)
servo1.angle(-90)
servo2.angle(+90)
sleep(1)
# Coordonner le mouvement - revenir à 0 degrés
servo1.angle(0,2000) # Pendant deux secondes (2000ms)
servo2.angle(0,2000)
# Attendre fin du mouvement, donc 2 secondes
sleep( 2 )
servo1.angle( +90 )
servo2.angle( +90 )
```
Pour information, les sorties servo-moteurs (X1 à X4) utilisent le Timer 5.

## Afficheur OLED
La carte Pyboard-Uno-R3 dispose d'un écran OLED 128*64 pixels placés sur un bus I2C séparé du brochage UNO.

Cet écran peut donc être utilisé en toute indépendance sans interférer avec vos autres opérations. Cet écran est piloté par l'intermédiaire du pilote `ssd1306.py` (classe `SSD1306_I2C`) disponible sur le GitHub de MicroPython (voir section dépendance pour télécharger la bibliothèque).

Pour simplifier encore plus les choses, la bibliothèque `unoextra.py` propose la classe `Unoled` comme une surcouche du pilote original. Ce pilote `Unoled` intègre la notion de curseur pour simplifier l'affichage de texte à l'écran.

Toutes les fonctionnalités du `SSD1306_I2C` restent applicables à la classe `Unoled` (manipulation de pixels, dessin de rectangle, ...). Ces fonctionnalités sont détaillés dans le tutoriel [OLED FeatherWing](https://wiki.mchobby.be/index.php?title=FEATHER-MICROPYTHON-OLED#Tester_la_biblioth.C3.A8que)... seule la création de l'instance `lcd` diffère du tutoriel.

``` Python
from unoextra import Unoled
from time import sleep

lcd = Unoled()

# Methode FrameBuffer = position absolue
# pour texte et dessin
lcd.text("Bonjour", 10,10, 1)
lcd.text("MicroPython !", 10,20, 1)
# Dessiner un rectangle blanc - rect( x, y, w, h, c )
lcd.rect( 3, 3, 128-2*3, 64-2*3, 1 )
lcd.show() # doit être appelé
sleep( 2 )

# Affichage + défilement
# print() et println() rafraîssent l'écran
lcd.clear()
for i in range(11):
	lcd.println( "Line %s" % i )
	sleep( 0.5 )
sleep(2)
```

Il est également possible de contrôler la position du curseur, ce qui permet d'afficher de petites animations comme dans l'exemple suivant:

``` Python
from unoextra import Unoled
from time import sleep

lcd = Unoled()

lcd.clear()
s = "\|/-"
lcd.print('Progress:')
pos = lcd.cursor()
iCount = 0
while iCount < 20:
	lcd.set_cursor( pos )
	lcd.print( s[iCount%len(s)] )
	sleep( 0.250 )
	iCount += 1
lcd.set_cursor( pos )
lcd.println('Done!')
```

Il existe d'autres exemples dans le fichier [test_oled_basic.py](examples/test_oled_basic.py) .

**Utiliser directement le pilote SSD1306_I2C:**

Il n'est pas obligatoire de passer par la classe `Unoled` pour piloter l'écran OLED présent sur la carte.
Voici un exemple décrivant comment instancier et utiliser directement le pilote SSD1306_I2C.

``` Python
from machine import I2C, Pin
from ssd1306 import SSD1306_I2C

i2c=I2C(sda=Pin("Y4"), scl=Pin("Y3"))
lcd=SSD1306_I2C(128,64,i2c)
# Effacer l'écran
lcd.fill(0)
# Afficher du texte
lcd.text("Bonjour", 10,10, 1)
lcd.text("MicroPython !", 10,20, 1)
# Afficher un rectangle blanc - rect( x, y, w, h, c )
lcd.rect( 3, 3, 128-2*3, 64-2*3, 1 )
lcd.show()
```  

## Chargeur Accu
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

Cela signifie que le port série sur les broche Arduino 0 et 1 est __totalement libre__ pour votre propre usage (ce qui change beaucoup d'une carte Arduino UNO). Ce n'est d'ailleurs pas le seul port série (UART) matériel disponible sur l'adaptateur, il y en a 5 autres!

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
