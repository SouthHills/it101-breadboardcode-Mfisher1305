# Description: Use the LCD display to display data
from lcd_display import LCDDisplayWrapper as LCDDisplay
from time import sleep
from datetime import datetime
from pathlib import Path
import sys
from gpiozero import TonalBuzzer, Button
from signal import pause

HERE = Path(__file__).parent.parent
sys.path.append(str(HERE / 'Common'))
from ADCDevice import * 

lcd = LCDDisplay()
BUZZER = TonalBuzzer(17)
is_ringing = False
BUTTON = Button(18)

USING_GRAVITECH_ADC = False # Only modify this if you are using a Gravitech ADC

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
    
    
 
def get_time_now():     # get system time
    return datetime.now().strftime('    %H:%M:%S')
    
def loop():
    global is_ringing
    while(True):
        lcd.clear()
        current_time = get_time_now()
        lcd.display_message(current_time, row=2)   # display the current time
        lcd.display_message("  Enter  Alarm", row=1)    # placeholder text
        alarm = get_time()
        lcd.clear()
        lcd.display_message(alarm, row=1)      # set time for alarm
        while(True):
            current_time = get_time_now()
            lcd.display_message(current_time, row=2)  # display the time
            if current_time == alarm:
                break
            volume = ADC.analogRead(0)    # read the ADC value of channel 0
            sleep(0.1)
        is_ringing = True
        while(is_ringing):
            volume = ADC.analogRead(0)
            if volume < 90:     # below 88 causes an error since its under the lowest tone possible
                volume = 90     
            for i in range(1,4):
                lcd.display_message(alarm, row=1)
                lcd.display_message(alarm, row=2)
                BUZZER.play(volume * 2.5, ) # max is 256, so multiply 2.5 to make it louder
                sleep(0.2)
                BUZZER.stop()
                sleep(0.2)
                lcd.clear()
            sleep(1)
            
        
def get_time():
    alarm = input("Set alarm (hh:mm:ss): ")
    return f"    {alarm}"

def stop_ringing():
    global is_ringing
    if is_ringing:
        is_ringing = False
    print("button pressed")
    BUZZER.stop()
        
def destroy():
    print('\nTerminating LCD instance. May take a moment...')
    lcd.clear()
    ADC.close()
    BUZZER.close()
    BUTTON.close()
    
if __name__ == '__main__':
    print ('Program is starting ... ')
    setup()
    try:
        BUTTON.when_pressed = stop_ringing
        loop()
    except KeyboardInterrupt:
        destroy()