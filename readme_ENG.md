[Ce fichier existe également en FRANCAIS](readme.md)

# MicroPython driver Pyboard's specific

This repository contains specific MicroPython drivers for Pyboard (requiring more memory or specific hardware support).

The drivers "plateform agnostic" based on the __machine API__ are stored in the [esp8266-upy](https://github.com/mchobby/esp8266-upy) repository.

The code and sample here are also used in the [MCHobby's French documentation Wiki about the Pyboard](https://wiki.mchobby.be/index.php?title=MicroPython-Accueil).

# Available libraries
Here is a description of the libraries available in this repository. <strong>Each sub-folders contain README file with additionnal informations about the driver, examples and wiring.</strong>

Explore it by:
* Interface:
[FEATHERWING](docs/indexes/drv_by_intf_FEATHERWING_ENG.md), [GPIO](docs/indexes/drv_by_intf_GPIO_ENG.md), [I2C](docs/indexes/drv_by_intf_I2C_ENG.md), [NCD](docs/indexes/drv_by_intf_NCD_ENG.md), [ONEWIRE](docs/indexes/drv_by_intf_ONEWIRE_ENG.md), [QWIIC](docs/indexes/drv_by_intf_QWIIC_ENG.md), [SPI](docs/indexes/drv_by_intf_SPI_ENG.md), [STEMMA](docs/indexes/drv_by_intf_STEMMA_ENG.md), [UART](docs/indexes/drv_by_intf_UART_ENG.md), [UEXT](docs/indexes/drv_by_intf_UEXT_ENG.md), [UNO-R3](docs/indexes/drv_by_intf_UNO-R3_ENG.md)
* Manufacturer:
[ADAFRUIT](docs/indexes/drv_by_man_ADAFRUIT_ENG.md), [MCHOBBY](docs/indexes/drv_by_man_MCHOBBY_ENG.md), [NCD](docs/indexes/drv_by_man_NCD_ENG.md), [NONE](docs/indexes/drv_by_man_NONE_ENG.md), [OLIMEX](docs/indexes/drv_by_man_OLIMEX_ENG.md), [SPARKFUN](docs/indexes/drv_by_man_SPARKFUN_ENG.md)
<table>
<thead>
  <th>Folder</th><th>Description</th>
</thead>
<tbody>
  <tr><td><a href="../../tree/master/FEATHERWING">FEATHERWING</a></td>
      <td><strong>Components</strong> : <br />
      <strong>Interfaces</strong> : FEATHERWING<br />
<small>Feather Interface for Pyboard allowing to control FeatherWings.</small><br/><br />
      <strong>Tested with</strong> : PYBOARD<br />
      <strong>Manufacturer</strong> : ADAFRUIT<br />
<ul>
<li>See <a href="https://shop.mchobby.be/fr/87-feather-adafruit">Feather board @ MCHobby</a></li>
<li>See <a href="https://www.adafruit.com/category/943">Feather boards @ Adafruit</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/NCD">NCD</a></td>
      <td><strong>Components</strong> : <br />
      <strong>Interfaces</strong> : NCD<br />
<small>Wiring an NCD connector to Pyboard.</small><br/><br />
      <strong>Tested with</strong> : PYBOARD<br />
      <strong>Manufacturer</strong> : NCD<br />
<ul>
<li>See <a href="https://ncd.io/">UEXT breakout @ National Control Device</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/QWIIC">QWIIC</a></td>
      <td><strong>Components</strong> : <br />
      <strong>Interfaces</strong> : QWIIC, STEMMA<br />
<small>Wiring a QWIIC or STEMMA connector to Pyboard.</small><br/><br />
      <strong>Tested with</strong> : PYBOARD<br />
      <strong>Manufacturer</strong> : SPARKFUN, ADAFRUIT<br />
<ul>
<li>See <a href="https://www.sparkfun.com/qwiic">QWIIC breakout @ SparkFun</a></li>
<li>See <a href="https://www.adafruit.com/category/1005">STEMMA breakout (Qwiic compatible) @ Adafruit</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/UEXT">UEXT</a></td>
      <td><strong>Components</strong> : <br />
      <strong>Interfaces</strong> : UEXT<br />
<small>Wiring an UEXT connector to Pyboard.</small><br/><br />
      <strong>Tested with</strong> : PYBOARD<br />
      <strong>Manufacturer</strong> : OLIMEX<br />
<ul>
<li>See <a href="https://shop.mchobby.be/fr/138-uext">UEXT breakout @ MCHobby</a></li>
<li>See <a href="https://www.olimex.com/Products/Modules/">UEXT breakout @ Olimex Ltd</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/UNO-R3">UNO-R3</a></td>
      <td><strong>Components</strong> : <br />
      <strong>Interfaces</strong> : UNO-R3<br />
<small>(ALPHA version) Create a 4 paws servo-motor walking robot with a PCA9685 PWM controler.</small><br/><br />
      <strong>Tested with</strong> : PYBOARD<br />
      <strong>Manufacturer</strong> : <br />
      </td>
  </tr>
  <tr><td><a href="../../tree/master/UPPY">UPPY</a></td>
      <td><strong>Components</strong> : <br />
      <strong>Interfaces</strong> : FEATHERWING, NCD, STEMMA, QWIIC, UEXT<br />
<small>UPPY (alpha) : Universal Prototyping interface for Pyboard.</small><br/><br />
      <strong>Tested with</strong> : PYBOARD, PYBD<br />
      <strong>Manufacturer</strong> : ADAFRUIT, OLIMEX, SPARKFUN, NCD<br />
      </td>
  </tr>
  <tr><td><a href="../../tree/master/ads1015-ads1115">ads1015-ads1115</a></td>
      <td><strong>Components</strong> : ADS1015, ADS1115, ADA1085<br />
      <strong>Interfaces</strong> : I2C<br />
<small>ADC converter (Analog to Digital) 4 channel allowing analog reading and differential reading.<br />L'ADS1115 have a internal amplifier (programmable) that can be used to read very small voltage.</small><br/><br />
      <strong>Tested with</strong> : PYBOARD<br />
      <strong>Manufacturer</strong> : ADAFRUIT<br />
<ul>
<li>See <a href="https://shop.mchobby.be/breakout/362-ads1115-convertisseur-adc-16bits-i2c-3232100003620-adafruit.html">ADS1115 breakout</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/eth">eth</a></td>
      <td><strong>Components</strong> : ETHERNET-FEATHERWING, WIZNET-W5500<br />
      <strong>Interfaces</strong> : SPI<br />
<small>Use a Wired Ethernet connection with a Wiznet W5500 Ethernet controler.</small><br/><br />
      <strong>Tested with</strong> : PYBOARD<br />
      <strong>Manufacturer</strong> : ADAFRUIT<br />
<ul>
<li>See <a href="https://shop.mchobby.be/fr/feather-adafruit/957-feather-ethernet-wing-3232100009578-adafruit.html">Ethernet FeatherWing @ MCHobby</a></li>
<li>See <a href="https://www.adafruit.com/product/3201">Adafruit Ethernet FeatherWing @ Adafruit</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/mma7660">mma7660</a></td>
      <td><strong>Components</strong> : MMA7660<br />
      <strong>Interfaces</strong> : I2C<br />
<small>Use the MMA7660 accelerometer available on the Pyboard original.</small><br/><br />
      <strong>Tested with</strong> : PYBOARD<br />
      <strong>Manufacturer</strong> : <br />
<ul>
<li>See <a href="https://shop.mchobby.be/fr/micropython/570-micropython-pyboard-3232100005709.html">Pyboard Originale (avec acceleromètre MMA7660) @ MCHobby</a></li>
<li>See <a href="https://store.micropython.org/product/PYBv1.1H">Original Pyboard (with MMA7660 accelerometer) @ MicroPython.org</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/mod-esp8266">mod-esp8266</a></td>
      <td><strong>Components</strong> : MOD-ESP8266<br />
      <strong>Interfaces</strong> : UART<br />
<small>Use an ESP8266 under AT command to grab a WiFi connexion on the Pyboard.</small><br/><br />
      <strong>Tested with</strong> : PYBOARD<br />
      <strong>Manufacturer</strong> : OLIMEX<br />
<ul>
<li>See <a href="https://shop.mchobby.be/fr/esp8266-esp32-wifi-iot/666-module-wifi-esp8266-uext-3232100006669-olimex.html">Module WiFi ESP8266 - connecteur UEXT @ MCHobby</a></li>
<li>See <a href="https://www.olimex.com/Products/IoT/ESP8266/MOD-WIFI-ESP8266/">MOD-WIFI-ESP826 @ Olimex.com</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/modvga">modvga</a></td>
      <td><strong>Components</strong> : MOD-VGA<br />
      <strong>Interfaces</strong> : UEXT<br />
<small>Contrôle an Gameduino based VGA adapter through a UEXT connector.</small><br/><br />
      <strong>Tested with</strong> : PYBOARD<br />
      <strong>Manufacturer</strong> : OLIMEX<br />
<ul>
<li>See <a href="https://shop.mchobby.be/fr/uext/1431-mod-vga-carte-type-gameduino-en-33v-3232100014312-olimex.html">MOD-VGA : carte type Gameduino en 3.3V @ MCHobby</a></li>
<li>See <a href="https://www.olimex.com/Products/Modules/Video/MOD-VGA/">Arduino-compatible Gameduino-based extension shield @ Olimex</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/motorskin">motorskin</a></td>
      <td><strong>Components</strong> : L293D, HC-SR04<br />
      <strong>Interfaces</strong> : GPIO<br />
<small>Motor skin for MicroPython PyBoard + ultrasonic distance sensor.</small><br/><br />
      <strong>Tested with</strong> : PYBOARD<br />
      <strong>Manufacturer</strong> : MCHOBBY<br />
<ul>
<li>See <a href="https://shop.mchobby.be/fr/micropython/918-pyboard-motor-skin-3232100009189.html">PyBoard Motor Skin KIT @ MCHobby</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/ressource">ressource</a></td>
      <td><strong>Components</strong> : <br />
      <strong>Interfaces</strong> : <br />
<small>*** RESSOURCES *** Fritzing, Pinouts and schematic for Pyboard and Pyboard-D (PYBD).</small><br/><br />
      <strong>Tested with</strong> : PYBOARD, PYBD<br />
      <strong>Manufacturer</strong> : <br />
      </td>
  </tr>
  <tr><td><a href="../../tree/master/servorobot">servorobot</a></td>
      <td><strong>Components</strong> : PCA9685<br />
      <strong>Interfaces</strong> : <br />
<small>Create Pyboard's based walking robot with micro Servo Robot and PWM Driver.</small><br/><br />
      <strong>Tested with</strong> : PYBOARD<br />
      <strong>Manufacturer</strong> : ADAFRUIT<br />
      </td>
  </tr>
  <tr><td><a href="../../tree/master/servorobot">servorobot</a></td>
      <td><strong>Components</strong> : PCA9685<br />
      <strong>Interfaces</strong> : I2C<br />
<small>Create a 4 paws servo-motor walking robot with a PCA9685 PWM controler.</small><br/><br />
      <strong>Tested with</strong> : PYBOARD<br />
      <strong>Manufacturer</strong> : <br />
<ul>
<li>See <a href="https://shop.mchobby.be/fr/moteur/913-allbot-patte-2-servo-vr012-3232100009134-velleman.html">AllBot Patte 2 Servo @ MCHobby</a></li>
</ul>
      </td>
  </tr>
</tbody>
</table>

## RShell

__RShell__ is a wonderfull tool used to edit/transfert/repl your board running MicroPython from a single serial connexion (or Serial over bluetooth).

It is a _really useful_ that would be great to learn... with RShell, you can access the MicroPython filesystem (in Flash memory) to edit and copy files.

The wonderfulnes of RShell, is that it also works great with ESP8266 (thankfully because there are no way to emulate USB Mass Storage on ESP8266, a _flash drive_ like is work with the genuine PyBoard).

 * [French tutorial on RShell](https://wiki.mchobby.be/index.php?title=MicroPython-Hack-RShell)
 * [Rshell GitHub](https://github.com/dhylands/rshell) - with english documentation and installation instruction.
 * [rshell-esp8266.sh](rshell-esp8266.sh) - to update. Calls RShell with a small size exchange buffer (needed for ESP8266).

__WARNING__ : On a ESP8266 it is necessary to reduce the exchange buffer... otherwise, it may corrupt the MicroPython filesystem (and it would be necessary to re-flash the ESP8266 with MicroPython) :-/  See the file [rshell-esp8266.sh](rshell-esp8266.sh) suggested in this repository.


# Various links

Many MicroPython drivers are already available on the esp8266-upy GitHub
* https://github.com/mchobby/esp8266-upy

There are many Adafruit  drivers (various plateforms) on this Github (Tony Dicola)
* https://github.com/adafruit/micropython-adafruit-bundle/tree/master/libraries/drivers

And some IMU (inertial sensor) driver on Github
* https://github.com/micropython-IMU/
