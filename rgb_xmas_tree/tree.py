"""
@file tree.py

@brief Controls RGB X-mas tree HW from PiHut via SPI.
Converted to uPy-libraries or custom code (where necessary) for uPy-platform.
"""

# from gpiozero import SPIDevice, SourceMixin
from machine import SPI                             # NOTE: we do NOT need any ChipSelect-pin, so no need to import 'Pin' class!!

from colorzero import Color, Hue                    # See: https://github.com/waveform80/colorzero

#from statistics import mean                        # NOT part of uPy std.lib!! 
from stat_funcs import mean                         # Replacement! See: https://github.com/rcolistete/MicroPython_Statistics

from time import sleep                              # 'time' is part of uPy std.lib


class Pixel:
    """ Strictly speaking a dataclass - modeling a single RGB-LED device. """
    def __init__(self, index):
        self.index = index          # Represents its number in the LED-string --> idx=0 is first(i.e. closest to SPI-host) in string.
        self.value = 0, 0, 0        # 'value' is actually color.
    
    @property
    def value(self):
        return self.value           # Return color(=RGB) value.

    @value.setter
    def value(self, value):
        self.value = value

    @property
    def color(self):
        r, g, b = self.value
        # return Color(*self.value)
        return r, g, b

    @color.setter
    def color(self, c):
        r, g, b = c             # TODO: assess - is this really necessary??
        self.value = (r, g, b)

    def on(self):
        self.value = (1, 1, 1)

    def off(self):
        self.value = (0, 0, 0)


class RGBXmasTree():
    def __init__(self, spi_num=0, pixels=25, brightness=0.5):
        # Set up SPI device w. 1MHz clock frequency:
        self._spi_dev = SPI(spi_num, baudrate=1000000)
        # 
        self._all = [Pixel(parent=self, index=i) for i in range(pixels)]
        # Initialize LEDs --> turn all OFF:
        self._value = [(0, 0, 0)] * pixels
        self.brightness = brightness            # Default brightness ...
        self.off()

    @property
    def color(self):
        average_r = mean(pixel.color[0] for pixel in self)
        average_g = mean(pixel.color[1] for pixel in self)
        average_b = mean(pixel.color[2] for pixel in self)
        return Color(average_r, average_g, average_b)           # TODO: re-implement!

    @color.setter
    def color(self, c, idx):
        r, g, b = c
        self.pixels[idx].value = r, g, b

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, brightness):
        max_brightness = 31
        self._brightness_bits = int(brightness * max_brightness)
        self._brightness = brightness

    @property
    def value(self):
        return self._value

    @value.setter                   # TODO: redo this!
    def value(self, value):
        start_of_frame = [0]*4
        end_of_frame = [0]*5
                     # SSSBBBBB (start, brightness)
        brightness = 0b11100000 | self._brightness_bits
        pixels = [[int(255*v) for v in p] for p in value]
        pixels = [[brightness, b, g, r] for r, g, b in pixels]
        pixels = [i for p in pixels for i in p]
        data = start_of_frame + pixels + end_of_frame
        self._spi_dev.write(data)
        self._value = value

    def on(self):
        self.value = ((1, 1, 1),) * len(self)

    def off(self):
        self.value = ((0, 0, 0),) * len(self)

    def close(self):
        pass                # What's the point in 'cleanup' here?? (release SPI-device???)


# **************************** BASIC TEST ***********************************
if __name__ == '__main__':
    tree = RGBXmasTree()
    
    tree.on()                   # All RGB-LEDs = 'ON' w. pattern=0xFFFFFF(FF)='white' (at full intensity).
