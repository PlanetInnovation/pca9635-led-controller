# -*- coding: utf-8 -*-
#
# PI Background IP
# Copyright (c) 2026, Planet Innovation Pty Ltd
# 436 Elgar Rd, Box Hill, 3128, VIC, Australia
# Phone: +61 3 9945 7510
#
# The copyright to the computer program(s) herein is the property of
# Planet Innovation, Australia.
# The program(s) may be used and/or copied only with the written permission
# of Planet Innovation or in accordance with the terms and conditions
# stipulated in the agreement/contract under which the program(s) have been
# supplied.

metadata(
    version="0.0.1",
    description="MicroPython driver for PCA9635 16-channel I2C LED controller with PWM",
)


module("micropython_pca9635.py")


# Any project runtime dependencies should be added here, eg. from micropython-lib
require("logging")
