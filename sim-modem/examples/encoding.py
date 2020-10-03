#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-

s = 'é' # Latin1 - Small letter e with acute accent - decimal 233

print( s[0] ) # é Should be displayed properly into Python output
print( ord(s[0]) ) # Should display 233

data = s.encode('ISO-8859-1') # Extended ASCII for Latin1.
print( data )     # Should only contains 1 byte with value 233
print( data[0] )  # should display 233
