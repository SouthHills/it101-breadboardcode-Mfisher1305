import subprocess
from gpiozero import Button
from signal import pause

CBUTTON = Button(24)  # Chromium button
FBUTTON = Button(12)  # Firefox button
Cprocess = subprocess
Fprocess = subprocess

chromium_active = False
def openCloseChromium():
    global chromium_active, Cprocess
    
    print("chromium button pressed")
    if chromium_active is False:
        Cprocess = subprocess.Popen(["chromium"])
        print ("opening chromium")
        chromium_active = True
    else:
        Cprocess.terminate()
        print ("closing chromium")
        chromium_active = False
                
firefox_active = False

def openCloseFirefox():
    global firefox_active, Fprocess
    
    print("firefox button pressed")
    if firefox_active is False:
        Fprocess = subprocess.Popen(["firefox"])
        print ("opening firefox")
        firefox_active = True
    else:
        Fprocess.terminate()
        print ("closing firefox")
        firefox_active = False

def destroy():
    global BUTTON
    # Release resources
    BUTTON.close()

if __name__ == "__main__":     # Program entrance
    print ("Program is starting...")
    try:
        # If the button gets pressed, call the function
        # This is an event
        CBUTTON.when_pressed = openCloseChromium
        FBUTTON.when_pressed = openCloseFirefox
        pause()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()

