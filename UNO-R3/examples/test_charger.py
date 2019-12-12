# Display various stats about the charger on the PYBOARD-UNO-R3 board
#
from unoextra import *
from time import sleep

ch = Charger()

CHARGING_TEXT = { CHARGING_NOT_CHARGING : "Not charging",
				  CHARGING_PRE_CHARGE   : "< V BATLOWV",
				  CHARGING_FAST_CHARGE  : "Fast Charging",
				  CHARGING_DONE         : "Charge Termination Done" }

VBUS_TEXT = { VBUS_NO_INPUT : "No input",
			  VBUS_USB_SDP  : "USB Host SDP",
			  VBUS_USB_CDP  : "USB CDP (1.5A)",
			  VBUS_USB_DCP  : "USB DCP (3.25A)",
			  VBUS_USB_DCP_MAX : "Adjustable High Voltage DCP (MaxCharge) (1.5A)",
			  VBUS_USB_UNKNOW  : "Unknown Adapter (500mA)",
			  VBUS_NOT_STD     : "Non-Standard Adapter (1A/2A/2.1A/2.4A)",
			  VBUS_OTG         : "USB OTG" }

CHARGING_FAULT_TEXT = { CHARGING_FAULT_NORMAL : "Normal",
		CHARGING_FAULT_INPUT  : "Input fault. VBUS > V ACOV or VBAT < VBUS < V VBUSMIN (typical 3.8V)",
		CHARGING_FAULT_THERMAL: "Thermal shutdown",
		CHARGING_FAULT_TIMER  : "Charge Safety Timer Expiration" }

NTC_FAULT_TEXT = { NTC_FAULT_NORMAL    : "Normal",
				   NTC_FAULT_BUCK_COLD : "TS Cold in Buck mode",
				   NTC_FAULT_BUCK_HOT  : "TS Hot in Buck mode",
				   NTC_FAULT_BOOST_COLD: "TS Cold in Boost mode",
				   NTC_FAULT_BOOST_HOT : "TS Hot in Boost mode" }

# Activate ADC conversion rate (1 sec)
ch.config( conv_rate=True )

while True:
	# Display last know status
	print( "-"*40 )
	print( "USB Input Status      : %s" % ("USB500" if ch.usb_input_status == USB500 else "USB100") )
	print( "VSYS regulation status: %s" % ("BAT < VSYSMIN" if ch.vsys_regulation else "BAT > VSYSMIN") )
	print( "Power Good            : %s" % ch.power_good )
	print( "CHARGING              : %s" % CHARGING_TEXT[ch.charging_status] )
	print( "VBUS Status           : %s" % VBUS_TEXT[ch.vbus_status] )
	print( "Watchdog fault        : %s" % ("Watchdog timer expiration" if ch.watchdog_fault else "Normal") )
	print( "Boost fault           : %s" % ("VBUS overloaded in OTG, or VBUS OVP, or battery is too low in boost mode" if ch.boost_fault else "Normal") )
	print( "Charging fault        : %s" % CHARGING_FAULT_TEXT[ch.charging_fault] )
	print( "Battery Fault         : %s" % ("BATOVP (VBAT > V BATOVP)" if ch.battery_fault else "Normal") )
	print( "NTC Fault             : %s" % NTC_FAULT_TEXT[ch.ntc_fault] )
	print( "Battery Voltage       : %s" % ch.vbat )
	print( "SYS Voltage           : %s" % ch.vsys )
	print( "BUS Voltage           : %s" % ch.vbus )

	sleep(1)
	# Request status update
	ch.update_status()
	# Request Fault update
	ch.update_fault()
