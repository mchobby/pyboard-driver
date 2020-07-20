[This file also exists in french here](README.md)

# UEXT connector on Pyboard

Here is a proposal of wiring (and pinout) of UEXT connector on the Pyboard.

![UEXT Pyboard Prototyping](UEXT-Breakout-LowRes.jpg)

Sur way, it is easier to test and prototypes with boards and sensors exposing UEXT connection. 
- See [UEXT product lines](https://shop.mchobby.be/fr/138-uext) at MCHobby
- See [UEXT product lines](https://www.olimex.com/Products/Modules/) at Olimex.

Finally, I did a prototyping board to ease the connection whith my Pyboard while working with the [module MOD-VGA (3.3V Gameduino board) exposing an UEXT interface](https://shop.mchobby.be/fr/uext/1431-mod-vga-carte-type-gameduino-en-33v-3232100014312-olimex.html).. 

# Pinout 

Here is the proposed pinout between the PyBoard and UEXT:

![UEXT Pyboard PinOut](UEXT-Pyboard-v0.2.jpg)

## Why this wiring?
This wiring proposal comes from the wider UPPY project which will cover more interfaces (this pinout have selected with care ;-) ).

It allows: 
* To keeps the DAC pins
* To keep a second I2C bus for other interfaces.
* To keep as much as PWM pins as possible.
* To keep the Garde les entrées analogiques blindées à disposition.
* To keep one CAN bus. 
* Optinally, the UEXT's UART can be transformed into a second I2C bus (`i2c_2 = I2C(1)` as they share the same lines).

# SPI, I2C, UART buses

Here are the python code to create instance of the various buses available on the UEXT connector.
```
# Create the I2C bus 
from machine import I2C
i2c = I2C( 2 ) # SDA=Y10, SCL=Y9

# Create the SPI bus 
from machine import SPI
spi = SPI(2) # MOSI=Y8, MISO=Y7, SCK=Y6, SS=Y5

# Create the UART bus 
from pyb import UART
ser = UART( 1, 9600 ) # RX=X10, TX=X9, 9600 baud
```

# Where to find MicroPython drivers for UEXT boards

All our MicroPython drivers are stored on [pyboard-driver](https://github.com/mchobby/pyboard-driver) github or [esp8266-upy](https://github.com/mchobby/esp8266-upy) github. MicroPython drivers running on ESP8266 will also work with Pyboard :-) 

The MicroPython drivers for boards exposing UEXT connector are stored under foldername starting with "__mod__" (eg: modvga, modrgb, modwii, etc).

# Ressources
* [Model UEXT.png for schematic](uext-conn.png)

# Where to buy
* [Pyboard prototyping board](https://shop.mchobby.be/fr/micropython/598-plaque-de-prototypage-pour-pyboard-3232100005983.html)
* [UEXT male connector](https://shop.mchobby.be/fr/uext/1524-connecteur-idc-case-header-2x5-254mm-3232100015425.html) qui est un connecteur IDC 2x5 broches
* Extension UEXT: [UEXT product line @ MCHobby](https://shop.mchobby.be/fr/138-uext) and [wide UEXT product line @ Olimex](https://www.olimex.com/Products/Modules/).
* [Pyboard Micropython board](https://shop.mchobby.be/fr/56-micropython)

