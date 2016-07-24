Motor-Skin 
==========

Dear english friends, an English version of this file is available in readme.md 

Chers amis Francophone, cette version du fichier est pour vous

Introduction
------------
J'ai placé des pilotes utiles pour le motor-skin dans cette bibliothèque.

Le but du motor-skin est de vous permettre de placer des roues sous votre carte MicroPython PyBoard pour qu'elle puisse se déplacer ici et là. 

Supportez nous, nos traductions libres et nos projets (librement disponible sur wiki.mchobby.be) en achetant vos produits sur shop.mchobby.be 

Vous pouvez redistribuer et/ou modifier le code que vous trouverez dans 
cette bibliothèque sous les termes de la licence GNU GPLv3 (voir le détail ci-dessous)

You can redistribute it and/or modify the code found in this repository
under the terms of the GNU GPLv3 license detailed above.

Wiki, branchement, Shop
------------------------
Les informations sur le projet, raccordement et recommandations sont disponibles sur notre Wiki
* __TODO__

La liste du matériel et liens vers le WebShop (France & Belgique)
* https://shop.mchobby.be/micro-python/918-pyboard-motor-skin-3232100009189.html
* https://shop.mchobby.be/micro-python/919-pyboard-a-roulette-3232100009196.html

Installer la bibliothèque:
--------------------------
Copiez simplement les fichiers '.py' disponibles dans le sous répertoire "motorskin" dans le répertoire principal (dit répertoire ''root'') dans votre lecteur PyBoard (la PYFLASH).

Une fois fait, vous pourrez utiliser la commande standard "import" pour utiliser la bibliothèue dans vos propres scripts.

Bibliothèques
-------------
Tous les fichiers des pilotes (et bibliothèques) sont stockés dans des répertoires différents et le code est sub-divisé en plusieurs fichiers/parties en fonction du périphérique/Senseur que vous avez besoin d'utiliser.

* __motorskin\hbridge.py__ : Bibliothèque HBridge pour un simple Pont-H (contrôle d'un moteur) et DualHBridge (deux moteurs).
 * Indiqué pour piloter directement un L293D
 * Les deux classes contiennent des méthodes de bases pour les mouvements (__forward, backward, halt__ pour avant, arriere, arret) avec gestion de la vitesse.
 * La classe DualHBridge prend en charge la dérivation provoquée par l'infime différence entre deux moteurs supposés identiques (deux moteurs ne sont jamais exactements identiques) 
* __motorskin\motorskin.py__ : bibliothèque avec la classe MotorSkin (complétant la classe DualHBridge) pour contrôler deux pont-H et un senseur Ultrason 
* __motorskin\r2wheel.py__ : Bibliothque avec la classe Robot2Wheel (complétant la classe MotorSkin) pour contrôler une plateforme robotique 2 roues (moteurs continu).
 * Implémente la méthode turn() avec RIGHT_ROTATE, LEFT_ROTATE, RIGHT_BEND, LEFT_BEND
 * Implémente les méthodes right() et left() plus pratique
 * Permet d'inverser la marche avant/arrière (forward/backward) via le code pour chacun des moteurs (gestion via le code plutôt que de modifier le câblage)
 * Permet d'interchanger les moteurs droit et gauche (right/left) par code (gestion via le code plutôt que de modifier les branchements moteurs)
* __motorskin\ultrasonic.py__ : Bibliothèque pour le senseur ultrason HC-SR04 permettant de mesurer des distances (par Sergio Conde Gómez, GPL V3, voyez l'entête du fichier pour plus de détails)

Historique
-----------
La carte d'extension motor-skin est le résultat du projet "PyBoard-à-roulette" que vous pourrez trouver ici [here](https://wiki.mchobby.be/index.php?title=MicroPython-Accueil#PyBoard_.C3.A0_roulette)

Le projet initial a été conduit en plusieurs étapes dépendant des différentes requêtes, contributions et idées d'implementations.

Licence: GPL v3
---------------
Copyright 2016 - Meurisse D <info[at]mchobby[dot]com> - http://shop.mchobby.be
_Voyez sur internet pour une traduction française adéquate_

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

