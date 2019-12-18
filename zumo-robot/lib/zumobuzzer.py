"""
zumobuzzer.py - easy library Pololu's Zumo Robot Buzzer for MicroPython Pyboard Original.

* Author(s):    Braccio M.  from MCHobby (shop.mchobby.be).
                Meurisse D. from MCHobby (shop.mchobby.be).

See project source @ https://github.com/mchobby/pyboard-driver/tree/master/zumo-robot

See example line_follower.py in the project source
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

__version__ = "0.0.1"
__repo__ = "https://github.com/mchobby/pyboard-driver.git"

from pyb import Timer, Pin
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
        print("Init PololuBuzzer")




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
            print("play note silence:  %s" %self.freq)
        #if((note == SILENT_NOTE) or (volume ==0)):
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

        #print("Offset: %s - Exponent: %s - Freq/tableau: %s" %(offset_note, exponent,self.freq))
        if (exponent < 7 ):
            self.freq = (self.freq << exponent)
            #print("freq apres exp: %s" %self.freq)
            if (exponent > 1):
                self.freq = int((self.freq + 5) //10)
                #print("Freq - exponent>1 : %s " %self.freq)
            else:
                self.freq += DIV_BY_10
                #print("Freq - DIV_BY_10: %s" %self.freq)
        else:
            self.freq = int((self.freq * 64 +2)//5)
            #print("Freq - else: %s" %self.freq)
        if (volume > 15):
            volume = 15



        if (self.freq>0):
            print("freq > 0")
            self.playFrequency(self.freq,self.dur,self.volume)
        else:
            print("freq pas plus grand que zero")
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


    """def playFromProgramSpace(self,notes_p):
        self.buzzerSequence = notes_p
        self.use_program_space = 1
        self.staccato_rest_duration = 0
        print("playFromProgramSpace")
        self.nextNote()"""


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
        print("stopPlaying")

    def off(self):
        self.ch_buzzer.pulse_width_percent( 0 )




    def currentCharacter(self):

        c=None

        if  (self.buzzerSequence >= len(self._notes)) :     #Si le compteur buzzerSequence et plus grand que la longeur de caractères
            return None                                     #c=None

        c = self._notes[self.buzzerSequence] #On prend le premier caractère [buzzerSequence == 0] initialement,
        if (c and c.isdigit() and self.buzzerSequence == 0):
            pass
            # exeption(" First character has to be a letter")
            # Ecrire erreur quand 1er pas une lettre
                                                      # doit etre incrémenté pour pouvoir utiliser le nieme caractère
        c= c.lower()                            # C toujours en minuscule

        while(c==" "):                          #on recherche si il y a un espace "silence" et qu'il y ai un autre caractère apres
            self.buzzerSequence+=1
            if  (self.buzzerSequence >= len(self._notes)) :        #verifie si il y a un autre  carac
                return None
            c = self._notes[self.buzzerSequence]
            c=c.lower()
        return(c)

    def getNumber(self):                #Fonction qui permet d'avoir un nombre a plusieurs chiffres
        arg = 0
        c=self.currentCharacter()       #Prends le caractère
        while(c and c.isdigit()):       #si il y a un caractère et que le caractère est un chiffre
            arg *=10                    #première fois (0*10), deuxieme fois (c*10), troisième fois ((c*10)*10)
            arg += int(c)               #change une chaine de caractères en integer et ajoute ,
            print(arg)                  #remets le chiffre en integer pour etre utilise dans des calculs
                                        # on soustrait les nombres et on les remets en chaine de caractères
            self.buzzerSequence+=1      #aug buzzerSequence pour le prochain caractère
            c=self.currentCharacter()   #on recherche un caractère. Si ce n'est plus un chiffre ou qu'il n'y a plus rien on sort de la boucle while
        return (arg)                    #retourne le nombre complet


    def nextNote(self):
        self.note=0                      #note vaut 0 au debut
        self.rest=0
        tmp_octave = 0                      #le rest vaut 0 au debut
        while(True):
                   #octave vaut 4
            #Sert a jouer une note silencieuse si il faut
            if(self.staccato==True and self.staccato_rest_duration>0):   #si on utilise le mode staccato on place un note de silence entre chaque note
                print("Staccato True: %s"  %self.freq)
                self.playNote(SILENT_NOTE,self.staccato_rest_duration,5) #(note,dur,volume)
                self.staccato_rest_duration=0                           #On remets le variable a 0 pour produire du son prochaine fois

            c = self.currentCharacter()         #on prend le premier caractère, en fonction de ce que c'est on peut faire plusieurs choses
            self.buzzerSequence+=1
            """> plays the next note one octave higher"""
            if (c== '>'):
                self.all_notes = False  #on agit que sur une note

                tmp_octave = tmp_octave +1      #on aug

                continue   # on revient au début su while pour voir

            elif(c== '<'):
                self.all_notes = False
                tmp_octave = tmp_octave -1

                continue
            elif (c== 'a'):
                self.note = NOTE_A(0)
                print("----------------------")
                print("Lettre: a - Note: La.")
                break
            elif (c== 'b'):
                self.note = NOTE_B(0)
                print("----------------------")
                print("Lettre b - Note: Si.")
                break
            elif (c== 'c'):
                self.note = NOTE_C(0)
                print("----------------------")
                print("Lettre c - Note: Do.")
                break
            elif (c== 'd'):
                self.note = NOTE_D(0)
                print("----------------------")
                print("Lettre d - Note: Re.")
                break
            elif (c== 'e'):
                self.note = NOTE_E(0)
                print("----------------------")
                print("Lettre e - Note: Mi.")
                break
            elif (c== 'f'):
                self.note = NOTE_F(0)
                print("----------------------")
                print("Lettre f - Note: Fa.")
                break
            elif (c== 'g'):
                self.note = NOTE_G(0)
                print("----------------------")
                print("Lettre g - Note: Sol.")
                break

            #L' followed by a number sets the default note duration to
            #the type specified by the number: 4 for quarter notes, 8
            #for eighth notes, 16 for sixteenth notes, etc.
            #(default: L4)"""
            elif (c== 'l'):                             #
                self.note_type =self.getNumber()
                self.duration=self.whole_note_duration/self.note_type
                c = self.currentCharacter()         #on prend le premier caractère
                self.buzzerSequence +=1
                print("Note duration changed to: %s." %self.note_type)
            #"""ML' sets all subsequent notes to play legato - each note is played
            #for its full length.  This is the default setting.

            #MS' sets all subsequent notes to play staccato - each note is played
            #for 1/2 of its allotted time, followed by an equal period
            #of silence."""
            elif (c== 'm'):
                if(self.currentCharacter() == 'l'):
                    self.staccato = False
                    print("Staccato mode OFF")
                elif (self.currentCharacter()=='s'):
                    self.staccato=True
                    self.staccato_rest_duration=0
                    print("Staccato mode ON.")
                else:
                    pass
                self.buzzerSequence+=1
                continue
            #"""O' followed by a number sets the octave (default: O4)."""
            elif (c== 'o'):
                self.all_notes = True
                self.octave = self.getNumber()
                print("Octave set to: %s." %self.octave)
                continue

            elif (c== 'r'):
                self.rest = 1
                print("----------------------")
                print("Pause Note")

            #"""T' followed by a number sets the tempo (default: T120)."""
            elif (c== 't'):
                self.whole_note_duration=60*400/self.getNumber()*10
                self.duration=self.whole_note_duration/self.note_type
                print("Tempo changed to: %s." %self.duration)
                continue
            #"""V' followed by a number from 0-15 sets the music volume.
            #(default: V15)"""
            elif (c== 'v'):
                self.volume = self.getNumber()
                continue
            #"""'!' resets all persistent settings to their defaults."""
            elif (c== '!'):
                self.octave = 4
                self.whole_note_duration = 2000
                self.note_type=4
                self.duration = 500
                self.volume = 15
                self.staccato = 0
                self.octave=4
                tmp_duration=self.duration
                print("Reset everything.")
                continue

                #c = self.currentCharacter()         #on prend le premier caractère
                #self.buzzerSequence +=1
            else:                                   #Si plus rien on remets buzzerSequence a 0 pour etre pret pour une nouvelle chaine de caractères
                self.buzzerSequence = 0
                break
            break
        #FIN WHILE
        if(self.all_notes == False):

            self.note+= (self.octave + tmp_octave) *12
            self.all_note = True
        else:
            self.note += self.octave*12    # note = key + octave *12     (0<=key<12)  octave 4 initiallement


        print("apres self.note: %s" %self.octave)
        c=self.currentCharacter()
        #"""+' or '#' after a note raises any note one half-step"""
        while(c=='+' or c=='#'):
                self.buzzerSequence+=1
                self.note+=1
                c=self.currentCharacter()
        #"""-' after a note lowers any note one half-step"""
        while(c=='-'):
                self.buzzerSequence+=1
                self.note-=1

                c=self.currentCharacter()

        tmp_duration=self.duration                  #si rien de spécial tmp_duration ==500
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
        print(tmp_duration)
        self.playNote(SILENT_NOTE if (self.rest>0) else (self.note),int(tmp_duration),self.volume)

        return(self.buzzerSequence< len(self._notes))



    def playMode(self,mode):
        self.play_mode_settings=mode

        if(mode == PLAY_AUTOMATIC):
            self.playCheck()

    def playCheck(self):
        self.nextNote()
        return (self.buzzerSequence != 0)
b = PololuBuzzer()
