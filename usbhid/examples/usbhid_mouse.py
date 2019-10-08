import pyb
from time import sleep_ms

# Activer le mode VCP+HID dans boot.py

switch = pyb.Switch()
accel = pyb.Accel()
hid = pyb.USB_HID()

while not switch():
    hid.send( (0, accel.x(), accel.y(), 0) )
    sleep_ms(20)

