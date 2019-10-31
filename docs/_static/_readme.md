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
@@interface_list:{'lang_code':'fr','str':'[%code%](docs/indexes/drv_by_intf_%code%.md)'} # List per interface

* Fabriquant:
@@manufacturer_list:{'lang_code':'fr','str':'[%code%](docs/indexes/drv_by_man_%code%.md)'} # List per manufacturer


@@driver_table:{'lang_code':'fr'} # Insert the driver table

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
