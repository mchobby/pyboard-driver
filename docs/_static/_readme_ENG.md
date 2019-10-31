[Ce fichier existe également en FRANCAIS](readme.md)

# MicroPython driver Pyboard's specific

This repository contains specific MicroPython drivers for Pyboard (requiring more memory or specific hardware support).

The drivers "plateform agnostic" based on the __machine API__ are stored in the [esp8266-upy](https://github.com/mchobby/esp8266-upy) repository.

The code and sample here are also used in the [MCHobby's French documentation Wiki about the Pyboard](https://wiki.mchobby.be/index.php?title=MicroPython-Accueil).

# Available libraries
Here is a description of the libraries available in this repository. <strong>Each sub-folders contain README file with additionnal informations about the driver, examples and wiring.</strong>

Explore it by:
* Interface:
@@interface_list:{'lang_code':'eng','str':'[%code%](docs/indexes/drv_by_intf_%code%_ENG.md)'} # List per interface

* Manufacturer:
@@manufacturer_list:{'lang_code':'eng','str':'[%code%](docs/indexes/drv_by_man_%code%_ENG.md)'} # List per manufacturer

@@driver_table:{'lang_code':'eng'} # Insert the driver table

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
