#Libraries
import RPi.GPIO as GPIO
import time
import pitch
import exporttocsv
import datetime
import numpy as np
import servo

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.IN)

ALLOWANCE = 8

HEADER = ['Id', 'Upper_Sensor', 'Lower_Sensor', 'Pitch', 'Toy', 'Timestamp']
currentPosture = ''
previousPosture = ''
beforePreviousPosture = ''
toy = ''

def distance(trigger, echo):
    # set Trigger to HIGH
    GPIO.output(trigger, True)
    
    # set Trigger after 0.01ms to LOW
    time.sleep(0.1)
    GPIO.output(trigger, False)
    

    StartTime = time.time()
    StopTime = time.time()
    
    counter = 0
    # save StartTime
    while GPIO.input(echo) == 0:
        StartTime = time.time()
        #counter = counter + 1
        #if counter == 100000:
         #   break
        
    
 
    # save time of arrival
    counter = 0
    while GPIO.input(echo) == 1:
        StopTime = time.time()
        #counter = counter + 1
        #if counter == 100000:
        #    break
    
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    #if distance > 100:
    #print (datetime.datetime.utcfromtimestamp(StopTime))
    #print(datetime.datetime.utcfromtimestamp(StartTime))
 
    return distance
 
if __name__ == '__main__':
    try:
        #GPIO.output(GPIO_TRIGGER, True)
        #GPIO.output(17, True)
        #time.sleep(0.00001)

        #GPIO.output(GPIO_TRIGGER, False)
        #GPIO.output(17, False)
        #print("Waiting For Sensor To Settle")
        #time.sleep(2)

        exporttocsv.WriteHeaderRow(HEADER)

        count = 0
        rows = []

        while True:
            count = count + 1

            lower = distance(18, 24) #lower
            #print ("Measured Distance 1 = %.1f cm" % lower)
            time.sleep(0.1)

            upper = distance(17, 27) #upper
            if upper > 100:
                time.sleep(0.01)
                upper = distance(17, 27) #upper
            #print ("Measured Distance 2 = %.1f cm" % upper)


            #find pitch from microbit gyroscope
            pitchStr = pitch.GetPitch()
            #print(pitchStr)
            ##print(len(pitch.GetPitch()))
            
            #find the delta
            delta = upper - lower
            if upper > 100 and lower > 100:
                currentPosture = 'straight'  #too close to both sensors
            elif upper > 100:
                currentPosture = previousPosture 
            elif delta - ALLOWANCE > 0:
                currentPosture = 'bent'
                #print("currentPosture bend")
            else:
                currentPosture = 'straight'
                #print("currentPosture straighten")

            #check last 3 readings before moving
            if currentPosture == previousPosture and currentPosture == beforePreviousPosture and currentPosture != toy:
                servo.Move(currentPosture)
            
            toy = beforePreviousPosture
            beforePreviousPosture = previousPosture
            previousPosture = currentPosture

            #log into csv
            row = [count, upper, lower, pitchStr, currentPosture, datetime.datetime.now().strftime('%m-%d-%Y_%H.%M.%S')]
            
            
            if len(rows) == 0:
                rows = row
            else:
                rows = np.vstack([rows, row])

            print(row)
            #print(len(rows))
            
            if count % 10 == 0:
                exporttocsv.WriteRows(rows)
                rows = []

            time.sleep(3)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        #print("Measurement stopped by User")
        GPIO.cleanup()