""" Copy/paste mini-keyboard sending CTRL-C et CTRL-V shortcut key to your
    computer. Use an AZERTY keymap for the Keyboard (but should be the same
	for QWERTY keyboard).

	Do not forgot to change the boot.py file to activate USB HID support with
    pyb.usb_mode('VCP+HID', hid=pyb.hid_keyboard)
"""
# CTRL-C : Wire X9 to the ground via a Push-Button
# CTRL-V : Wire X10 to the ground via a Push-Button
from machine import Pin
import pyb
from kmap_frbe import kmap, CTRL
from usbhid import *

hid = pyb.USB_HID()

class Btn():
    """ Button with software debouncing. Count the number of time a button is
        pressed. Have a reject_ms to reject several button within a given
        timelapse. """
    def __init__( self, pin, reject_ms=200 ):
        self.pin = pin
        self.counter = 0
        self.last_millis = 0
        self.reject_ms = 200
        self.state = pin.value()

    def update( self ):
        """ Compute the state of the button. Call it as ofter as possible """
        _current = self.pin.value()
        if _current != self.state:
            sleep_ms( 20 )
            if self.pin.value()!=_current:
                return
            # count on raising edge
            if self.state==False and _current==True:
                if (pyb.millis()-self.last_millis)<self.reject_ms:
                    return
                self.counter += 1
                self.last_millis = pyb.millis()
            self.state = _current

    @property
    def has_pressed( self ):
        """ Check if the button as been pressed somehow """
        if self.counter > 0:
            self.counter = 0 # reset the counter
            return True
        return False

# CTRL-C / Copy will be wired to X9
pin_X9 = Pin("X9", Pin.IN, Pin.PULL_UP)
btn_copy = Btn( pin_X9 )
# CTRL-C / Paste will be wired to X10
pin_X10 = Pin("X10", Pin.IN, Pin.PULL_UP)
btn_paste = Btn( pin_X10 )

while True:
    btn_copy.update()
    if btn_copy.has_pressed:
        sendchr( 'c', hid, kmap, modifiers=[CTRL] )
    btn_paste.update()
    if btn_paste.has_pressed:
        sendchr( 'v', hid, kmap, modifiers=[CTRL] )
