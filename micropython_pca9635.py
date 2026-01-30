# -*- coding: utf-8 -*-
# !/usr/bin/env python
#
#   Copyright (c) 2020, Planet Innovation
#   436 Elgar Road, Box Hill VIC 3128 Australia
#   Phone: +61 3 9945 7510
#
#   The copyright to the computer program(s) herein is the property of
#   Planet Innovation, Australia.
#   The program(s) may be used and/or copied only with the written permission
#   of Planet Innovation or in accordance with the terms and conditions
#   stipulated in the agreement/contract under which the program(s) have been
#   supplied.
#
#   @file driver for PCA9635

"""A MicroPython driver for the PCA9635 LED controller.

The driver provides 16 output channels and can apply 8-bit PWM to each channel.

See manufacturer site:

    https://www.nxp.com/products/power-management/lighting-driver-and-controller-ics/automotive-led-controllers/16-bit-fm-plus-i2c-bus-led-driver:PCA9635PW

Evolved from a driver based on the Kinder project which was based on an Adafruit
driver for the PCA9685:

    https://gitlab.pi.planetinnovation.com.au/kinder/kinder_app/-/blob/master/src/lib/pca9635.py
    https://github.com/adafruit/micropython-adafruit-pca9685
"""

import ustruct  # pylint: disable=import-error
import utime  # pylint: disable=import-error


class PCA9635:
    # Registers/etc:
    # please refer data sheet for PCA9635
    MODE1 = 0x00
    MODE2 = 0x01

    LED0_PMW = 0x02

    LEDOUT0 = 0x14
    LEDOUT1 = 0x15
    LEDOUT2 = 0x16
    LEDOUT3 = 0x17

    # Mode1:
    SLEEP = 0x10
    ALLCALL = 0x01

    # Mode2:
    INVRT = 0x10  # Output logic state inverted. Value to use when no external driver used.
    OCH_SET_ON_STOP = 0x00  # Outputs change trigger
    OCH_SET_ON_ACK = 0x08  # Outputs change trigger
    OUTDRV_OPEN_DRAIN = 0x00  # Outputs driver mode
    OUTDRV_TOTEM_POLE = 0x04  # Outputs driver mode
    OUTNE_LOW_WHEN_DISABLED = 0x00  # LEDn = 0
    OUTNE_HIGH_WHEN_DISABLED = 0x01  # LEDn = high-impedance when OUTDRV = 0,  1 when OUTDRV = 1
    OUTNE_HIZ_WHEN_DISABLED = 0x02  # LEDn = high-impedance.

    # Reset
    RESET_ADDR = 0x03
    RST_CMD = b"\xa5\x5a"

    MAX_LEVEL = 255  # 8 bit PWM max

    def __init__(self, i2c, address=0x40, reset=True):
        """

        :param i2c: User passed I2C object
        :param address: I2C address
        :param reset: Command board reset on init
        """
        self.i2c = i2c
        self.address = address
        self.buff = bytearray(1)  # preallocate for interrupt usage

        if reset:
            self.reset()

    def _write(self, address, value):
        self.i2c.writeto_mem(self.address, address, bytearray([value]))

    def _read(self, address):
        return self.i2c.readfrom_mem_into(self.address, address, self.buff)[0]

    def shutdown(self):
        """Ensure led output drivers are in high impedance mode"""
        self._write(
            self.MODE2,
            self.OUTNE_HIZ_WHEN_DISABLED | self.OUTDRV_OPEN_DRAIN | self.OCH_SET_ON_ACK,
        )
        self.set_all(0)

    def reset(self):
        """
        Send Software Reset on I2C
        :return:
        """
        # Ref 7.6 Software reset
        self.i2c.writeto(self.RESET_ADDR, self.RST_CMD)
        utime.sleep_us(5)  # bus free time between a STOP and START condition (4.7 micro seconds)

        self._write(self.MODE1, self.ALLCALL)
        self._write(
            self.MODE2,
            self.OUTNE_HIZ_WHEN_DISABLED | self.OUTDRV_OPEN_DRAIN | self.OCH_SET_ON_ACK,
        )

        # Two bits per output channel, \b10 => "LED driver x individual
        # brightness controlled through its PWMx register"
        self._write(self.LEDOUT0, 0xAA)
        self._write(self.LEDOUT1, 0xAA)
        self._write(self.LEDOUT2, 0xAA)
        self._write(self.LEDOUT3, 0xAA)

        self.set_all(0)

    def set(self, index=None, level=None):
        """
        :param int index:
        :param int level: 8 bit pmw value
        :return:
        """
        assert self.validate_value(level)
        address = self.LED0_PMW + index
        if level is None:
            self.i2c.readfrom_mem_into(self.address, address, self.buff)
            return ustruct.unpack_from("<B", self.buff, 0)  # <B unsigned char ( 1 byte)

        ustruct.pack_into("<B", self.buff, 0, level)
        self.i2c.writeto_mem(self.address, address, self.buff)

        return True

    @staticmethod
    def validate_value(level):
        """
        validate if LED value is valid as per specs
        :param int level: pwm value
        :return: True if value is valid False otherwise
        """
        # Each LED output has its own 8-bit resolution (256 steps) fixed frequency individual PWM
        return isinstance(level, int) and 0 <= level <= PCA9635.MAX_LEVEL

    def off(self, index=None):
        """Turn an LED off"""
        address = self.LED0_PMW + index
        self.i2c.writeto_mem(self.address, address, b"\x00")

    def set_all(self, level):
        """
        Set all led channels to provided level
        :param int level:
        :return:
        """
        assert self.validate_value(level)

        for i in range(16):
            self.set(i, level)

    @staticmethod
    def address_from_pins(a6, a5, a4, a3, a2, a1, a0):
        # pylint: disable=invalid-name,too-many-arguments
        """
        Returns device address for PCA9685 based on physical address pins
        :param bool|int a6: Address pin A6
        :param bool|int a5: Address pin A5
        :param bool|int a4: Address pin A4
        :param bool|int a3: Address pin A3
        :param bool|int a2: Address pin A2
        :param bool|int a1: Address pin A1
        :param bool|int a0: Address pin A0
        :return: int
        """
        address = 0b0000000
        for i, pin in enumerate((a0, a1, a2, a3, a4, a5, a6)):
            address |= int(pin) << i
        return address
