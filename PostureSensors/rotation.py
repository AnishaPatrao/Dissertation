#Filename: dance.py
#Description: Used to light the connect with micro:bit

# import required modules
import os 
import time
from datetime import datetime 
from serial import Serial 
import re

nextCompassPoll = 0.0 
rotationStr = ""
numbers = re.compile('-?\d+')

#serial connectoion to the microbit - microbits device id is stored in the below path
serialDevDir='/dev/serial/by-id' 

def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

#function to trigger the microbit
def GetRotation():
    try:
        if (os.path.isdir(serialDevDir)):
            serialDevices = os.listdir(serialDevDir) 
            if (len(serialDevices) > 0):
                serialDevicePath = os.path.join(serialDevDir, serialDevices[0])
                serial = Serial(port=serialDevicePath, baudrate=115200, timeout=0.2) 
                #send a serial signal to the microbit
                time.sleep(0.01)
                rotationStr = str(serial.readline())
                if has_numbers(rotationStr):
                    result = list(map(int, numbers.findall(rotationStr)))
                    return result[0]
                else:
                    return GetRotation()
                
    except OSError as exception:
        raise


