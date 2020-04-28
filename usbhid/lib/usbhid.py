""" Basic tools to send HID reports to the USB host.
    Mainly concerns keyboard HID device"""

__version__ = '0.0.1'

from time import sleep_ms

hidkey_buffer = bytearray(8)

def sendchr(char, hid, kmap, modifiers=None):
	""" Send a character by typing it on a KEYBOARD hid device.
	    Send the char X on hid instance by using the keyboard layout map.

		Modifiers is a list with additionnal PLAIN, SHIFT, CTRL, ALT_GR... modifier bits """
	if not char in kmap.keys() :
		raise Exception( "Char %s not registered in kmap" )
	global hidkey_buffer
	# key down
	hidkey_buffer[2], hidkey_buffer[0] = kmap[char]
	if modifiers:
		for modifier in modifiers:
			if (hidkey_buffer[0] & modifier) != modifier: # If modifier not yet applied
				hidkey_buffer[0] = hidkey_buffer[0] | modifier
	hid.send(hidkey_buffer)
	sleep_ms(10)
	# key up
	hidkey_buffer[2], hidkey_buffer[0] = 0x00, 0x00
	hid.send(hidkey_buffer)
	sleep_ms(10)

def sendstr(s, hid, kmap):
	""" Send the string by typing it on a KEYBOARD hid device.
	    Send the string on hid instance by using the keyboard layout map """
	for c in s:
		sendchr( c, hid, kmap )
