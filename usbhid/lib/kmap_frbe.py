""" ScanCode Mapping for AZERTY keyboard (FR_BE layout)

    Copyright 2019, Meurisse D. for shop.MCHobby.be
"""
__version__ = '0.0.1'

# HID standard Modifier Flasg
PLAIN      = 0x00
SHIFT      = 0x02  # Shift left
SHIFT_RIGHT= 0x20
CTRL       = 0x01  # Ctrl left
CRTL_RIGHT = 0x10
ALT        = 0x04  # Alt on left
ALT_GR     = 0x40  # Alt right
GUI        = 0x08  # GUI Left - should be Windows Key
GUI_RIGHT  = 0x80  # GUI Right

kmap = dict()

# Row 1
kmap['²'] = (0x35,PLAIN)
kmap['³'] = (0x35,SHIFT)
kmap['&'] = (0x1e,PLAIN)
kmap['1'] = (0x1e,SHIFT)
kmap['|'] = (0x1e,ALT_GR)
kmap['é'] = (0x1f,PLAIN)
kmap['2'] = (0x1f,SHIFT)
kmap['@'] = (0x1f,ALT_GR)
kmap['"'] = (0x20,PLAIN)
kmap['3'] = (0x20,SHIFT)
kmap['#'] = (0x20,ALT_GR)
kmap["'"] = (0x21,PLAIN)
kmap['4'] = (0x21,SHIFT)
kmap['('] = (0x22,PLAIN)
kmap['5'] = (0x22,SHIFT)
kmap['§'] = (0x23,PLAIN)
kmap['6'] = (0x23,SHIFT)
kmap['è'] = (0x24,PLAIN)
kmap['7'] = (0x24,SHIFT)
kmap['!'] = (0x25,PLAIN)
kmap['8'] = (0x25,SHIFT)
kmap['ç'] = (0x26,PLAIN)
kmap['9'] = (0x26,SHIFT)
kmap['{'] = (0x26,ALT_GR)
kmap['à'] = (0x27,PLAIN)
kmap['0'] = (0x27,SHIFT)
kmap['}'] = (0x27,ALT_GR)
kmap[')'] = (0x2d,PLAIN)
kmap['°'] = (0x2d,SHIFT)
kmap['-'] = (0x2e,PLAIN)
kmap['_'] = (0x2e,SHIFT)


# Row 2
kmap['a'] = (0x14,PLAIN)
kmap['A'] = (0x14,SHIFT)
kmap['z'] = (0x1a,PLAIN)
kmap['Z'] = (0x1a,SHIFT)
kmap['e'] = (0x08,PLAIN)
kmap['E'] = (0x08,SHIFT)
kmap['€'] = (0x08,ALT_GR)
kmap['r'] = (0x15,PLAIN)
kmap['R'] = (0x15,SHIFT)
kmap['t'] = (0x17,PLAIN)
kmap['T'] = (0x17,SHIFT)
kmap['y'] = (0x1c,PLAIN)
kmap['Y'] = (0x1c,SHIFT)
kmap['u'] = (0x18,PLAIN)
kmap['U'] = (0x18,SHIFT)
kmap['i'] = (0x0c,PLAIN)
kmap['I'] = (0x0c,SHIFT)
kmap['o'] = (0x12,PLAIN)
kmap['O'] = (0x12,SHIFT)
kmap['p'] = (0x13,PLAIN)
kmap['P'] = (0x13,SHIFT)
kmap['^'] = (0x2f,PLAIN)
#kmap[''] = (0x2f,SHIFT)
kmap['['] = (0x2f,ALT_GR)
kmap['$'] = (0x30,PLAIN)
kmap['*'] = (0x30,SHIFT)
kmap[']'] = (0x30,ALT_GR)
kmap['\r'] = (0x28, PLAIN) # return key

# Row 3
kmap['q'] = (0x04,PLAIN)
kmap['Q'] = (0x04,SHIFT)
kmap['s'] = (0x16,PLAIN)
kmap['S'] = (0x16,SHIFT)
kmap['d'] = (0x07,PLAIN)
kmap['D'] = (0x07,SHIFT)
kmap['f'] = (0x09,PLAIN)
kmap['F'] = (0x09,SHIFT)
kmap['g'] = (0x0a,PLAIN)
kmap['G'] = (0x0a,SHIFT)
kmap['h'] = (0x0b,PLAIN)
kmap['H'] = (0x0b,SHIFT)
kmap['j'] = (0x0d,PLAIN)
kmap['J'] = (0x0d,SHIFT)
kmap['k'] = (0x0e,PLAIN)
kmap['K'] = (0x0e,SHIFT)
kmap['l'] = (0x0f,PLAIN)
kmap['L'] = (0x0f,SHIFT)
kmap['m'] = (0x33,PLAIN)
kmap['M'] = (0x33,SHIFT)
kmap['ù'] = (0x24,PLAIN)
kmap['%'] = (0x34,SHIFT)
kmap['µ'] = (0x32,PLAIN)
kmap['£'] = (0x32,SHIFT)

# Row 4
kmap['<'] = (0x64,PLAIN)
kmap['>'] = (0x64,SHIFT)
kmap['\\'] = (0x64,ALT_GR)
kmap['w'] = (0x1d,PLAIN)
kmap['W'] = (0x1d,SHIFT)
kmap['x'] = (0x1b,PLAIN)
kmap['X'] = (0x1b,SHIFT)
kmap['c'] = (0x06,PLAIN)
kmap['C'] = (0x06,SHIFT)
kmap['v'] = (0x19,PLAIN)
kmap['V'] = (0x19,SHIFT)
kmap['b'] = (0x05,PLAIN)
kmap['B'] = (0x05,SHIFT)
kmap['n'] = (0x11,PLAIN)
kmap['N'] = (0x11,SHIFT)
kmap[','] = (0x10,PLAIN)
kmap['?'] = (0x10,SHIFT)
kmap[';'] = (0x36,PLAIN)
kmap['.'] = (0x36,SHIFT)
kmap[':'] = (0x37,PLAIN)
kmap['/'] = (0x37,SHIFT)
kmap['='] = (0x38,PLAIN)
kmap['+'] = (0x38,SHIFT)
kmap['~'] = (0x38,ALT_GR)

kmap[' '] = (0x2c,PLAIN)
