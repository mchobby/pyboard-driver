# boot.py -- run on boot-up
# can run arbitrary Python, but best to keep it minimal

import machine
import pyb
#pyb.main('main.py') # main script to run after this one

# act as a serial device and a keyboard
pyb.usb_mode('VCP+HID', hid=pyb.hid_keyboard) 

# Act as a serial device and a mouse
#pyb.usb_mode('VCP+HID', hid=pyb.hid_mouse) 
