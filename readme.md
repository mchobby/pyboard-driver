[This file also exists in english here](readme_eng.md)

# Introduction

Ce dépôt contient des pilotes MicroPython pour PyBoard . Il s'appuie également sur le dépôt [esp8266-upy](https://github.com/mchobby/esp8266-upy) contenant de nombreux pilotes MicroPython pour ESP8266 (__Si cela fonctionne sur ESP8266 alors cela fonctionnera aussi sur la Pyboard!__).

Les codes et exemples sont également utilisés sur le [wiki documentaire Pyboard de MCHobby](https://wiki.mchobby.be/index.php?title=MicroPython-Accueil).

# Ressources & projets

<table>
<thead>
  <th>Répertoire</th><th>Senseur / Description</th>
</thead>
<tbody>
  <tr><td><strong>ressource/Fritzing</strong></td>
      <td>Fichiers Fritzing pour la carte Pyboard.<br />
      </td>
  </tr>
  <tr><td><strong>UEXT</strong></td>
      <td>Proposition de brochage et connectique UEXT pour la carte Pyboard.<br /><br />
Plus d'info: <a href="https://www.olimex.com/Products/Modules/">gamme UEXT @ Olimex</a><br />
Plus d'info: <a href="https://shop.mchobby.be/fr/138-uext">gamme UEXT @ MCHobby</a>
      </td>
  </tr>
	<tr><td><strong>NCD</strong></td>
      <td>Proposition de brochage et connectique NCD pour la carte Pyboard.<br /><br />
Plus d'info: <a href="https://ncd.io/">gamme NCD @ National Control Device</a>
      </td>
  </tr>
  <tr><td>Servo Robot</td>
      <td>Utiliser un controleur PWM pca9685 pour réaliser un robot quadripède (à servo-moteurs).
      </td>
  </tr>

</tbody>
</table>

# Bibliothèques disponibles

<table>
<thead>
  <th>Répertoire</th><th>Senseur / Description</th>
</thead>
	<tbody>
	<tr><td>MOD-VGA<br />GameDuino</td>
			<td>Shield GameDuino 3.3V avec sortie VGA, sortie Son entrée clavier et __connecteur UEXT__ (pour la communication avec Pyboard). Permet de faire des affichages de texte en VGA.</a><br /><br />
	Plus d'info: <a href="https://shop.mchobby.be/fr/uext/1431-mod-vga-carte-type-gameduino-en-33v-3232100014312-olimex.html">MOD-VGA</a>
			</td>
	</tr>

  <tr><td>MotorSkin<br />L293D</td>
      <td>Contrôleur pour deux moteurs continu basé sur un L293D. Provient du projet <a href="https://wiki.mchobby.be/index.php?title=Hack-MotorSkin">Pyboard à roulette documenté sur le Wiki de MCHobby.</a><br /><br />
Plus d'info: <a href="https://shop.mchobby.be/fr/micropython/918-pyboard-motor-skin-3232100009189.html">MotorSkin</a>
      </td>
  </tr>

  <tr><td>PCA9685</td>
      <td>Le PCA9685 est un contrôleur PWM à 16 canaux pour piloter servo moteur ou LEDs<br /><br />
Plus d'info: <a href="https://shop.mchobby.be/fr/breakout/89-adafruit-controleur-pwm-servo-16-canaux-12-bits-i2c-interface-pca9685-3232100000896-adafruit.html">Controleur PWM Servo 16 canaux 12 bits - I2C interface - PCA9685</a>
      </td>
  </tr>

  <tr><td><strong>Autres pilotes<br />(esp8266-upy)</strong></td>
      <td>Le <a href="https://github.com/mchobby/esp8266-upy">github esp8266-upy</a> contient de nombreux autres pilotes MicroPython.

Puisqu'ils fonctionnent sur ESP8266 (ayant moins de ressources), ces pilotes fonctionnerons également avec des cartes Pyboard!
      </td>
  </tr>

</tbody>
</table>
