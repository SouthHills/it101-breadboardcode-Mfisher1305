from gpiozero import RGBLED, Button
from signal import pause
import time
import random

# active_high must be true because it is a common anode RGBLed
LED = RGBLED(red=17, green=18, blue=27, active_high=True)
BUTTON = Button(24) # define buttonPin
on = False

def set_color(r, g, b):
    """ Invert the colors due to using a common anode """
    LED.color = (1 - r, 1 - g, 1 - b)

def initial_test():
    set_color(1, 0, 0)
    print("All red")
    time.sleep(1)
    set_color(0, 1, 0)
    print("All green")
    time.sleep(1)
    set_color(0, 0, 1)
    print("All blue")
    time.sleep(1)

def loop():
    while True :
        if on:
            r=random.randint(0,100)
            g=random.randint(0,100)
            b=random.randint(0,100)
            set_color(r / 100, g / 100, b / 100) # Colors should be between 0 and 1
            print (f'r={r}% \tg={g}% \tb={b}%')
            time.sleep(1)
        else:
            LED.on()
        
def changeLedState():
    global LED, BUTTON
    global on
    
    print("Starting cycle")
    on = not on
        
def destroy():
    LED.close()
    
if __name__ == '__main__':     # Program entrance
    print ('Program is starting ... ')
    initial_test()
    try:
        BUTTON.when_pressed = changeLedState
        loop()
        pause()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()