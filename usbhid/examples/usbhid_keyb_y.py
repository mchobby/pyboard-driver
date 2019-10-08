import pyb
from time import sleep_ms

# Ne pas oublier de modifier boot.py
# pyb.usb_mode('VCP+HID', hid=pyb.hid_keyboard) 

hid = pyb.USB_HID()
report = bytearray( 8 )

# Envoyer un Key-press pour Y
report[0] = 0x02 # Shift gauche
report[2] = 0x1C # touche Y
hid.send( report )
sleep_ms( 10 )

# Envoyer le release 
report[0] = 0x00
report[2] = 0x00
hid.send( report )
