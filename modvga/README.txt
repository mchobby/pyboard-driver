[This file also exists in ENGLISH](README_eng.md)

# MODVGA - GameDuino 3.3V avec connecteur UEXT

![MOV-VGA branché sur une Pyboard](modvga.jpg)

La MOD-VGA est un shield 3.3V basé sur la populaire conception de Gameduino.

Quelques modification on été apportées pour ajouter une sortie Audio, un clavier PS2 et __un connecteur UEXT__ permettant d'utiliser le shield avec toutes les cartes disposant d'un connecteur/sortie UEXT.

# ATTENTION
Une bonne partie de la bibliothèque GameDuino est disponible dans le fichier `gd.py` mais seuls quelques exemples ont étés portés sous MicroPython.

Ce port MicroPython est orienté vers l'affichage de texte. Le but étant de créer un terminal REPL VGA pour utiliser une carte MicroPython Pyboard sur un moniteur VGA.

Les autres fonctionnalités/exemples seront portés en fonction du temps disponible et intérêts personnels.

# Comment brancher

Comme vous pouvez le voir, la carte MOD-VGA est branchée sur la Pyboard via le connecteur UEXT.
* bus SPI exploité pour communication avec GameDuino
* bus I2C (a confirmer) utiliser pour le connecteur PS2

Vous pouvez en apprendre plus sur ce connecteur __et son câblage__ dans le GitHub [connecteur UEXT pour Pyboard](https://github.com/mchobby/pyboard-driver/tree/master/UEXT).

![connecteur UEXT sur Pyboard](https://raw.githubusercontent.com/mchobby/pyboard-driver/master/UEXT/UEXT-Breakout-LowRes.jpg)

# Où acheter

* [MOD-VGA @ shop.mchobby.be ](https://shop.mchobby.be/uext/1431-mod-vga-33v-gameduino-alike-board-3232100014312-olimex.html)
* [UEXT boards @ shop.mchobby.be](https://shop.mchobby.be/fr/138-uext)
* [MOD-VGA @ Olimex](https://www.olimex.com/Products/Modules/Video/MOD-VGA/open-source-hardware)
* [Pyboard @ shop.mchobby.be](https://shop.mchobby.be/fr/micropython/570-micropython-pyboard-3232100005709.html)
