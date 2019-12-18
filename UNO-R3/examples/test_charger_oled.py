# PYBOARD-UNO-R3 board : display charger voltages on the OLED screen
#
from unoextra import *
from time import sleep

ch = Charger()
lcd = Unoled()

CHARGING_TEXT = { CHARGING_NOT_CHARGING : "Not ch.",
				  CHARGING_PRE_CHARGE   : "<V BATLOWV",
				  CHARGING_FAST_CHARGE  : "Fast",
				  CHARGING_DONE         : "Done" }

# Activate ADC conversion rate (1 sec) for read battery voltage
ch.config( conv_rate=True )

i = 0
while True:
	lcd.clear(show=False)
	lcd.println( "--- Iter. %s ---" % i, show=False )
	lcd.println( "VBat: %2.2f v" % ch.vbat, show=False )
	lcd.println( "VSYS: %2.2f v" % ch.vsys, show=False )
	lcd.println( "VBus: %2.2f v" % ch.vbus, show=False )
	lcd.println( "Charging: %s" % CHARGING_TEXT[ch.charging_status], show=False )
	#lcd.println( "I In Lim: %1.3f" % ch.input_current_limit )
	lcd.println( "I bat   : %2.3f" % ch.ibat )
	ch.update()
	i+=1
	sleep(1)
