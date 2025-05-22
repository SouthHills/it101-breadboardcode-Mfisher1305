from gpiozero import LED as LEDClass # Alias
import time
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent.parent
sys.path.append(str(HERE / 'Common'))
from ADCDevice import *

USING_GRAVITECH_ADC = False

REDLED = LEDClass(18)  # define led
GREENLED = LEDClass(12)
BLUELED = LEDClass(27)
YELLED = LEDClass(6)
ADC = ADCDevice()

def setup():
    global ADC
    if(ADC.detectI2C(0x48) and USING_GRAVITECH_ADC): 
        ADC = GravitechADC()
    elif(ADC.detectI2C(0x48)): # Detect the pcf8591.
        ADC = PCF8591()
    elif(ADC.detectI2C(0x4b)): # Detect the ads7830
        ADC = ADS7830()
    else:
        print("No correct I2C address found, \n"
            "Please use command 'i2cdetect -y 1' to check the I2C address! \n"
            "Program Exit. \n")
        exit(-1)

def loop():
    global REDLED, GREENLED, YELLED, BLUELED, ADC
    while True:
        value = ADC.analogRead(0)
        if value / 255.0 < 0.25:
            BLUELED.off()
        elif value / 255.0 >= 0.25 and value / 255.0 < 0.5:
            BLUELED.on()
            GREENLED.off()
        elif value / 255.0 >= 0.5 and value / 255.0 < 0.75:
            GREENLED.on()
            YELLED.off()
        elif value / 255.0 >= 0.75 and value / 255.0 < 0.95:
            YELLED.on()
            REDLED.off()
        elif value / 255.0 >= 0.95:
            REDLED.on()
        
def destroy():
    global REDLED, GREENLED, YELLED, BLUELED, ADC
    # Release resources
    REDLED.close()
    GREENLED.close()
    BLUELED.close()
    YELLED.close()
    ADC.close()

if __name__ == "__main__":    # Program start point
    print("Program is starting ... \n")
    setup()
    try:
        loop()
    except KeyboardInterrupt:   # Press ctrl-c to end the program.
        destroy()
