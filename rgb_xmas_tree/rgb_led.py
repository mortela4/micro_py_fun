"""
@file rgb_led.py

@brief Definitions for RGB-LED w. 'reduced' serial(=SPI) interface (SCK and SOUT connections only). 
"""


# Constants:
START_OF_FRAME = [0]*4      # A RGB-LED frame must START w. 32x SPI-clocks (SOUT='0')
END_OF_FRAME = [0]*5        # A RGB-LED frame must END w. 40x SPI-clocks (SOUT='0')


# ************************ TEST ******************************
if __name__ == "__main__":
    from machine import SPI
    #
    import time
    #
    spi = SPI("SPI_0")
    spi.init(baudrate=400000, polarity=0, phase=0, bits=8, firstbit=SPI.MSB)
    #
    intensity = 0xff
    rgb_val = [0xff]*3
    led_data = intensity + rgb_val 
    #
    test_data = START_OF_FRAME + led_data + END_OF_FRAME
    #
    for txb in test_data:
        spi.write(bytes([txb]))
    #
    time.sleep(10)
    #
    multi_led_data = led_data * 25      # 25x LEDs in string.
    #
    test_data = START_OF_FRAME + multi_led_data + END_OF_FRAME
    #
    for txb in test_data:
        spi.write(bytes([txb]))
    #  
    print("Done ...")

