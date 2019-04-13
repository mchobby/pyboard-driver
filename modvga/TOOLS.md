[This file also exists in ENGLISH](TOOLS_eng.md)

# htobin.py (.h --> .bin)
le script `htobin.py` permet de compiler une fichier header de GameDuino (.h) contenant généralement des ressources vers un fichier binaire (.bin) que MicroPython pourra charger directement sur GameDuino.

La bibliothèque `gd.py` déprécie dont la fonction `copy()` (copie de Flash Arduino vers GameDuino) au profit de `copybin()` (copie d'un fichier binaire vers GameDuino)

## Cas pratique
De nombreux exemples utilise des ressources statiques stockées en Flash à l'aide d'un fichier header.

Voici l'exemple (01_basics/sprite256/sprite256.h)[01_basics/sprite256/sprite256.h]

```
static flash_uint8_t sprites256_pic[] = {

0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,
0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00, ...
                              ... 0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,
};
```

Transformer ce contenu en code MicroPython crée une script beaucoup trop grand pour un microcontrôleur. Celui-ci ne pourra pas être parsé et transformé en byte code.

La solution réside donc à créer un fichier binaire contenant exactement les octets encodés dans le fichier header.

Voici le contenu de `sprite256_pal.bin` correspondant à la déclaration de `static flash_uint8_t sprites256_pal[] = {` dans le fichier (01_basics/sprite256/sprite256.h)[01_basics/sprite256/sprite256.h] (_Hé oui, il peut y avoir plusieurs déclarations_)
```
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
__Ainsi encodées, les données seront disponibles dans le système de fichier MicroPython (donc en Flash!).__

## fonctionnement de htobin.py

[00_basic/htobin.py](00_basic/htobin.py) est un fichier python3 à exécuter sur PC.

Il inspecte un fichier header (.h) passé en paramètre et crée les différents fichiers binaires `XXXXXXXXXX.bin` correspondants aux déclarations `static flash_uint8_t XXXXXXXXXX[] = {` dans le fichier header. A noter que les données ne peuvent pas se trouver sur la même ligne que les instructions d'ouverture ou fermeture.

Les fichiers .bin sont créés au même emplacement que le fichier d'entête (.h).

Dans le cas de l'exemple (01_basics/sprite256/sprite256.h)[01_basics/sprite256/sprite256.h], la commande

```
$ ./htobin.py ../01_basics/sprite256/sprites256.h
```

Produit le résultat suivant:

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

## Recharger .bin -> Gameduino

Voici du code issu de l'exemple [01_basics/sprite256/spr256.py](../01_basics/sprite256/spr256.py)

```
# Ouverture du fichier en lecture (r) et mode binaire (b)
# L'instruction 'with' libérera automatiquement le ressource
with open( 'sprites256_pic.bin', 'rb' ) as f:
	# Copier le continu du fichier en commencant à l'adresse RAM_PIC (0x0000)
	gd.copybin( f, RAM_PIC )
```
