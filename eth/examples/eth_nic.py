from pyb import SPI, Pin
import network

nic = network.WIZNET5K( SPI(1), Pin.board.X5, Pin.board.X4 )
print( "Activate")
nic.active( True )
# Fixing static IP
# nic.ifconfig(('10.0.0.77', '255.255.255.0', '10.0.0.240', '8.8.8.8'))
print( "Querying DHCP for address" )
nic.ifconfig('dhcp')
print( "getting IP config" )
print( nic.ifconfig() )
# returns ('192.168.1.60', '255.255.255.0', '192.168.1.1', '192.168.1.1')
print( nic.isconnected() )
# returns True
