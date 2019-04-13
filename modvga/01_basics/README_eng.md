[Ce fichier existe également en FRANCAIS](README.md)

* sprite256 : defines, display and moves 256 sprites on the screen.
* ...

# sprite256 example

The `spr256.py` script sample use the 5 .bin files stored on the `/sd` pyboard's directory.
Those files are compiled with the `htobin.py` tool and avoids the GameDuino header files (.h) to be encoded as a Python script.

 ![results of spr256.py script](sprite256.jpg)

 See also the [YouTube video (YouTube)](https://youtu.be/_6DVzVwcSMQ)

## Create the .bin files
Here is how the .bin files were created on a Linux or Raspbian OS.
```
$ cd modvga/00_basic
$ ./htobin.py ../01_basics/sprite25/sprites256.h
Openning sprites256.h ...
Writing sprites256_pic.bin ...
4096 bytes written
Writing sprites256_chr.bin ...
3808 bytes written
Writing sprites256_pal.bin ...
1904 bytes written
Done!

$ ./htobin.py ../01_basics/sprite256/pickups2.h
Openning pickups2.h ...
Writing pickups2_img.bin ...
13312 bytes written
Writing pickups2_pal.bin ...
512 bytes written
Done!
```

## Test the script

Start a REPL session and key-in the following instruction.

```
import spr256
```
