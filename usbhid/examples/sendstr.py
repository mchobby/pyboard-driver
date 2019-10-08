""" Test the Keymap and usbhid.sendstr()

    Send a complete string as if it was typed on the Keyboard."""
import pyb
from kmap_frbe import kmap
from usbhid import sendstr

# Do not forgot to change the boot.py file
# pyb.usb_mode('VCP+HID', hid=pyb.hid_keyboard)

hid = pyb.USB_HID()
sendstr( 'MicroPython is too awesome!', hid, kmap )

print( "That''s all folks" )
