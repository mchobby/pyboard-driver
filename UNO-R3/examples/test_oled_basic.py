# Test the OLED screen present on the PYBOARD-UNO-R3 board
# Use Unoled class to which improve the SSD1306 features.
#
# Unoled class is based on MicroPython SSD1306 driver (see MicroPython GitHub)
from unoextra import Unoled
from time import sleep
lcd = Unoled()

# Absolute position drawing & text
lcd.text("Bonjour", 10,10, 1)
lcd.text("MicroPython !", 10,20, 1)
# Draw a white rectangle - rect( x, y, w, h, c )
lcd.rect( 3, 3, 128-2*3, 64-2*3, 1 )
lcd.show() # must be called
sleep( 2 )

# Scrolling on display
# Print statement will always refresh the screen
lcd.clear()
for i in range(11):
	lcd.println( "Line %s" % i )
	sleep( 0.5 )
sleep(2)

lcd.clear()
lcd.println( "Long text does not wrap!" )
sleep(2)

lcd.clear()
lcd.println( "Long text does may wrap on request!", wrap=True  )
sleep(2)


# Cursor management
lcd.clear()
lcd.println( "Move cursor:")
lcd.set_cursor( (3,5) ) # 4th line, 6th caracter (0 based position)
lcd.println( "+" )
sleep(2)

# Clear some char somewhere in the screen
for i in range(6):
	lcd.println( "************")
lcd.set_cursor( (2,2) ) # 3th line, 3th charater
lcd.print("   ") # Clear with 3 spaces
sleep( 2 )

lcd.clear()
lcd.println("Progressing:")
for i in range(10):
	lcd.print('.')
	sleep(0.3)
lcd.println('')
lcd.println( 'Done!' )
sleep( 2 )

# Nice rotating progress
lcd.clear()
s = "\|/-"
lcd.print('Progress:')
pos = lcd.cursor()
iCount = 0
while iCount < 20:
	lcd.set_cursor( pos )
	lcd.print( s[iCount%len(s)] )
	sleep( 0.250 )
	iCount += 1
lcd.set_cursor( pos )
lcd.println('Done!')

# Drawing lines
lcd.clear()
for i in range( 0, lcd.height, 2 ):
	lcd.line( 0,0, lcd.width, i, 1 )
	lcd.show() # Update the screen

print( "That's all Folks!" )
