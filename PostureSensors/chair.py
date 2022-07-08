#Libraries
import RPi.GPIO as GPIO
import time
import pitch

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

ALLOWANCE = 5

def distance(trigger, echo):
    # set Trigger to HIGH
    GPIO.output(trigger, True)
    
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(trigger, False)
    

    StartTime = time.time()
    StopTime = time.time()
    
    counter = 0
    # save StartTime
    while GPIO.input(echo) == 0:
        StartTime = time.time()
        counter = counter + 1
        if counter == 100000:
            break
        
    
 
    # save time of arrival
    counter = 0
    while GPIO.input(echo) == 1:
        StopTime = time.time()
        counter = counter + 1
        if counter == 100000:
            break
    
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 
if __name__ == '__main__':
    try:
        GPIO.output(GPIO_TRIGGER, False)
        GPIO.output(17, False)
        print("Waiting For Sensor To Settle")
        time.sleep(2)
        while True:
            lower = distance(18, 24) #lower
            print ("Measured Distance 1 = %.1f cm" % lower)

            upper = distance(17, 27) #upper
            print ("Measured Distance 2 = %.1f cm" % upper)


            #find pitch from microbit gyroscope
            print(pitch.GetPitch())
            #print(len(pitch.GetPitch()))
            
            #find the delta
            delta = upper - lower
            if delta - ALLOWANCE > 0:
                print("toy bend")
            else:
                print("toy straighten")

            time.sleep(5)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()