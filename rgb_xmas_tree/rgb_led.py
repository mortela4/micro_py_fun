"""
@file rgb_led.py

@brief Definitions for RGB-LED w. 'reduced' serial(=SPI) interface (SCK and SOUT connections only). 
"""


# Constants:
# ----------
NUM_LEDS_IN_STRING = 25
# 
START_OF_FRAME = [0]*4      # A RGB-LED frame must START w. 32x SPI-clocks (SOUT='0')
END_OF_FRAME = [0]*5        # A RGB-LED frame must END w. 40x SPI-clocks (SOUT='0')
ONE_OFF = [0xE0, 0, 0, 0]
ALL_OFF = ONE_OFF*25


# ************************ TEST ******************************
if __name__ == "__main__":
    from machine import SPI
    #
    import time
    #
    spi = SPI("SPI_0")
    spi.init(baudrate=400000, polarity=0, phase=0, bits=8, firstbit=SPI.MSB)
    #
    def all_off():
        spi.write(bytes(START_OF_FRAME + ALL_OFF + END_OF_FRAME))
    #
    all_off()
    #
    time.sleep(1)
    #
    intensity = [0x0f]
    rgb_val = [0x04, 0x04, 0]
    led_data = intensity + rgb_val 
    #
    test_data = START_OF_FRAME + led_data + END_OF_FRAME
    # Light the 1.st LED in string:
    print("Testing single LED ...")
    for txb in test_data:
        spi.write(bytes([txb]))
    #
    time.sleep(10)
    #
    multi_led_data = led_data * 25      # 25x LEDs in string.
    #
    test_data = START_OF_FRAME + multi_led_data + END_OF_FRAME
    # Light ALL the LEDs in string:
    print("Testing ALL 25 of the LEDs in string ...")
    spi.write(bytes(test_data))
    #for txb in test_data:
    #    spi.write(bytes([txb]))
    #  
    time.sleep(5)
    #
    all_off()
    #
    print("Done ...")

