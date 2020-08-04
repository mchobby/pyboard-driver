[This file also exists in ENGLISH](readme_ENG.md)

# Pilote MicroPython spécifique pour Pyboard

Ce dépôt contient des pilotes MicroPython spécifique pour la PyBoard (nécessitant plus de mémoire ou support matériel spécifique).

Les pilotes "plateforme agnostique" basée sur l' __API machine__ sont stockés dans le dépôt [esp8266-upy](https://github.com/mchobby/esp8266-upy).

Les codes et exemples sont également utilisés sur le [wiki documentaire Pyboard de MCHobby](https://wiki.mchobby.be/index.php?title=MicroPython-Accueil).

# Autres sources d'information
* [__Wiki pour MicroPython sur ESP8266__]( https://wiki.mchobby.be/index.php?title=MicroPython-Accueil#ESP8266_en_MicroPython) pour apprendre comment flasher votre ESP sous MicroPython.
* [__GitHub dédicacé Pyboard__](https://github.com/mchobby/pyboard-driver) avec des pilotes nécessitant plus de ressources. https://github.com/mchobby/pyboard-driver.
* Achat de matériel - https://shop.mchobby.be

# Bibliothèques disponibles
Voici une description des bibliothèques disponibles dans ce dépôt. <strong>Chaque sous-répertoire contient des instructions, schémas et codes dans un readme.md personnalisé.</strong>


Explorer par:
* Interface:
[FEATHERWING](docs/indexes/drv_by_intf_FEATHERWING.md), [GPIO](docs/indexes/drv_by_intf_GPIO.md), [HAT](docs/indexes/drv_by_intf_HAT.md), [I2C](docs/indexes/drv_by_intf_I2C.md), [NCD](docs/indexes/drv_by_intf_NCD.md), [ONEWIRE](docs/indexes/drv_by_intf_ONEWIRE.md), [PYBSTICK](docs/indexes/drv_by_intf_PYBSTICK.md), [QWIIC](docs/indexes/drv_by_intf_QWIIC.md), [SPI](docs/indexes/drv_by_intf_SPI.md), [STEMMA](docs/indexes/drv_by_intf_STEMMA.md), [UART](docs/indexes/drv_by_intf_UART.md), [UEXT](docs/indexes/drv_by_intf_UEXT.md), [UNO-R3](docs/indexes/drv_by_intf_UNO-R3.md)
* Fabriquant:
[ADAFRUIT](docs/indexes/drv_by_man_ADAFRUIT.md), [GARATRONIC](docs/indexes/drv_by_man_GARATRONIC.md), [MCHOBBY](docs/indexes/drv_by_man_MCHOBBY.md), [NCD](docs/indexes/drv_by_man_NCD.md), [NONE](docs/indexes/drv_by_man_NONE.md), [OLIMEX](docs/indexes/drv_by_man_OLIMEX.md), [POLOLU](docs/indexes/drv_by_man_POLOLU.md), [SPARKFUN](docs/indexes/drv_by_man_SPARKFUN.md)

<table>
<thead>
  <th>Répertoire</th><th>Description</th>
</thead>
<tbody>
  <tr><td><a href="../../tree/master/FEATHERWING">FEATHERWING</a></td>
      <td><strong>Composants</strong> : <br />
      <strong>Interfaces</strong> : FEATHERWING<br />
<small>Interface Feather pour Pyboard permettant de piloter des FeatherWings.</small><br/><br />
      <strong>Testé avec</strong> : PYBOARD<br />
      <strong>Fabricant</strong> : ADAFRUIT<br />
<ul>
<li>Voir <a href="https://shop.mchobby.be/fr/87-feather-adafruit">Feather board @ MCHobby</a></li>
<li>Voir <a href="https://www.adafruit.com/category/943">Feather boards @ Adafruit</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/NCD">NCD</a></td>
      <td><strong>Composants</strong> : <br />
      <strong>Interfaces</strong> : NCD<br />
<small>Brancher un connecteur NCD sur une Pyboard.</small><br/><br />
      <strong>Testé avec</strong> : PYBOARD<br />
      <strong>Fabricant</strong> : NCD<br />
<ul>
<li>Voir <a href="https://ncd.io/">UEXT breakout @ National Control Device</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/PYBStick">PYBStick</a></td>
      <td><strong>Composants</strong> : <br />
      <strong>Interfaces</strong> : PYBSTICK<br />
<small>PYBStick: une carte MicroPython abordable pour tous projets</small><br/><br />
      <strong>Testé avec</strong> : PYBSTICK<br />
      <strong>Fabricant</strong> : <br />
      </td>
  </tr>
  <tr><td><a href="../../tree/master/PYBStick-hat-face">PYBStick-hat-face</a></td>
      <td><strong>Composants</strong> : <br />
      <strong>Interfaces</strong> : PYBSTICK, HAT<br />
<small>Carte d'interface entre PYBStick et HAT pour Raspberry-Pi</small><br/><br />
      <strong>Testé avec</strong> : PYBSTICK<br />
      <strong>Fabricant</strong> : GARATRONIC<br />
<ul>
<li>Voir <a href="https://shop.mchobby.be/fr/nouveaute/1935-interface-pybstick-vers-raspberry-pi-3232100019355.html">PYBStick Hat Face @ MCHobby</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/QWIIC">QWIIC</a></td>
      <td><strong>Composants</strong> : <br />
      <strong>Interfaces</strong> : QWIIC, STEMMA<br />
<small>Brancher un connecteur QWIIC ou STEMMA sur une Pyboard.</small><br/><br />
      <strong>Testé avec</strong> : PYBOARD<br />
      <strong>Fabricant</strong> : SPARKFUN, ADAFRUIT<br />
<ul>
<li>Voir <a href="https://www.sparkfun.com/qwiic">QWIIC breakout @ SparkFun</a></li>
<li>Voir <a href="https://www.adafruit.com/category/1005">STEMMA breakout (Qwiic compatible) @ Adafruit</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/UEXT">UEXT</a></td>
      <td><strong>Composants</strong> : <br />
      <strong>Interfaces</strong> : UEXT<br />
<small>Brancher un port UEXT sur une Pyboard.</small><br/><br />
      <strong>Testé avec</strong> : PYBOARD<br />
      <strong>Fabricant</strong> : OLIMEX<br />
<ul>
<li>Voir <a href="https://shop.mchobby.be/fr/138-uext">UEXT breakout @ MCHobby</a></li>
<li>Voir <a href="https://www.olimex.com/Products/Modules/">UEXT breakout @ Olimex Ltd</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/UNO-R3">UNO-R3</a></td>
      <td><strong>Composants</strong> : OLED, SSD1306<br />
      <strong>Interfaces</strong> : UNO-R3<br />
<small>Arduino UNO R3 compatible interface for Pyboard</small><br/><br />
      <strong>Testé avec</strong> : PYBOARD<br />
      <strong>Fabricant</strong> : GARATRONIC<br />
      </td>
  </tr>
  <tr><td><a href="../../tree/master/UPPY">UPPY</a></td>
      <td><strong>Composants</strong> : <br />
      <strong>Interfaces</strong> : FEATHERWING, NCD, STEMMA, QWIIC, UEXT<br />
<small>UPPY (alpha) : Interface de Prototypage Universelle pour Pyboard.</small><br/><br />
      <strong>Testé avec</strong> : PYBOARD, PYBD<br />
      <strong>Fabricant</strong> : ADAFRUIT, OLIMEX, SPARKFUN, NCD<br />
      </td>
  </tr>
  <tr><td><a href="../../tree/master/UniPi-MicroPython-Automation">UniPi-MicroPython-Automation</a></td>
      <td><strong>Composants</strong> : <br />
      <strong>Interfaces</strong> : I2C<br />
<small>Créer un automate programmable MicroPython avec la PYBStick et UniPi</small><br/><br />
      <strong>Testé avec</strong> : PYBSTICK<br />
      <strong>Fabricant</strong> : <br />
<ul>
<li>Voir <a href="https://shop.mchobby.be/fr/nouveaute/1891-carte-interface-unipi-pro-et-lite-pour-pybstick-3232100018914.html">UniPiFace for PYBStick</a></li>
<li>Voir <a href="https://shop.mchobby.be/fr/tactile-flex-pot-softpad/83-clavier-16-touches-souple-3232100000834.html">UniPi V1.1</a></li>
<li>Voir <a href="https://shop.mchobby.be/fr/pi-extensions/1196-extension-unipi-lite-pour-raspberry-pi-3232100011960-unipi-technology.html">UniPi Lite</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/ads1015-ads1115">ads1015-ads1115</a></td>
      <td><strong>Composants</strong> : ADS1015, ADS1115, ADA1085<br />
      <strong>Interfaces</strong> : I2C<br />
<small>Convertisseur ADC (Analogique vers Digital) 4 canaux pour réaliser des lectures analogiques et lectures différentielles.<br />L'ADS1115 dispose d'un amplificateur interne programmable, ce qui permet de lire des tensions très faibles.</small><br/><br />
      <strong>Testé avec</strong> : PYBOARD<br />
      <strong>Fabricant</strong> : ADAFRUIT<br />
<ul>
<li>Voir <a href="https://shop.mchobby.be/breakout/362-ads1115-convertisseur-adc-16bits-i2c-3232100003620-adafruit.html">ADS1115 breakout</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/ctrl-panel">ctrl-panel</a></td>
      <td><strong>Composants</strong> : MCP23017, OLED, SSD1306<br />
      <strong>Interfaces</strong> : I2C, HAT<br />
<small>Panneau de contrôle en format HAT pour application MicroPython ou Raspberry-Pi.</small><br/><br />
      <strong>Testé avec</strong> : PYBSTICK<br />
      <strong>Fabricant</strong> : GARATRONIC<br />
<ul>
<li>Voir <a href="https://shop.mchobby.be/fr/nouveaute/1934-hat-panneau-de-controle-oled-joystick-bouton-led-3232100019348.html">Hat / Panneau de controle OLED + Joystick + bouton + LEDs</a></li>
<li>Voir <a href="https://shop.mchobby.be/fr/nouveaute/1935-interface-pybstick-vers-raspberry-pi-3232100019355.html">PYBStick Hat Face @ MCHobby</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/eth">eth</a></td>
      <td><strong>Composants</strong> : ETHERNET-FEATHERWING, WIZNET-W5500<br />
      <strong>Interfaces</strong> : SPI<br />
<small>Utiliser une connexion Ethernet filaire avec un contrôleur Wiznet W5500.</small><br/><br />
      <strong>Testé avec</strong> : PYBOARD<br />
      <strong>Fabricant</strong> : ADAFRUIT<br />
<ul>
<li>Voir <a href="https://shop.mchobby.be/fr/feather-adafruit/957-feather-ethernet-wing-3232100009578-adafruit.html">Ethernet FeatherWing @ MCHobby</a></li>
<li>Voir <a href="https://www.adafruit.com/product/3201">Adafruit Ethernet FeatherWing @ Adafruit</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/keypad-4x4">keypad-4x4</a></td>
      <td><strong>Composants</strong> : <br />
      <strong>Interfaces</strong> : GPIO<br />
<small>Utiliser un keypad 4x4 avec un microcontroleur MicroPython Pyboard</small><br/><br />
      <strong>Testé avec</strong> : PYBOARD<br />
      <strong>Fabricant</strong> : <br />
<ul>
<li>Voir <a href="https://shop.mchobby.be/fr/tactile-flex-pot-softpad/83-clavier-16-touches-souple-3232100000834.html">Clavier 16 touches souple @ MCHobby</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/mma7660">mma7660</a></td>
      <td><strong>Composants</strong> : MMA7660<br />
      <strong>Interfaces</strong> : I2C<br />
<small>Utiliser l'accéléromètre MMA7660 présent sur la Pyboard originale.</small><br/><br />
      <strong>Testé avec</strong> : PYBOARD<br />
      <strong>Fabricant</strong> : <br />
<ul>
<li>Voir <a href="https://shop.mchobby.be/fr/micropython/570-micropython-pyboard-3232100005709.html">Pyboard Originale (avec acceleromètre MMA7660) @ MCHobby</a></li>
<li>Voir <a href="https://store.micropython.org/product/PYBv1.1H">Original Pyboard (with MMA7660 accelerometer) @ MicroPython.org</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/mod-esp8266">mod-esp8266</a></td>
      <td><strong>Composants</strong> : MOD-ESP8266<br />
      <strong>Interfaces</strong> : UART<br />
<small>Utiliser un ESP8266 en commande AT pour obtenir une connexion WiFi on the Pyboard.</small><br/><br />
      <strong>Testé avec</strong> : PYBOARD<br />
      <strong>Fabricant</strong> : OLIMEX<br />
<ul>
<li>Voir <a href="https://shop.mchobby.be/fr/esp8266-esp32-wifi-iot/666-module-wifi-esp8266-uext-3232100006669-olimex.html">Module WiFi ESP8266 - connecteur UEXT @ MCHobby</a></li>
<li>Voir <a href="https://www.olimex.com/Products/IoT/ESP8266/MOD-WIFI-ESP8266/">MOD-WIFI-ESP826 @ Olimex.com</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/modvga">modvga</a></td>
      <td><strong>Composants</strong> : MOD-VGA<br />
      <strong>Interfaces</strong> : UEXT<br />
<small>Contrôler un adaptateur VGA type GameDuino via une interface UEXT.</small><br/><br />
      <strong>Testé avec</strong> : PYBOARD<br />
      <strong>Fabricant</strong> : OLIMEX<br />
<ul>
<li>Voir <a href="https://shop.mchobby.be/fr/uext/1431-mod-vga-carte-type-gameduino-en-33v-3232100014312-olimex.html">MOD-VGA : carte type Gameduino en 3.3V @ MCHobby</a></li>
<li>Voir <a href="https://www.olimex.com/Products/Modules/Video/MOD-VGA/">Arduino-compatible Gameduino-based extension shield @ Olimex</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/motorskin">motorskin</a></td>
      <td><strong>Composants</strong> : L293D, HC-SR04<br />
      <strong>Interfaces</strong> : GPIO<br />
<small>Carte d'extension moteur pour MicroPython PyBoard + capteur de distance ultrason.</small><br/><br />
      <strong>Testé avec</strong> : PYBOARD<br />
      <strong>Fabricant</strong> : MCHOBBY<br />
<ul>
<li>Voir <a href="https://shop.mchobby.be/fr/micropython/918-pyboard-motor-skin-3232100009189.html">PyBoard Motor Skin KIT @ MCHobby</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/ressource">ressource</a></td>
      <td><strong>Composants</strong> : <br />
      <strong>Interfaces</strong> : <br />
<small>*** RESSOURCES *** Fritzing, brochage et schémas pour la Pyboard et Pyboard-D (PYBD).</small><br/><br />
      <strong>Testé avec</strong> : PYBOARD, PYBD<br />
      <strong>Fabricant</strong> : <br />
      </td>
  </tr>
  <tr><td><a href="../../tree/master/servorobot">servorobot</a></td>
      <td><strong>Composants</strong> : PCA9685<br />
      <strong>Interfaces</strong> : I2C<br />
<small>Créer un robot à 4 pattes avec des servo-moteurs et un contrôleur PWM PCA9685.</small><br/><br />
      <strong>Testé avec</strong> : PYBOARD<br />
      <strong>Fabricant</strong> : ADAFRUIT<br />
<ul>
<li>Voir <a href="https://shop.mchobby.be/fr/moteur/913-allbot-patte-2-servo-vr012-3232100009134-velleman.html">AllBot Patte 2 Servo @ MCHobby</a></li>
<li>Voir <a href="https://shop.mchobby.be/fr/breakout/89-adafruit-controleur-pwm-servo-16-canaux-12-bits-i2c-interface-pca9685-3232100000896-adafruit.html">PWM Driver (PCA9685) @ MCHobby</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/usbhid">usbhid</a></td>
      <td><strong>Composants</strong> : <br />
      <strong>Interfaces</strong> : <br />
<small>Exemples expliquant comment utiliser la Pyboard comme périphérique HID (clavier, souris)</small><br/><br />
      <strong>Testé avec</strong> : PYBOARD<br />
      <strong>Fabricant</strong> : <br />
      </td>
  </tr>
  <tr><td><a href="../../tree/master/zumo-robot">zumo-robot</a></td>
      <td><strong>Composants</strong> : <br />
      <strong>Interfaces</strong> : UNO-R3<br />
<small>Piloter un Robot Zumo pour Arduino avec un microcontroleur MicroPython Pyboard</small><br/><br />
      <strong>Testé avec</strong> : PYBOARD<br />
      <strong>Fabricant</strong> : POLOLU<br />
<ul>
<li>Voir <a href="https://shop.mchobby.be/fr/prototypage-robotique-roue/448-robot-zumo-pour-arduino-assemble-moteurs-3232100004481-pololu.html">Zumo Robot @ MCHobby</a></li>
<li>Voir <a href="https://www.pololu.com/product/2510">Zumo Robot @ Pololu</a></li>
</ul>
      </td>
  </tr>
</tbody>
</table>

## RShell

__RShell__ est un outil formidable qui permet de d'éditer/transférer/repl sur une carte MicroPython a travers une simple connexion série (et même Bluetooth serial).

C'est un outil vraiment _très utile_ qui vaut la peine de s'y attarder... avec lui plus besoin d'avoir accès au "lecteur Flash" de votre carte MicroPython pour y éditer ou y copier un fichier.

Ce qu'il y de génial avec RShell, c'est qu'il fonctionne aussi avec ESP8266 (tant mieux parce qu'il n'y a pas de _lecteur flash_ comme sur une PyBoard).

 * [Tuto RShell en Français](https://wiki.mchobby.be/index.php?title=MicroPython-Hack-RShell)
 * [Github de rshell](https://github.com/dhylands/rshell) - documentation et instruction d'installation.
 * [rshell-esp8266.sh](rshell-esp8266.sh) - A adapater. Appel RShell avec buffer réduit pour ESP8266.

__ATTENTION__ : pour un ESP8266 il faut absolument réduire le buffer d'échange... sinon on écrase facilement le système de fichier (et il faudra reflasher la bête) :-/  Voyez le fichier [rshell-esp8266.sh](rshell-esp8266.sh) qui est proposé ici.

# Lien divers

De nombreux pilotes MicroPython sont disponible sur le GitHUb esp8266-upy
* https://github.com/mchobby/esp8266-upy

Il y a de nombreux pilotes Adafruit sur ce Github (Tony Dicola)
* https://github.com/adafruit/micropython-adafruit-bundle/tree/master/libraries/drivers

Il y a de nombreux pilotes Adafruit sur ce Github (Tony Dicola)
* https://github.com/adafruit/micropython-adafruit-bundle/tree/master/libraries/drivers

Également trouvé des pilotes pour centrales Intertielles sur ce Github
* https://github.com/micropython-IMU/
