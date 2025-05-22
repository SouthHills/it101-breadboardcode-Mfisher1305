from gpiozero import RGBLED
from pathlib import Path
import time
import tkinter as tk
from tkinter import messagebox


class CPUTempGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Temperature")
        self.root.geometry("250x175")

        self.temp_label = tk.Label(root, text="Click Below\n|\nv", font=("Arial", 20))
        self.temp_label.pack(pady=20)
        
        self.update_button = tk.Button(root, text="Start Reading", command=self.update_temp)
        self.update_button.pack(pady=10)
        
    def read_temp(self):
        path = Path('/sys/class/thermal/thermal_zone0/temp')
        cpu = round(int(path.read_text().strip()) / 1000, 1)
        return f"{cpu} C"

    def update_temp(self):        
        self.temp_label.config(text=self.read_temp(), foreground="red", background="black", font=("Arial", 40))
        self.root.after(1000, self.update_temp)

# active_high must be true because it is a common anode RGBLed
LED = RGBLED(red=17, green=27, blue=22, active_high=True)

def set_color(r, g, b):
    """ Invert the colors due to using a common anode """
    LED.color = (1 - r, 1 - g, 1 - b)

def loop():
    while True :
        path = Path('/sys/class/thermal/thermal_zone0/temp')
        cpu = round(int(path.read_text().strip()) / 1000, 1)
        print(f"Temp: {cpu} C")
        if cpu <= 15.0:
            set_color(0, 0, 255)
        elif cpu >= 80.0:
            set_color(255, 0, 0)
        else:
            red = cpu / 100
            blue = 1 - (cpu / 100)
            set_color(red, 0, blue)
        root.update()
        time.sleep(1)
        
def destroy():
    LED.close()
    
if __name__ == '__main__':     # Program entrance
    print ('Program is starting ... ')
    root = tk.Tk()
    CPUGUI = CPUTempGUI(root)
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()