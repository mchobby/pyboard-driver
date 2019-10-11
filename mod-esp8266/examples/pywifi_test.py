'''
Testing the pywifi from TonyLabs on the MOD-ESP8266 of Olimex Ltd

11 oct 2019, Domeu, Minor update for MOD-ESP8266

-- Original License --
The MIT License (MIT)
Copyright (c) 2016 TONYLABS, support@tonylabs.com
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

from pyb import Pin
import pyb
import pywifi

SSID = 'WIFI-NETWORK-SSID'
PASSPHRASE = 'WIFI-NETWORK-PASSWORD'

# On UART(1) @ 115200 bauds
esp = pywifi.ESP8266(1, 115200)

print('Testing generic methods')
print('=======================')
print('AT startup...')
if esp.test():
    print('Success!')
    pyb.LED(1).on() #GREEN LED ON
else:
    print('Failed!')

'''
print('Soft-Reset...')
if esp.reset():
    print('Success!')
else:
    print('Failed!')
'''

print('Another AT startup...')
if esp.test():
    print('Success!')
else:
    print('Failed!')

'''
print('Check ESP8266 firmware version')
print('==============================')
esp.version()
'''

print('Testing WIFI methods')
print('====================')
'''
1: station mode
2: accesspoint mode
3: accesspoint and station mode
'''

wifi_mode = 1
print("Testing get_mode/set_mode of value '%s'(%i)..." % (pywifi.WIFI_MODES[wifi_mode], wifi_mode))
esp.set_mode(wifi_mode)

if esp.get_mode() == wifi_mode:
    print('Success!')
else:
    print('Failed!')

pyb.delay(100)

print('Connecting to network')
print('==============================')
esp.connect(ssid=SSID, psk=PASSPHRASE)

pyb.delay(20)
print(esp.get_station_ip())

pyb.LED(1).off() #GREEN LED ON
pyb.LED(4).on() #BLUE LED ON

esp.start_connection(protocol='TCP', dest_ip='192.168.1.10', dest_port=80, debug=True)

esp.send('GET /index.php?temperature=23&light=658 HTTP/1.0\r\nHost: 192.168.1.10\r\n\r\n', debug=True)
