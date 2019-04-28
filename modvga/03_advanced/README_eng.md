[Ce fichier existe également en FRANCAIS](README.md)

* bitmap : draw a moving rectangle. Drawed pixel per pixel.
* snow : use MicroCode son the co-processor to smilutate a snowy screen.

# Bitmap example
Manipulate image pixel per pixel and drawing lines. Use a moving triangle as a sample.

![bitmap.py screen capture](bitmap.jpg)

## Test the script

Start a REPL session then key-in

```
import bitmap
```

# snow example
This example will simulate snow on screen (like disconnected monitor) with
micro-code autonomously executed by the co-processor. So leaving the microcontroler
processor executing its main tasks.

![snow.py screen capture](snow.jpg)

## Test the script

Start the REPL session then key-in this command

```
import snow
```
