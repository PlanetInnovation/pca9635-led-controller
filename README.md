# micropython-pca9635

A MicroPython driver for the [PCA9635 16-channel I2C LED controller](https://www.nxp.com/products/power-management/lighting-driver-and-controller-ics/automotive-led-controllers/16-bit-fm-plus-i2c-bus-led-driver:PCA9635PW) with PWM

## Installation

### Using mip (recommended)
```python
import mip
mip.install("github:planetinnovation/micropython-pca9635")
```

### Manual installation
Download `micropython_pca9635.py` and copy it to your MicroPython device.

## Usage

```python
from micropython_pca9635 import PCA9635
from machine import I2C

# Initialize I2C bus
i2c = I2C(1, freq=100_000)

# Create PCA9635 instance with address based on address pins
address = PCA9635.address_from_pins(a6=0, a5=0, a4=0, a3=0, a2=0, a1=0, a0=0)
led_controller = PCA9635(i2c, address=address, reset=True)

# Set individual LED channel brightness (0-255)
led_controller.set(index=0, level=128)   # Set channel 0 to 50% brightness
led_controller.set(index=1, level=255)   # Set channel 1 to 100% brightness

# Turn off a specific LED
led_controller.off(index=0)

# Set all channels to the same level
led_controller.set_all(level=100)

# Shutdown - set all outputs to high-impedance mode
led_controller.shutdown()
```

## Features

- Control 16 independent LED channels
- 8-bit PWM resolution (256 levels) per channel
- Software reset support
- Individual and group channel control
- Configurable I2C address using 7 address pins
- Low-level register access for advanced configurations

## License

MIT License - Copyright (c) 2020, Planet Innovation
