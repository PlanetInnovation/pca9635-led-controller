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

import unittest

from mock_machine import register_as_machine

# Inject the mocked machine interface
register_as_machine()

from micropython_pca9635 import PCA9635  # noqa: E402


class TestPCA9635(unittest.TestCase):
    def test_import(self):
        """Test that PCA9635 can be imported."""
        self.assertIsNotNone(PCA9635)


if __name__ == "__main__":
    unittest.main()
