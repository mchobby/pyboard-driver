"""
zumobuzzer.py - easy library Pololu's Zumo Robot Buzzer for MicroPython Pyboard Original.

* Author(s):    Braccio M.  from MCHobby (shop.mchobby.be).
                Meurisse D. from MCHobby (shop.mchobby.be).

See project source @ https://github.com/mchobby/pyboard-driver/tree/master/zumo-robot

23 jul 2021 - domeu - code cleaning
"""
#
# The MIT License (MIT)
#
# Copyright (c) 2019 Meurisse D. for MC Hobby
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

__version__ = "0.0.2"
__repo__ = "https://github.com/mchobby/pyboard-driver.git"

from pyb import Timer
from machine import Pin
import time
"""x est l'octave des notes """
def NOTE_C(x):
    return( 0 + x*12)
def NOTE_C_SHARP(x):
    return( 1 + x*12)
def NOTE_D_FLAT(x):
    return( 1 + x*12)
def NOTE_D(x):
    return( 2 + x*12)
def NOTE_D_SHARP(x):
    return( 3 + x*12)
def NOTE_E_FLAT(x):
    return( 3 + x*12)
def NOTE_E(x):
    return( 4 + x*12)
def NOTE_F(x):
    return( 5 + x*12)
def NOTE_F_SHARP(x):
    return( 6 + x*12)
def NOTE_G_FLAT(x):
    return( 6 + x*12)
def NOTE_G(x):
    return( 7 + x*12)
def NOTE_G_SHARP(x):
    return( 8 + x*12)
def NOTE_A_FLAT(x):
    return( 8 + x*12)
def NOTE_A(x):
    return( 9 + x*12)
def NOTE_A_SHARP(x):
    return(10 + x*12)
def NOTE_B_FLAT(x):
    return(10 + x*12)
def NOTE_B(x):
    return(11 + x*12)
PLAY_CHECK = 1
PLAY_AUTOMATIC = 0
SILENT_NOTE   = 0xFF


DIV_BY_10 = (1<<15)



