from gpiozero import RGBLED, Button
import time
import random
from signal import pause


# active_high must be true because it is a common anode RGBLed
LED = RGBLED(red=17, green=18, blue=27, active_high=True)
BUTTON = Button(24)
g = (0, 1, 0)
r = (1, 0, 0)
b = (0, 0, 1)
y = (1, 1, 0)
p = (0.5, 0, 0.5)
o = (1, 0.35, 0)
off = (0, 0, 0)
Colors = (g, r, b, y, p, o, off)
Green_light = False


def set_color(color):
    """ Invert the colors due to using a common anode """
    LED.color = (1 - color[0], 1 - color[1], 1 - color[2])

def initial_setup():
    LED.on()

def loop():
    global Colors, Green_light
    while True :
        if Green_light is False :
            random_int = random.randint(0,5)
            if random_int == 0:
                Green_light = True
            else:
                Green_light = False
        
            set_color(Colors[6])
            time.sleep(0.01)
            set_color(Colors[random_int])
            time.sleep(1)
        

def button_pressed():
    global Colors, Green_light
   
    if Green_light:
        for i in range(0,5):
            set_color(Colors[6])
            time.sleep(0.2)
            set_color(Colors[0])
            time.sleep(0.2)
    else: 
        for i in range(0,5):
            set_color(Colors[6])
            time.sleep(0.2)
            set_color(Colors[1])
            time.sleep(0.2)
    destroy()
        
def destroy(): 
    LED.close()
    
if __name__ == '__main__':     # Program entrance
    print ('Program is starting ... ')
    initial_setup()
    try:
        BUTTON.when_pressed = button_pressed
        loop()
        
        pause()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()