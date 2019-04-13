[Ce fichier existe également en FRANCAIS](TOOLS.md)

# htobin.py (.h --> .bin)
The `htobin.py` script compiles GameDuino header files (.h) containing ressources to binary files (.bin). The .bin files can then be loaded by MicroPython onto the GameDuino board.

The `gd.py` library did deprecate the `copy()` (which copy data from Arduino's Flash Arduino to GameDuino) and replace it by `copybin()` (copy the binary file content to  GameDuino)

## Use case
Many Gamesuino examples are using ressource stored into the Arduino's Flash by using a header file (.h).

With the example (01_basics/sprite256/sprite256.h)[../1_basics/sprite256/sprite256.h] the header file looks to:

```
static flash_uint8_t sprites256_pic[] = {

0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,
0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00, ...
                              ... 0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,
};
```

Transform this content into MicroPython code creates a quite too large python script to be parsed on a microcontroler. As a result, the content could not be transform in byte code. The best would be to have a ressource like for Arduino but not in Flash but into a file (which achieve the same results).

Final solution is to create a binary file which exactly math the bytes encoded in the header file.

So here the HEX content of `sprite256_pal.bin` file matching the `static flash_uint8_t sprites256_pal[] = {` declaration in the (01_basics/sprite256/sprite256.h)[../01_basics/sprite256/sprite256.h] file (_the header file can contains several ressources_)
```
...
0000000 00 00 00 00 00 00 00 00 ef 3d 00 00 c6 18 bd 77 | .........=.....w
0000010 08 21 00 00 ff 7f d6 5a 00 00 ff 7f bd 77 18 63 | .!.....Z.....w.c
0000020 29 25 00 00 ff 7f de 7b 00 00 ff 7f 00 00 00 00 | )%.....{........
0000030 00 00 ff 7f 00 00 00 00 00 00 ff 7f 00 00 00 00 | ................
0000040 42 08 52 4a 00 00 00 00 08 21 00 00 18 63 ff 7f | B.RJ.....!...c..
0000050 de 7b 00 00 ff 7f 18 63 63 0c 73 4e 00 00 ff 7f | .{.....cc.sN....
0000060 00 00 ff 7f ef 3d bd 77 73 4e 00 00 ff 7f 42 08 | .....=.wsN....B.
0000070 42 08 00 00 ff 7f 94 52 18 63 ff 7f 00 00 00 00 | B......R.c......
...
```
__Encoded such a way, the data can be made available in the MicroPython filesystem (so also in Flash!).__

## How htobin.py does works

[00_basic/htobin.py](00_basic/htobin.py) is a python3 script to execute on your computer (we are using Linux or Raspberry-Pi).

It inspect the header file (.h) named in parameters and creates as many `XXXXXXXXXX.bin` binary files as there is `static flash_uint8_t XXXXXXXXXX[] = {` declaration in the header file. Notice that data CANNOT SHARE the same line of the openning or closing statements.

The .bin files are created in the same directory than source header file (.h).

In the case of the (01_basics/sprite256/sprite256.h)[../01_basics/sprite256/sprite256.h] exemple, the `htobin.py` commands will look to

```
$ ./htobin.py ../01_basics/sprite256/sprites256.h
```

which will produce the following output (plus the files):

```
Openning sprites256.h ...
Writing sprites256_pic.bin ...
4096 bytes written
Writing sprites256_chr.bin ...
3808 bytes written
Writing sprites256_pal.bin ...
1904 bytes written
Done!
```

## Reload .bin -> Gameduino

Here is the snip of code used to reload a .bin content (example comming from  [01_basics/sprite256/spr256.py](../01_basics/sprite256/spr256.py) )

```
# Openning the ressource file as read (r) and binary mode (b)
# The 'with' statement would automatically release the file ressource asap
with open( 'sprites256_pic.bin', 'rb' ) as f:
	# Copy the file content to GameDuino starting from address RAM_PIC (0x0000)
	gd.copybin( f, RAM_PIC )
```

# ramtoh.py (Gameduino -> .h)

This MicroPython script allows you to extract the content (the state) of the Gameduino RAM_CHR, RAM_PAL, RAM_PIC under the header file format (.h). The extraction result is displayed directly into the REPL session.

This script may be very interesting to fetch a pre-initialized binary image  (.bin) from the Gameduino's RAM (only the useful sections) which can be reloaded later.

Please, note that `htobin.py` script must still be used after the extract to convert the header format (.h generated with  `ramtoh.py`) to .bin files.
  
