[Ce fichier existe également en Français ici](readme.md)

# Introduction

This repository contains MicroPython drivers for the Pyboard. It also relies on the [esp8266-upy](https://github.com/mchobby/esp8266-upy) containing lot of MicroPython drivers running on ESP8266 (__if it runs on ESP8266 it will also run on Pyboard!__).

The code and sample here are also used in the [MCHobby's French documentation Wiki about the Pyboard](https://wiki.mchobby.be/index.php?title=MicroPython-Accueil).

# Ressources & projects

<table>
<thead>
  <th>Folder</th><th>Sensor / Description</th>
</thead>
<tbody>
  <tr><td><strong>ressource/Fritzing</strong></td>
      <td>Fritzing file of the Pyboard.<br />
      </td>
  </tr>
  <tr><td><strong>UEXT</strong></td>
      <td>UEXT pinout and wiring proposal for the Pyboard.<br /><br />
More info: <a href="https://www.olimex.com/Products/Modules/">UEXT product line @ Olimex</a><br />
More info: <a href="https://shop.mchobby.be/fr/138-uext">UEXT product line @ MCHobby</a>
      </td>
  </tr>
	<tr><td><strong>NCD</strong></td>
      <td>NCD pinout and wiring proposal for the Pyboard.<br /><br />
More info: <a href="https://ncd.io/">NCD sensor boards @ National Control Device</a>
      </td>
  </tr>
  <tr><td>Servo Robot</td>
      <td>Use a pca9685 PWM driver to create quadruped robot (with servo motors).
      </td>
  </tr>

</tbody>
</table>

# Available drivers

<table>
<thead>
  <th>Folder</th><th>Sensor / Description</th>
</thead>
<tbody>
	<tr><td>MOD-VGA<br />GameDuino</td>
			<td>3.3V GameDuino shield with VGA output, sound output, keyboard input and  __UEXT connector__ (to communicate with the Pyboard). Allows to display texte within the VGA mode.</a><br /><br />
	More information: <a href="https://shop.mchobby.be/fr/uext/1431-mod-vga-carte-type-gameduino-en-33v-3232100014312-olimex.html">MOD-VGA</a>
			</td>
	</tr>

  <tr><td>MotorSkin<br />L293D</td>
      <td>A DC motor controler (for 2 motors) based on the L293D. Comes from the project <a href="https://wiki.mchobby.be/index.php?title=Hack-ENG-MotorSkin">Pyboard à roulette documenté sur le Wiki de MCHobby.</a> (<a href="https://wiki.mchobby.be/index.php?title=Hack-MotorSkin">French version</a>)<br /><br />
More information: <a href="https://shop.mchobby.be/fr/micropython/918-pyboard-motor-skin-3232100009189.html">MotorSkin</a>
      </td>
  </tr>

  <tr><td>PCA9685</td>
      <td>The PCA9685 PWM driver offering 16 channels to drive servo-motors and LEDs<br /><br />
Plus d'info: <a href="https://shop.mchobby.be/fr/breakout/89-adafruit-controleur-pwm-servo-16-canaux-12-bits-i2c-interface-pca9685-3232100000896-adafruit.html">16 channel PWM controler - 12 bits - I2C interface - PCA9685</a>
      </td>
  </tr>

  <tr><td><strong>Other drivers<br />(esp8266-upy)</strong></td>
      <td>The <a href="https://github.com/mchobby/esp8266-upy">esp8266-upy github</a> contains many other MicroPython drivers.

If it runs on the ESP8266 (having lfew ressources), those drivers will also run on a Pyboard!
      </td>
  </tr>

</tbody>
</table>
