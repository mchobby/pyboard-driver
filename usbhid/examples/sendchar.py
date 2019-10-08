""" Test the Keymap and usbhid.sendchar()

    Send characters to the USB Host as if it was typed on a Keyboard."""
import pyb
from kmap_frbe import kmap
from usbhid import sendchr

# Do not forgot to change the boot.py file
# pyb.usb_mode('VCP+HID', hid=pyb.hid_keyboard)

hid = pyb.USB_HID()
sendchr( '@', hid, kmap ) # Layout FR-FR / FR-BE sensitive
sendchr( 'A', hid, kmap ) # Layout FR / US sensitive
sendchr( 'T', hid, kmap ) # Same on all layout FR / US
sendchr( 'C', hid, kmap )
sendchr( 'G', hid, kmap )


print( "That''s all folks" )
