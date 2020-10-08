[Ce fichier existe également en FRANCAIS ici](readme.md)

# Using a SIMCom GSM module with MicroPython

This library was written against the [NADHAT GSM board](https://shop.mchobby.be/fr/pi-hats/1656-nadhat-gsm-gprs-connecteur-sim800c-v1-3232100016569-garatronic.html) from Garatronic.

This board is fitted with a SIM800 module from SIMCOM.

![NADHAT GSM board with SIM800 module](docs/_static/nadhat-gsm.jpg)

## Consumption

Some GSM operations does imply impressive current peak (EG: register the module on the mobile network). Les efficient PSU may temporarily under 5V which would cause the SIM module to reboot (even by using distinct power supply for the GSM board).

![LOW ESR Capacitor](docs/_static/low-esr-cap.jpg)

We do recommend to place a 2200µF LOW ESR capacitor directly on the GPIO (over the +5V & GND, as shown on the schematic here below).

The Low ESR capacitor do have a very low ESR (internal resistance) and so, they can discharge very quickly... great to balance current peak on the NadHat board. The counterpart of this feature is the initial powering of the board will also draw a current peak to load up the capacitor (but that is not too embarassing).

__Here is a list of the various modes and corresponding consumption__:

| Mode    | Consumption | Notes        |
|---------|--------------|--------------|
| Power down | 60µA ||
| Sleep mode | 1mA  | Sleep with DTR @ HIGH, Wake with DTR @ LOW. Serial connection lost in Sleep mode. |
| Stand by mode | 18 mA ||
| Appels / SMS | | depends on the Network Band used ([GSM Band](https://en.wikipedia.org/wiki/GSM_frequency_bands))|
|| 200 mA | GSM-850
|| 220 mA | E-GSM-900 (Extended GSM-900 band)
|| 145 mA | DCS-1800  (Digital Cellular System)
|| 130 mA | PCS-1900 (Personal Communication Service)
|Data / GPRS | 450 mA ||
| Burst | 2 A | Current peak occuring during mobile network communication |

## Status LEDs
The SIMCOM modules are usually fitted on board with Status LEDs. Such LEDs are useful to identify the connection state on the mobile network.

* Blink once every 1s: Not connected to mobile network
* Blink once every 2s: __Connected!__ GPRS data session.
* Blink once every 3s: __Connected!__ Call/SMS services availables

# Wiring

## Nadhat GSM to PyBoard

![NadHat GSM to Pyboard](docs/_static/nadhat-gsm-to-pyboard.jpg)

## Nadhat GSM to PYBStick

![NadHat GSM to PYBStick](docs/_static/nadhat-gsm-to-pybstick.jpg)

# Test
All examples are written against the MicroPython Pyboard.

To make the script runnng with the PYBStick, some adhistement must be made in the script (changing the used Pin Names)

| With Pyboard | With PYBStick  | Notes   |
|--------------| ---------------|---------|
| uart = UART(1)  | uart = UART(1)  | __Pyboard:__ X9, X10. __PYBStick:__ S22, S24
| pwr = Pin('Y3') | pwr = Pin('S18')  | Power On Pin

__Mobile phone into the test scripts:__

Many test script do use mobile phone number. Such number are partially mask with "xxx". You will need to write down valids GSM/Mobile number!

## Test Raw (test_raw.py)
The [`test_raw.py`](examples/test_raw.py) does activate le GSM module, sends AT commands and read their response.

This example can be executed from the REPL sesion by typing `import test_raw`

``` python
PYB: sync filesystems
PYB: soft reboot
MicroPython v1.10 on 2019-01-25; PYBv1.1 with STM32F405RG
Type "help()" for more information.
>>> import test_raw
POWER UP
Training auto-baud detect
--> AT+CGMI
<-- b'AT+CGMI\r\r\n'
<-- b'SIMCOM_Ltd\r\n'
<-- b'\r\n'
<-- b'OK\r\n'
OK received :-)
--> AT+CGMM
<-- b'AT+CGMM\r\r\n'
<-- b'SIMCOM_SIM800C\r\n'
<-- b'\r\n'
<-- b'OK\r\n'
OK received :-)
--> AT+CPIN=1427
<-- b'AT+CPIN=1427\r\r\n'
<-- b'ERROR\r\n'
--> AT+CNET
<-- b'AT+CNET\r\r\n'
<-- b'ERROR\r\n'
```

This REPL example is quite interesting to test additionnal AT commands directly from the REPL session.

After the test execution, the `test_raw` namespace is still available which means that you can call the various `test_raw` functions from REPL

```
>>> test_raw.send_then_read( 'AT+CPIN=?' )
--> AT+CPIN=?
<-- b'AT+CPIN=?\r\r\n'
<-- b'OK\r\n'
OK received :-)
```

## Library test (test_lib.py)

The [`test_lib.py`](examples/test_lib.py) script do operate the [smodem](lib/smodem.py) library foundation.

The library do configure the SIMCom module and handle PIN code introduction to unlock module.

As it run with DEBUG mode activated, all the messages exchange over the UART are visible in the REPL session.

__Before running the script__, think to update the value of __PIN_CODE__ constant in the script to reflect the PinCode attached to your own SIM card.

```
from machine import UART, Pin
from smodem import SimModem
import time

PIN_CODE = '1234'   # <<<<< MODIFIER ICI !
```

Once the execution ends, the user gets hand over the REPL session (10 seconds to ends execution). Now you can enter your own AT commands.

``` python
MicroPython v1.10 on 2019-01-25; PYBv1.1 with STM32F405RG
Type "help()" for more information.
>>>
>>> import test_lib
 -->>: AT
 <<--: b'AT\r\r\n'
 <<--: b'OK\r\n'
debug: Modem already running
debug: Configure modem
 -->>: ATZ
 <<--: b'ATZ\r\r\n'
 <<--: b'OK\r\n'
 -->>: ATE0
 <<--: b'ATE0\r\r\n'
 <<--: b'OK\r\n'
 -->>: AT+CPIN=1234
 <<--: None
 <<--: None
 <<--: None
 <<--: b'\r\n'
 <<--: b'OK\r\n'
debug: Modem configured
Modem initialized!
 <<--: None
...
 <<--: None
 <<--: b'+CPIN: READY\r\n'
 <<--: None
...
 <<--: None
 <<--: b'\x00'
 <<--: None
 <<--: None
...
 <<--: None
That's all folks
  Do not hesitate to call send() and pump() for your own AT tests
```

The following functions are availables under the `test_lib` name space so you can test your own AT commands:
* __send()__ : sent an AT command the read the messages until the next OK or ERROR (timeout_ms = 3000 by default)
* __pump()__ : pump the messages over the serial connexion (timeout_ms = 5000 by default)

Here some samples of AT commands executed after `test_lib.py` execution.

``` python
>>> test_lib.send( 'at+cgmi' )
 -->>: at+cgmi
 <<--: b'at+cgmi\r\r\n'
 <<--: b'SIMCOM_Ltd\r\n'
 <<--: b'\r\n'
 <<--: b'OK\r\n'
>>> test_lib.send( 'at+cgmm' )
 -->>: at+cgmm
 <<--: b'at+cgmm\r\r\n'
 <<--: b'SIMCOM_SIM800C\r\n'
 <<--: b'\r\n'
 <<--: b'OK\r\n'
>>>
```

## Status (test_status.py)

The [`test_status.py`](examples/test_status.py) script return the status of several useful parameters available through `SimModem` class members.

```python
MicroPython v1.10 on 2019-01-25; PYBv1.1 with STM32F405RG
Type "help()" for more information.
>>>
>>> import test_status
debug: False
Status: Ready
Activating....
----[Iteration    0]--------------------------------
Status: Ready, callee:
Mode: 0, format: 0, operator: Orange
Signal Quality: -78 dBm
Network Registration Status: Registered, Home network
Unsollicited Result Code status: Disable Unsollicited Result Code
SIM Serial : 8932026618xxxxxxxxxx
IMEI serial : 86745xxxxxxxxxx
----[Iteration    1]--------------------------------
Status: Ready, callee:
Mode: 0, format: 0, operator: Orange
Signal Quality: -78 dBm
Network Registration Status: Registered, Home network
Unsollicited Result Code status: Disable Unsollicited Result Code
SIM Serial : 8932026618xxxxxxxxxx
IMEI serial : 86745xxxxxxxxxx
```

## Network Scan test (test_netscan.py)

The [`test_netscan.py`](examples/test_netscan.py) do scan the mobile networks aailable around.

The debug mode is not activated by default but you can switch it on to read the messages exchanged with the UART.

__Before execution the script__, change the value for the __PIN_CODE__ constant (to match the SIM card pincode).

``` python
MicroPython v1.10 on 2019-01-25; PYBv1.1 with STM32F405RG
Type "help()" for more information.
>>>
>>> import test_netscan
debug: False
-- Scan 1/5 ---------------------------------------------------
Scaning can takes up to 45s
-- Scan 2/5 ---------------------------------------------------
Scaning can takes up to 45s
<NetworkScan operator:Orange B, rxlev:26, cellid:0C2B, arfcn:41>
<NetworkScan operator:Orange B, rxlev:21, cellid:0C29, arfcn:37>
<NetworkScan operator:Orange B, rxlev:17, cellid:CC29, arfcn:32>
<NetworkScan operator:PROXIMUS, rxlev:40, cellid:3D66, arfcn:28>
<NetworkScan operator:PROXIMUS, rxlev:32, cellid:3D61, arfcn:30>
<NetworkScan operator:PROXIMUS, rxlev:27, cellid:3D5B, arfcn:71>
<NetworkScan operator:PROXIMUS, rxlev:24, cellid:3AFA, arfcn:4>
<NetworkScan operator:PROXIMUS, rxlev:19, cellid:A062, arfcn:2>
<NetworkScan operator:PROXIMUS, rxlev:18, cellid:B1D0, arfcn:86>
<NetworkScan operator:BASE, rxlev:31, cellid:B29D, arfcn:976>
<NetworkScan operator:BASE, rxlev:28, cellid:B29C, arfcn:985>
<NetworkScan operator:BASE, rxlev:19, cellid:B0F0, arfcn:982>
-- Scan 3/5 ---------------------------------------------------
...
```

## Pick up phone test (test_pickup.py)

The following test, available in [test_pickup.py](examples/test_pickup.py), waits a phone call, pick up the call and hang-up after 10 seconds.

Results:

``` python
>>> import test_pickup
debug: False
Status: Ready
Activating....
Iteration    0, Status: Ready, callee:
Iteration    1, Status: Ready, callee:
Iteration    2, Status: Ready, callee:
...
Iteration   19, Status: Ready, callee:
Iteration   20, Status: Ready, callee:
Iteration   21, Status: Ringing, callee:
Pickup phone (will ends in 10 secs)
Iteration   22, Status: Call in progress, callee: +3249692xxxx
Iteration   23, Status: Call in progress, callee: +3249692xxxx
Iteration   24, Status: Call in progress, callee: +3249692xxxx
Iteration   25, Status: Call in progress, callee: +3249692xxxx
...
...
...
Iteration   37, Status: Call in progress, callee: +3249692xxxx
Iteration   38, Status: Call in progress, callee: +3249692xxxx
Iteration   39, Status: Call in progress, callee: +3249692xxxx
Iteration   40, Status: Call in progress, callee: +3249692xxxx
Hangup call!
Iteration   41, Status: Ready, callee:
Iteration   42, Status: Ready, callee:
Iteration   43, Status: Ready, callee:
```

## Make a call test (test_call.py)

This example script, available in [test_call.py](examples/test_call.py), attempt to call the callee until it wait long enough for the script to hangup the call himself.
In this exemple we can clearly note a LONG latency in state change when the call is rejected (or prematurely) hangup by the callee.

Please note that each iteration implies a delay of 0.5 sec.

``` Python
MicroPython v1.10 on 2019-01-25; PYBv1.1 with STM32F405RG
Type "help()" for more information.
>>>
>>> import test_call
debug: False
Status: Ready
Activating....
Iteration    0, Status: Ready
Calling +3249692xxxx (will ends in 60 secs)
Hey the callee did hang-up! I wonna call it again...
Iteration    1, Status: Call in progress
Iteration    2, Status: Call in progress
Iteration    3, Status: Call in progress
Iteration    4, Status: Call in progress
Iteration    5, Status: Call in progress
Iteration    6, Status: Call in progress
Iteration    7, Status: Call in progress
Iteration    8, Status: Call in progress >>> Callee REJECT the CALL
Iteration    9, Status: Call in progress
Iteration   10, Status: Call in progress
Iteration   11, Status: Call in progress
...
... It may takes up to 40 sec to the caller to return to READY status
...
Iteration   88, Status: Call in progress
Iteration   89, Status: Call in progress
Iteration   90, Status: Ready
...
... The script detected the hang-up
... and waits for some additional time before recalling the callee
...
Hey the callee did hang-up! I wonna call it again...
Iteration   91, Status: Ready
Hey the callee did hang-up! I wonna call it again...
Iteration   92, Status: Ready
Hey the callee did hang-up! I wonna call it again...
...
...
...
Iteration  153, Status: Ready
Calling +3249692xxxx (will ends in 60 secs)
Hey the callee did hang-up! I wonna call it again...
Iteration  154, Status: Call in progress >>> Script makes a new call to callee
Iteration  155, Status: Call in progress
Iteration  156, Status: Call in progress
Iteration  157, Status: Call in progress
Iteration  158, Status: Call in progress
Iteration  159, Status: Call in progress
Iteration  160, Status: Call in progress >>> Callee pickup the call
Iteration  161, Status: Call in progress
Iteration  162, Status: Call in progress
...
...
...
Iteration  265, Status: Call in progress
Iteration  266, Status: Call in progress
Iteration  267, Status: Call in progress
Hangup call!                             >>> This time the scripts ends as espected!
That's all Folks!

```

# Envoi SMS

*** Traduction ***
The [test_sms_send.py](examples/test_sms_send.py) script, showned here below, will send SMS to a target phone number.

``` python
from machine import UART, Pin
from smodem import SimModem, AS_READY
import time

PIN_CODE = '1234'       # <<<<< CHANGE HERE !

PHONE = '+32496928xxx'  # <<<<< CHANGE HERE !

# UART and PowerPin to SIM Module
# Will be reconfigured by SimModem
uart = UART(1)  # X9, X10 sur Pyboard
pwr = Pin('Y3') # Broche Power On

m = SimModem( uart, pwr_pin = pwr, pin_code=PIN_CODE )
m.debug = False

r = m.activate()   # Activate/Réinit the modem
m.wait_for_ready() # Wait for the modem to be ready

mr = m.send_sms( PHONE, 'Hello world!\r\nFrom MicroPython' )
if mr:
	print( "Message sent. Message_reference: %i" % mr )
else:
	print( "Message not sent (or Message_reference not captured)" )

# Using Latin chars
mr = m.send_sms( PHONE, 'Bénédicte est la maîtresse à demeure :-)\r\nMerci MicroPython & NADHAT-GSM' )
if mr:
	print( "Message sent. Message_reference: %i" % mr )
else:
	print( "Message not sent (or Message_reference not captured)" )
```

Which produce the following results:

```
MicroPython v1.10 on 2019-01-25; PYBv1.1 with STM32F405RG
Type "help()" for more information.
>>>
>>> import test_sms_send
Modem initialized!
Message sent. Message_reference: 2
Message sent. Message_reference: 3
```

# Receiving a SMS (test_sms_read.py)

The [test_sms_read.py](examples/test_sms_read.py) script, listed here below, will receive and read SMS from the SIMCOM module.

__Note:__ The `m.stored_sms` sometime produce an error (which is send back by the SIMCOM module). Maybe make several tentative (the modem is perhaps not yet fully ready ?!?!)

``` python
from machine import UART, Pin
from smodem import SimModem, AS_READY
import time

PIN_CODE = '1234'  # <<<<< MODIFIER ICI !

# UART and PowerOn Pin wired to the SICOM will be reconfigured
# by the SimModem library
uart = UART(1) # X9, X10 on Pyboard
pwr = Pin('Y3') # Power On pin

m = SimModem( uart, pwr_pin = pwr, pin_code=PIN_CODE )
m.debug = False

r = m.activate() # Activate / Reinit the modem
print( 'Modem initialized!' )

# Wait for the modem to be ready
m.wait_for_ready()

# Some SMS may still be stored inside the SIMCOM module  memory OR received
# by the SIM800 while the microcontroler is not running its software. Then the
#   SMS are keept stored inside the SIM800 (the microcontroler did miss the
#   "Unsollicited Result Code" send over the UART)
#
# Here how to read and drop the message before overloading the available SMS SLOT SMS.
print( '==[ Display stored SMS ]=============================================' )
print( '' )
stored = m.stored_sms
for id in stored:
	sms = m.read_sms( id, delete=False ) # Must be dropped onto a distinct line because not registered into the received_list
	m.delete_sms( id )
	print( 'Sender : %s' % sms.sender )
	print( 'Time   : %s' % sms.send_date )
	for line in sms.lines:
		print( line )
	print( '-'*40 )

# Wait for the Next SMS and read them
print( '' )
print( '==[ Wait for SMS ]===================================================' )
print( '' )
while True:
	m.update()
	if m.has_sms:
		for id in m.rec_sms:
			sms = m.read_sms( id, delete=True ) # Delete it from the SMS Store
			print( 'Sender : %s' % sms.sender )
			print( 'Time   : %s' % sms.send_date )
			for line in sms.lines:
				print( line )
			print( '-'*40 )
```
Which produces the following results into the REPL session.

```
MicroPython v1.12 on 2020-05-12; PYBSTICK26_STD with STM32F411RE
Type "help()" for more information.
>>> import test_sms_read

debug: Modem already running
debug: Configure modem
debug: Modem configured!
Modem initialized!

==[ Display stored SMS ]=============================================


==[ Wait for SMS ]===================================================

Sender : +324969xxxx
Time   : 20/10/07 23:18:35+08
I love MicroPython
----------------------------------------
Sender : +324969xxxx
Time   : 20/10/07 23:19:28+08
1000000000 de fois plus efficace
----------------------------------------
```

# Shopping list
* [Carte NadHat GSM](https://shop.mchobby.be/fr/pi-hats/1656-nadhat-gsm-gprs-connecteur-sim800c-v1-3232100016569-garatronic.html)
* [Carte MicroPython Pyboard](https://shop.mchobby.be/fr/micropython/570-micropython-pyboard-3232100005709.html)
* [PYBStick Standard](https://shop.mchobby.be/fr/micropython/1844-pybstick-standard-26-micropython-et-arduino-3232100018440-garatronic.html) & [PYBStick-Hat-Face](https://shop.mchobby.be/fr/micropython/1935-interface-pybstick-vers-raspberry-pi-3232100019355.html)
