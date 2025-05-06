from gpiozero import Buzzer, Button

BUZZER = Buzzer(17)
BUTTON = Button(12)

def loop():
    while True:
        if BUTTON.is_pressed: # if button is pressed
            BUZZER.on() # turn on buzzer
            print ('buzzer turned on >>>')
        else: # if button is relessed
            BUZZER.off() # turn off buzzer
            print ('buzzer turned off <<<')

def destroy():
    BUZZER.close()
    BUTTON.close()

if __name__ == '__main__':     # Program entrance
    print ('Program is starting...')
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()

