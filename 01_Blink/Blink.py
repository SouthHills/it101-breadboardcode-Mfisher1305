from gpiozero import LED as LEDClass # Alias
import time

LED1 = LEDClass(17)  # define led
LED2 = LEDClass(19)

def loop():
    global LED1
    while True:
        LED1.on() 
        LED2.off()
        print ("led turned on >>>") # print information on terminal
        time.sleep(1)
        LED1.off()
        LED2.on()
        print ("led turned off <<<")
        time.sleep(1)
        
def destroy():
    global LED1
    # Release resources
    LED1.close()
    LED2.close()

if __name__ == "__main__":    # Program start point
    print("Program is starting ... \n")
    print(f"Using pin {LED1.pin} and {LED2.pin}")
    try:
        loop()
    except KeyboardInterrupt:   # Press ctrl-c to end the program.
        destroy()
