# Description : Use ADC module to read the voltage value of potentiometer.
from pathlib import Path
import sys
from gpiozero import PWMLED
import time

HERE = Path(__file__).parent.parent
sys.path.append(str(HERE / 'Common'))
from ADCDevice import * 

USING_GRAVITECH_ADC = False # Only modify this if you are using a Gravitech ADC

LED1 = PWMLED(17) #17 is the pin
LED2 = PWMLED(19)
ADC = ADCDevice() # Define an ADCDevice class object

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
    global LED1, LED2
    while True:
        # read the ADC value of channel 0
        value1 = ADC.analogRead(0)  # Gets a value between 0 and 255
        value2 = ADC.analogRead(1)
        # Set LED brightness directly with value from ADC
        LED1.value = value1 / 255.0  # Value of PWM LED must be between 0 and 1
        LED2.value = value2 / 255.0
        # calculate the voltage value
        voltage1 = value1 / 255.0 * 3.3  # 3.3 because we are using the 3.3V lead
        print(f'ADC Value: {value1} \tVoltage: {voltage1:.2f}')
        voltage2 = value2 / 255.0 * 3.3  # 3.3 because we are using the 3.3V lead
        print(f'ADC Value: {value2} \tVoltage: {voltage2:.2f}')
        time.sleep(0.03)

def destroy():
    global LED1, LED2, ADC
    LED1.close()
    LED2.close()
    ADC.close()
    
if __name__ == '__main__':   # Program entrance
    print ('Program is starting ... ')
    try:
        setup()
        loop()
    except KeyboardInterrupt: # Press ctrl-c to end the program.
        destroy()
        
