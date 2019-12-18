"""
L3G.py - easy Gyroscope library for MicroPython Pyboard Original.

* Author(s):    Braccio M.  from MCHobby (shop.mchobby.be).
                Meurisse D. from MCHobby (shop.mchobby.be).

See project source @ https://github.com/mchobby/pyboard-driver/tree/master/zumo-robot

See example gyroscope.py in the project source
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
# OUT OF OR IN
# 

__version__ = "0.0.1"
__repo__ = "https://github.com/mchobby/pyboard-driver.git"

from machine import I2C
from micropython import const
import struct

L3DS20_RANGE_250DPS = const(0)   #measurement range
L3DS20_RANGE_500DPS = const(1)
L3DS20_RANGE_2000DPS = const(2)

_L3GD20_REGISTER_CTRL_REG1 = const(0x20) #0 0 1 0   0 0 0 0
_L3GD20_REGISTER_CTRL_REG2 = const(0x21) #0 0 1 0   0 0 0 0
_L3GD20_REGISTER_CTRL_REG3 = const(0x22) #0 0 1 0   0 0 0 0
_L3GD20_REGISTER_CTRL_REG4 = const(0x23) #0 0 1 0   0 0 1 1

# _L3GD20_REGISTER_OUT_X_L = const(0x28)
_L3GD20_REGISTER_OUT_X_L_X80 = const(0xA8) #1 0 1 0   1 0 0 0
_L3GD20_REGISTER_OUT_X_L_X40 = const(0x68) #0 1 1 0   1 0 0 0

_ID_REGISTER = const(0x0F) #0 0 0 0   1 1 1 1

_L3GD20_CHIP_ID = const(0xD4) #1 1 0 1   0 1 0 0
_L3GD20H_CHIP_ID = const(0xD7)  #1 1 0 1   0 1 1 1

_L3GD20_SENSITIVITY_250DPS = 0.00875      ## Roughly 22/256 for fixed point match
_L3GD20_SENSITIVITY_500DPS = 0.0175       ## Roughly 45/256
_L3GD20_SENSITIVITY_2000DPS = 0.070        ## Roughly 18/256


# pylint: disable=no-member
class L3GD20(object):
    """
    Driver for the L3GD20 3-axis Gyroscope sensor.

    :param int rng: a range value one of L3DS20_RANGE_250DPS (default), L3DS20_RANGE_500DPS, or
        L3DS20_RANGE_2000DPS
    """

    def __init__(self, rng=L3DS20_RANGE_250DPS):
        chip_id = self.read_register(_ID_REGISTER,True)     #registre WHO_AM_I
        print("Chip-ID: %s" %chip_id)
        if chip_id != _L3GD20_CHIP_ID and chip_id != _L3GD20H_CHIP_ID:

            raise RuntimeError("bad chip id (%x != %x or %x)" %
                               (chip_id, _L3GD20_CHIP_ID, _L3GD20H_CHIP_ID))

        if (rng != L3DS20_RANGE_250DPS) and (rng != L3DS20_RANGE_500DPS) and (rng != L3DS20_RANGE_2000DPS):
            raise ValueError("Range value must be one of L3DS20_RANGE_250DPS, "
                             "L3DS20_RANGE_500DPS, or L3DS20_RANGE_2000DPS")





        # Set CTRL_REG1 (0x20)
        # ====================================================================
        # BIT  Symbol    Description                                   Default
        # ---  ------    --------------------------------------------- -------
        # 7-6  DR1#0     Output data rate
        # 5-4  BW1#0     Bandwidth selection
        #     3  PD        0 = Power-down mode, 1 = normal#sleep mode
        #     2  ZEN       Z-axis enable (0 = disabled, 1 = enabled)
        #     1  YEN       Y-axis enable (0 = disabled, 1 = enabled)
        #     0  XEN       X-axis enable (0 = disabled, 1 = enabled)

        # Switch to normal mode and enable all three channels
        self.write_register(_L3GD20_REGISTER_CTRL_REG1, 0x0F)   #les 3 axes sont activé et le mode normal est selectioné

        # Set CTRL_REG2 (0x21)
        # ====================================================================
        # BIT  Symbol    Description                                   Default
        # ---  ------    --------------------------------------------- -------
        # 5-4  HPM1#0    High-pass filter mode selection
        # 3-0  HPCF3..0  High-pass filter cutoff frequency selection

        # Nothing to do ... keep default values
        # ------------------------------------------------------------------

        #  Set CTRL_REG3 (0x22)
        # ====================================================================
        # BIT  Symbol    Description                                   Default
        # ---  ------    --------------------------------------------- -------
        #     7  I1_Int1   Interrupt enable on INT1 (0=disable,1=enable)
        #     6  I1_Boot   Boot status on INT1 (0=disable,1=enable)
        #     5  H-Lactive Interrupt active config on INT1 (0=high,1=low)
        #     4  PP_OD     Push-Pull#Open-Drain (0=PP, 1=OD)
        #     3  I2_DRDY   Data ready on DRDY#INT2 (0=disable,1=enable)
        #     2  I2_WTM    FIFO wtrmrk int on DRDY#INT2 (0=dsbl,1=enbl)
        #     1  I2_ORun   FIFO overrun int on DRDY#INT2 (0=dsbl,1=enbl)
        #     0  I2_Empty  FIFI empty int on DRDY#INT2 (0=dsbl,1=enbl)

        #  Nothing to do ... keep default values
        #  -----------------------------------------------------------------

        #  Set CTRL_REG4 (0x23)
        # ====================================================================
        # BIT  Symbol    Description                                   Default
        # ---  ------    --------------------------------------------- -------
        #     7  BDU       Block Data Update (0=continuous, 1=LSB#MSB)
        #     6  BLE       Big#Little-Endian (0=Data LSB, 1=Data MSB)
        # 5-4  FS1#0     Full scale selection
        #                                 00 = 250 dps
        #                                 01 = 500 dps
        #                                 10 = 2000 dps
        #                                 11 = 2000 dps
        #     0  SIM       SPI Mode (0=4-wire, 1=3-wire)

        # Adjust resolution if requested

        if rng == L3DS20_RANGE_250DPS:
            self.scale = _L3GD20_SENSITIVITY_250DPS
            self.write_register(_L3GD20_REGISTER_CTRL_REG4, 0x00)  #0

        if rng == L3DS20_RANGE_500DPS:
            self.scale = _L3GD20_SENSITIVITY_500DPS
            self.write_register(_L3GD20_REGISTER_CTRL_REG4, 0x10) #0 0 0 1   0 0 0 0

        if rng == L3DS20_RANGE_2000DPS:
            self.scale = _L3GD20_SENSITIVITY_2000DPS
            self.write_register(_L3GD20_REGISTER_CTRL_REG4, 0x20) # 0 0 1 0   0 0 0 0


        # ------------------------------------------------------------------

        # Set CTRL_REG5 (0x24)
        # ====================================================================
        # BIT  Symbol    Description                                   Default
        # ---  ------    --------------------------------------------- -------
        #     7  BOOT      Reboot memory content (0=normal, 1=reboot)
        #     6  FIFO_EN   FIFO enable (0=FIFO disable, 1=enable)
        #     4  HPen      High-pass filter enable (0=disable,1=enable)
        # 3-2  INT1_SEL  INT1 Selection config
        # 1-0  OUT_SEL   Out selection config

        # Nothing to do ... keep default values
        # ------------------------------------------------------------------


    @property
    def gyro(self):
        """
        x, y, z angular momentum tuple floats, rescaled appropriately for
        range selected
        """
        raw = self.gyro_raw
        return tuple(self.scale*v for v in raw)


class L3GD20_I2C(L3GD20):
    """
    Driver for L3GD20 Gyroscope using I2C communications

    :param ~busio.I2C i2c: initialized busio I2C class
    :param int rng: the optional range value: L3DS20_RANGE_250DPS(default), L3DS20_RANGE_500DPS, or
        L3DS20_RANGE_2000DPS
    :param address: the optional device address, 0x68 is the default address
    """

#    gyro_raw = Struct(_L3GD20_REGISTER_OUT_X_L_X80, '<hhh')
    """Gives the raw gyro readings, in units of rad/s."""

    def __init__(self, i2c, rng=L3DS20_RANGE_2000DPS, address=0x6B): # 0 1 1 0   1 0 1 1 (107) adresse capteur

        self._device = i2c
        self._address = address
        super().__init__(rng)


        #import adafruit_bus_device.i2c_device as i2c_device
        #self.i2c_device = i2c_device.I2CDevice(i2c, address)
        #self.buffer = bytearray(2)


    def write_register(self, register, value,stop=True):
        """
        Update a register with a byte value

        :param int register: which device register to write
        :param value: a byte to write
        """
        buffer=bytes([register,value])   #

        self._device.writeto(self._address,buffer,stop)




        #self.buffer[0] = register
        #self.buffer[1] = value
        #with self.i2c_device as i2c:
        #    i2c.write(self.buffer)

    def read_register(self, register,stop=True):
        """
        Returns a byte value from a register

        :param register: the register to read a byte
        """

        data = bytes([register])     #registre qu'on veut lire du capteur
        self._device.writeto(self._address, data,stop)
                # If stop is true then a STOP condition is generated at the end of the transfer, even if a NACK is received.
                # The function returns the number of ACKs that were received.
        data= bytearray(1)
        self._device.readfrom_into(self._address,data,stop)
        return data[0]

        #self.buffer[0] = register
        #with self.i2c_device as i2c:
        #    i2c.write_then_readinto(self.buffer, self.buffer, out_end=1, in_start=1)
        #return self.buffer[1]

    def read(self):

        x_l = self.read_register(0x28)
        x_h = self.read_register(0x29)

        y_l = self.read_register(0x2A)
        y_h = self.read_register(0x2B)

        z_l = self.read_register(0x2C)
        z_h = self.read_register(0x2D)

        y=bytes([y_h,y_l])
        x=bytes([x_h,x_l])
        z=bytes([z_h,z_l])

        _y=struct.unpack(">h",y)[0]
        _x=struct.unpack(">h",x)[0]
        _z=struct.unpack(">h",z)[0]
        return(_x,_y,_z)



#class L3GD20_SPI(L3GD20):
#    """
#    Driver for L3GD20 Gyroscope using SPI communications
#
#    :param ~busio.SPI spi_busio: initialized busio SPI class
#    :param ~digitalio.DigitalInOut cs: digital in/out to use as chip select signal
#    :param int rng: the optional range value: L3DS20_RANGE_250DPS(default), L3DS20_RANGE_500DPS, or
#        L3DS20_RANGE_2000DPS
#    :param baudrate: spi baud rate default is 100000
#    """
#    def __init__(self, spi_busio, cs, rng=L3DS20_RANGE_250DPS, baudrate=100000):
#        import adafruit_bus_device.spi_device as spi_device
#        self._spi = spi_device.SPIDevice(spi_busio, cs, baudrate=baudrate)
#        self._spi_bytearray1 = bytearray(1)
#        self._spi_bytearray6 = bytearray(6)
#        super().__init__(rng)
#
#    def write_register(self, register, value):
#        """
#        Low level register writing over SPI, writes one 8-bit value
#
#        :param int register: which device register to write
#        :param value: a byte to write
#        """
#        register &= 0x7F  # Write, bit 7 low.
#        with self._spi as spi:
#            spi.write(bytes([register, value & 0xFF]))    #255
#
#    def read_register(self, register):
#        """
#        Low level register reading over SPI, returns a list of values
#
#        :param register: the register to read a byte
#        """             #1 0 0 0   0 0 0 0
#        register = (register | 0x80) & 0xFF  # Read single, bit 7 high.
#        with self._spi as spi:
#            self._spi_bytearray1[0] = register
#            spi.write(self._spi_bytearray1)
#            spi.readinto(self._spi_bytearray1)
#            # Uncomment to dump bytearray:
#            # print("$%02X => %s" % (register, [hex(i) for i in self._spi_bytearray1]))
#            return self._spi_bytearray1[0]
#
#    def read_bytes(self, register, buffer):
#        """
#        Low level register stream reading over SPI, returns a list of values
#
#        :param register: the register to read bytes
#        :param bytearray buffer: buffer to fill with data from stream
#        """
#        register = (register | 0x80) & 0xFF  # Read single, bit 7 high.
#        with self._spi as spi:
#            self._spi_bytearray1[0] = register
#            spi.write(self._spi_bytearray1)
#            spi.readinto(buffer)
#
    @property
    def gyro_raw(self):
        """Gives the raw gyro readings, in units of rad/s."""
        buffer = self._spi_bytearray6
        self.read_bytes(_L3GD20_REGISTER_OUT_X_L_X40, buffer)
        return unpack('<hhh', buffer)
