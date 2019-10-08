[Ce fichier existe également en FRANCAIS](readme.md)

# Using ESP8266 on pyboard to gain WiFi connectivity

The Olimex's MOD-WIFI-ESP8266 is preconfigured with AT Command firmware allowing the module to be used as WiFi modem.

![Plug MOD-WIFI-ESP8266 on a Pyboard](docs/_static/mod-wifi-esp8266-to-pyboard.jpg)

## Note about the ESP8266
* The ESP UART is set to 115200 bauds 8N1 by default
* The ESP Firmware REQUIRES the command to end with \r\l (CR+LF)
* When working properly the ESP8266 does ECHO the received byte to the TX.
* Starts in access point AP mode.

# wiring

The easiest way to wire the MOD-WIFI-ESP8266 module is to plug it onto an UEXT connector.

The MOD-WIFI-ESP8266 use the following connexions:
* 3.3V and GND
* RX and TX

You may learn more about this connector and its __wiring to the Pyboard__ with [UEXT connector for Pyboard](https://github.com/mchobby/pyboard-driver/tree/master/UEXT).

![UEXT connector on Pyboard](https://raw.githubusercontent.com/mchobby/pyboard-driver/master/UEXT/UEXT-Breakout-LowRes.jpg)

# test

## PassThrough
This example will forward all serial data coming from ESP8266 Serial Port to USB VCP (Virtual Com Port). Making it working back and forward.

This script be great to test the AT Commands on the ESP8266 module.

Just run the `passthrough.py` script and press USR button to cancel the the execution.

Here a REPL Session with a commented example of passthrough

```
MicroPython v1.10-278-g673e154df on 2019-04-13; PYBv1.1 with STM32F405RG
Type "help()" for more information.
>>>
>>> import passthrough
Activating UART<->USB passthrough...
  debug        = False
  enforce_crlf = True
press USR button while sending a byte to EXIT
Ready!
# Test the simpliest command ever!
AT

OK

# Passer en mode station
AT+CWMODE=3

OK

# Scan des réseaux
AT+CWLAP
+CWLAP:(3,"ATCG103",-71,"40:f2:01:88:1e:0a",6,75,0)

OK

# Connect the network ATCG103
AT+CWJAP="ATCG103","password"
WIFI CONNECTED
WIFI GOT IP

OK

# Which network is connected?
AT+CWJAP?
+CWJAP:"ATCG103","40:f2:01:88:1e:0a",6,-83

OK

# Quit WiFi Access Point
AT+CWQAP

OK
WIFI DISCONNECT
```

# Ressources
* [ESP8266 - AT Command Reference @ Room-15](https://room-15.github.io/blog/2015/03/26/esp8266-at-command-reference/)
* [ESP8266 Resources (with documentation)](https://www.espressif.com/en/products/hardware/esp8266ex/resources)

# Where to buy
* [MOD-WIFI-ESP8266 @ MC Hobby](https://shop.mchobby.be/product.php?id_product=666)
* [MOD-WIFI-ESP8266 @ Olimex](https://www.olimex.com/Products/IoT/ESP8266/MOD-WIFI-ESP8266/open-source-hardware)
