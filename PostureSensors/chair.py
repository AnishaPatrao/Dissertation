#Libraries
import RPi.GPIO as GPIO
import time
import rotation
import exporttocsv
import datetime
import numpy as np
import servo
import medianFilter
#import client
import threading
import socketio

#sio = socketio.Client()


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

SENSOR_READING_LIMIT = 20
SEND_READING_LIMIT = 40

def saveReadings(readings, currentReading, readingLimit):
    if len(readings) >= readingLimit:
        readings = np.delete(readings, 0)
    return np.concatenate((readings, [currentReading]))

def distance(trigger, echo):
    # set Trigger to HIGH
    GPIO.output(trigger, True)
    
    # set Trigger after 0.01ms to LOW
    time.sleep(0.01)
    GPIO.output(trigger, False)
    

    StartTime = time.time()
    StopTime = time.time()
    
    counter = 0
    # save StartTime
    while GPIO.input(echo) == 0:
        StartTime = time.time()
        counter = counter + 1
        if counter == 100000:
            print('loop')
            break
        
    
 
    # save time of arrival
    counter = 0
    while GPIO.input(echo) == 1:
        StopTime = time.time()
        counter = counter + 1
        if counter == 100000:
            print('loop')
            break
    
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    #if distance > 100:
    #print (datetime.datetime.utcfromtimestamp(StopTime))
    #print(datetime.datetime.utcfromtimestamp(StartTime))
 
    return distance


def StartSensors():

    ALLOWANCE = 5

    HEADER = ['Id', 'Upper_Sensor', 'Lower_Sensor', 'Rotation', 'Difference', 'Posture', 'Timestamp']
    currentPosture = ''
    previousPosture = ''
    beforePreviousPosture = ''
    toy = ''
    upperReadings = []
    lowerReadings = []
    rotationReadings = []
    sendReadings = []


    exporttocsv.WriteHeaderRow(HEADER)

    count = 0
    rows = []

    thoracicBend = False
    lumbarBend = False

    while True:
        count = count + 1

        lower = distance(18, 24) #lower
        #print ("Measured Distance 1 = %.1f cm" % lower)
        time.sleep(0.01)

        upper = distance(17, 27) #upper
        if upper > 100:
            time.sleep(0.01)
            upper = distance(17, 27) #upper
        #print ("Measured Distance 2 = %.1f cm" % upper)


        #find rotation from microbit gyroscope
        rotationStr = rotation.GetRotation()
        if rotationStr > -60:
            ALLOWANCE = 6
        else:
            ALLOWANCE = 8
        #print(rotationStr)
        ##print(len(rotation.GetPitch()))

        #store latest 10 readings
        upperReadings = saveReadings(upperReadings, upper, SENSOR_READING_LIMIT)
        #print(upperReadings)

        lowerReadings = saveReadings(lowerReadings, lower, SENSOR_READING_LIMIT)
        #print(lowerReadings)

        rotationReadings = saveReadings(rotationReadings, rotationStr, SENSOR_READING_LIMIT)


        #find mediam of readings
        upper = medianFilter.median(upperReadings)
        lower = medianFilter.median(lowerReadings)
        rotationStr = medianFilter.median(rotationReadings)
        
        #find the delta
        delta = upper - lower
        """ if upper > 100 and lower > 100:
            currentPosture = 'straight'  #too close to both sensors
        elif upper > 100:
            currentPosture = previousPosture 
        elif delta - ALLOWANCE > 0:
            currentPosture = 'bent'
            #print("currentPosture bend")
        else:
            currentPosture = 'straight' """

        #24+-5 degree of thoracic flexion is allowable for upright to intermediate posture. anthing more is a slump
        if rotationStr <= 61:
            thoracicBend = True
        else:
            thoracicBend = False

        if upper > 15 or lower > 8:
            lumbarBend = True
        else:
            lumbarBend = False

        if thoracicBend or lumbarBend:
            currentPosture = 'bent'
        else:
            currentPosture = 'straight'
            #print("currentPosture straighten")

        #check last 3 readings before moving
        #if currentPosture == previousPosture and currentPosture == beforePreviousPosture and currentPosture != toy:
        #if currentPosture != previousPosture:

            #servo.Move(currentPosture)
            #server.sendServo()
        sendReadings = saveReadings(sendReadings, currentPosture, SEND_READING_LIMIT)
        #print(sendReadings)
        toSend = medianFilter.median(sendReadings)
        #print(toSend)
            
        if len(sendReadings) >= SEND_READING_LIMIT and toSend != previousPosture:
            print(currentPosture)
            print(len(sendReadings))
            previousPosture = toSend
            #client.SendPosture(toSend)

            """ lock = threading.Lock()
            th = threading.Thread(target = client.SendPosture(toSend))
            with lock:
                th.start() """
        
        #toy = beforePreviousPosture
        #beforePreviousPosture = previousPosture
        """ previousPosture = currentPosture
        prevPosture = previousPosture """

        #log into csv
        row = [count, upper, lower, rotationStr, delta, currentPosture, datetime.datetime.now().strftime('%m-%d-%Y_%H.%M.%S')]
        
        
        if len(rows) == 0:
            rows = row
        else:
            rows = np.vstack([rows, row])

        print(row)
        #print(len(rows))
        
        if count % 30 == 0:
            exporttocsv.WriteRows(rows)
            rows = []

        time.sleep(0.1)
 
#if __name__ == '__main__':
try:
    #GPIO.output(GPIO_TRIGGER, True)
    #GPIO.output(17, True)
    #time.sleep(0.00001)

    #GPIO.output(GPIO_TRIGGER, False)
    #GPIO.output(17, False)
    #print("Waiting For Sensor To Settle")
    #time.sleep(2)
    
    #sio.connect('ws://raspberrypi2.local:5000')
    StartSensors()

    """ lock = threading.Lock()
    th = threading.Thread(target = )
    with lock:
        th.start() """
    """ while True:
        client.SendPosture(changeMannequin)
     """
    
    # Reset by pressing CTRL + C
except KeyboardInterrupt:
    #print("Measurement stopped by User")
    GPIO.cleanup()



    