# Flashing
Voir la documentation de la PYBStick pour flasher votre carte PYBStick.

Voici la commande de référence pour le flashage:

```
sudo dfu-util -a 0 -D fw_pybstick26std_20200506.dfu
```

# PYBStick Standard 26

* [fw_pybstick26std_20200509-0.dfu](fw_pybstick26std_20200509-0.dfu) - 09 mai 2020 - MicroPython 1.12!
* [fw_pybstick26std_20200513-0.dfu](fw_pybstick26std_20200513-0.dfu) - 13 mai 2020 - MicroPython 1.12!
 * Régression servo (0 à -90)

# PYBStick Standard 26 NUSB (no usb)
Cette version du firmware duplique la console REPL sur UART(2). Voir fichier `boot.py`

* [fw_pybstick26std_nusb_20200520-0.dfu](fw_pybstick26std_nusb_20200520-0.dfu) - 20 mai 2020 - MicroPython 1.12!