class PololuBuzzer(object):
    def __init__(self):
        self.buzzer=Pin("X1",Pin.OUT)
        self.tim_buzzer=Timer(2,freq=500)
        self.ch_buzzer=self.tim_buzzer.channel(1,Timer.PWM,pin=self.buzzer)
        self.buzzerInitialized = 0
        self.buzzerFinished = 1
        self.buzzerSequence=0
        self.buzzerTimeout = 0
        self.play_mode_settings = PLAY_AUTOMATIC

        self.octave = 4
        self.whole_note_duration = 2000
        self.note_type = 4
        self.duration = 500
        self.volume = 15
        self.staccato = 0
        self.all_notes = False           #False au debut. N'agit que sur une note

    def playFrequency(self,freq,dur,volume):
        self.freq=freq
        self.dur=dur
        self.volume = volume
        self.buzzerFinished = 0
        multiplier = 1
        if (self.freq & DIV_BY_10):      #si le bit de résolution est activé on doit diviser par 10
            multiplier = 10
            self.freq = (self.freq and ~DIV_BY_10)
        min = 40* multiplier    #(40*1 minimum)

        if (self.freq < min):
            self.freq = min
        if ((multiplier == 1) and (self.freq > 10000)):
            self.freq = 10000

        if (multiplier == 10):
            self.freq = int((self.freq + 5) /10)
        if (self.freq == 1000):
            timeout=self.dur
        else:
            timeout=int((self.dur*self.freq /1000))

        if (self.volume > 15):
            self.volume = 15


        if freq == 0:
            self.tim_buzzer.freq( self.freq )
            self.ch_buzzer.pulse_width_percent( 0 )
        else:

            self.tim_buzzer.freq( self.freq )
            self.ch_buzzer.pulse_width_percent( 30 )
            time.sleep_us(self.dur*1000)   #sert a arreter le son apres le temps demandé
            self.ch_buzzer.pulse_width_percent(0)

    def playNote(self,note,dur,volume):
        self.freq = 0
        self.dur=dur
        self.note = note
        self.volume = volume
        offset_note = self.note -16

        if ((note==SILENT_NOTE)):
            freq = 1000
            self.playFrequency(0,self.dur,0)
            time.sleep_us(self.dur*1000)
            return

        if (self.note <= 16):
            offset_note = 0
        elif(offset_note > 95):
            offset_note = 95

        exponent = offset_note // 12  # // division entière
        tab_sound = {0:412,1:437,2:463,3:490,4:519,5:550,6:583,7:617,8:654,9:693,10:734,11:778}
        self.freq = tab_sound[offset_note - (exponent *12)]

        if (exponent < 7 ):
            self.freq = (self.freq << exponent)
            if (exponent > 1):
                self.freq = int((self.freq + 5) //10)
            else:
                self.freq += DIV_BY_10
        else:
            self.freq = int((self.freq * 64 +2)//5)
        if (volume > 15):
            volume = 15

        if (self.freq>0):
            self.playFrequency(self.freq,self.dur,self.volume)
        else:
            self.playFrequency(0,0,0)





    def isPlaying(self):
        return(self.buzzerFinished==False or self.buzzerSequence != 0 )

    def play(self,notes):
        self.buzzerSequence = 0   #on est au premier caractère de la sequence
        self._notes=notes         #on retiens la séquence
        self.staccato_rest_duration = 0
        self.octave = 4

        note=self.nextNote()   #note pour vérifier qu'il y a un charactère
        while(note):
            note=self.nextNote()

        self.reset()
        self.off()

    def reset(self):
        self.octave = 4
        self.whole_note_duration = 2000
        self.note_type=4
        self.duration = 500
        self.volume = 15
        self.staccato = 0
        self.octave=4
        tmp_duration=self.duration

    def stopPlaying(self):
        self.buzzerFinished = 1
        self.buzzerSequence = 0

    def off(self):
        self.ch_buzzer.pulse_width_percent( 0 )

    def currentCharacter(self):
        c=None
        if  (self.buzzerSequence >= len(self._notes)) :
            return None

        c = self._notes[self.buzzerSequence]
        if (c and c.isdigit() and self.buzzerSequence == 0):
            pass
            # exeption(" First character has to be a letter")
        c= c.lower()

        while(c==" "):
            self.buzzerSequence+=1
            if  (self.buzzerSequence >= len(self._notes)) :        #verifie si il y a un autre  carac
                return None
            c = self._notes[self.buzzerSequence]
            c=c.lower()
        return(c)

    def getNumber(self):
        arg = 0
        c=self.currentCharacter()
        while(c and c.isdigit()):
            arg *=10
            arg += int(c)
            self.buzzerSequence+=1
            c=self.currentCharacter()
        return (arg)


    def nextNote(self):
        self.note=0
        self.rest=0
        tmp_octave = 0
        while(True):
            # Sert a jouer une note silencieuse si il faut
            if(self.staccato==True and self.staccato_rest_duration>0):
                self.playNote(SILENT_NOTE,self.staccato_rest_duration,5)
                self.staccato_rest_duration=0

            c = self.currentCharacter()
            self.buzzerSequence+=1
            if (c== '>'): # play note 1 octave higher
                self.all_notes = False
                tmp_octave = tmp_octave +1
                continue

            elif(c== '<'):
                self.all_notes = False
                tmp_octave = tmp_octave -1
                continue
            elif (c== 'a'): # La
                self.note = NOTE_A(0)
                break
            elif (c== 'b'): # Si
                self.note = NOTE_B(0)
                break
            elif (c== 'c'): # Do
                self.note = NOTE_C(0)
                break
            elif (c== 'd'): # Re
                self.note = NOTE_D(0)
                break
            elif (c== 'e'): # Mi
                self.note = NOTE_E(0)
                break
            elif (c== 'f'): # Fa
                self.note = NOTE_F(0)
                break
            elif (c== 'g'): # Sol
                self.note = NOTE_G(0)
                break
            elif (c== 'l'):
                self.note_type =self.getNumber()
                self.duration=self.whole_note_duration/self.note_type
                c = self.currentCharacter()         #on prend le premier caractère
                self.buzzerSequence +=1
            elif (c== 'm'):
                if(self.currentCharacter() == 'l'):
                    self.staccato = False
                elif (self.currentCharacter()=='s'):
                    self.staccato=True
                    self.staccato_rest_duration=0
                else:
                    pass
                self.buzzerSequence+=1
                continue
            elif (c== 'o'): # Change octave
                self.all_notes = True
                self.octave = self.getNumber()
                continue
            elif (c== 'r'): # Pause note
                self.rest = 1
            elif (c== 't'): # Tempo Change
                self.whole_note_duration=60*400/self.getNumber()*10
                self.duration=self.whole_note_duration/self.note_type
                continue
            elif (c== 'v'): # Volume setting
                self.volume = self.getNumber()
                continue
            elif (c== '!'): # Reset all parameters
                self.octave = 4
                self.whole_note_duration = 2000
                self.note_type=4
                self.duration = 500
                self.volume = 15
                self.staccato = 0
                self.octave=4
                tmp_duration=self.duration
                continue
            else:
                self.buzzerSequence = 0
                break
            break
        #FIN WHILE

        if(self.all_notes == False):
            self.note+= (self.octave + tmp_octave) *12
            self.all_note = True
        else:
            self.note += self.octave*12 # note = key + octave *12

        c=self.currentCharacter()
        # + or # after a note raises any note one half-step
        while(c=='+' or c=='#'):
                self.buzzerSequence+=1
                self.note+=1
                c=self.currentCharacter()
        # - after a note lowers any note one half-step
        while(c=='-'):
                self.buzzerSequence+=1
                self.note-=1
                c=self.currentCharacter()

        tmp_duration=self.duration
        if(c and c.isdigit()):
                tmp_duration=int(self.whole_note_duration/self.getNumber())

        dot_add=tmp_duration/2
        while(self.currentCharacter() =='.'):
                self.buzzerSequence+=1
                tmp_duration+=dot_add
                dot_add=int(dot_add/2)
                break

        if(self.staccato==True):
                self.staccato_rest_duration = int(tmp_duration/2)
                tmp_duration = int(tmp_duration - self.staccato_rest_duration)
        self.playNote(SILENT_NOTE if (self.rest>0) else (self.note),int(tmp_duration),self.volume)

        return (self.buzzerSequence< len(self._notes))


    def playMode(self,mode):
        self.play_mode_settings=mode
        if(mode == PLAY_AUTOMATIC):
            self.playCheck()

    def playCheck(self):
        self.nextNote()
        return (self.buzzerSequence != 0)
