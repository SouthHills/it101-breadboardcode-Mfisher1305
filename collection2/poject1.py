from gpiozero import LED as LEDClass # Alias
import time
import subprocess

REDLED = LEDClass(17)  # define led
GREENLED = LEDClass(18)

def loop():
    global REDLED, GREENLED
    while True:
        if is_internet_connected() is True:
            REDLED.off()
            GREENLED.on()
        else:
            REDLED.on()
            GREENLED.off()
        
def is_internet_connected():
    try:
        # Run the ping command with a timeout of 2 seconds and count 1 packet
        subprocess.check_output(['ping', '-c', '1', '-W', '2', 'www.google.com'])
        return True
    except subprocess.CalledProcessError:
        return False
        
def destroy():
    global REDLED, GREENLED
    # Release resources
    REDLED.close()
    GREENLED.close()

if __name__ == "__main__":    # Program start point
    print("Program is starting ... \n")
    
    try:
        loop()
    except KeyboardInterrupt:   # Press ctrl-c to end the program.
        destroy()
