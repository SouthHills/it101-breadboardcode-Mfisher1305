from gpiozero import LED as LEDClass, Button
from signal import pause
import time

LED = LEDClass(17)  # define ledPin
BUTTON = Button(18)  # define buttonPin
flash = False

def changeLedState():
    global LED, BUTTON
    global flash
    
    print("starting strobe")
    flash = not flash
    
        
def loop():
    while True:
        if flash:
            LED.toggle()
            time.sleep(0.1)
        else:
            
            LED.off()

def destroy():
    global LED, BUTTON
    # Release resources
    LED.close()
    BUTTON.close()

if __name__ == "__main__":     # Program entrance
    print ("Program is starting...")
    try:
        # If the button gets pressed, call the function
        # This is an event
        BUTTON.when_pressed = changeLedState
        loop()
        
        pause()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()