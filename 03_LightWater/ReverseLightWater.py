# NOTE: If this fails to run, turn off the SPI and I2C interfaces.
# Turn them back on when this lab is complete.
# Alternatively, you can use the lesser abstracted RPi.GPIO interface
#   in the LightWater_RPi.GPIO.py file.
from gpiozero import LEDBarGraph
from time import sleep

LED_PINS : list[int] = [17, 18, 27, 22, 23, 24, 25, 2, 3, 12]
LEDS = LEDBarGraph(*LED_PINS, active_high=False)

def setup():
    global LEDS
    for led in LEDS:  # make led(on) move from left to right
        led.on()

def loop():
    global LEDS
    while True:
        for led in LEDS:  # make led(on) move from left to right
            led.off()
            sleep(0.2)
            led.on()
        for led in LEDS[::-1]:  # make led(on) move from right to left
            led.off()
            sleep(0.2)
            led.on()
            
def destroy():
    global LEDS
    for led in LEDS:  # make led(on) move from left to right
        led.close()

if __name__ == '__main__':  # Program entrance
    print ('Program is starting...')
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()