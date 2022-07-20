import RPi.GPIO as GPIO
import time

servoPIN1 = 10
servoPIN2 = 19
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN1, GPIO.OUT)
GPIO.setup(servoPIN2, GPIO.OUT)

p = GPIO.PWM(servoPIN1, 50) # GPIO 10 for PWM with 50Hz
p2 = GPIO.PWM(servoPIN2, 50) # GPIO 14 for PWM with 50Hz
p.start(7.5) # Initialization
p2.start(12.5) # Initialization
time.sleep(2.5)
""" p.ChangeDutyCycle(7.5)
time.sleep(0.5) """


def Move(position):
  try:
    print(position)
    if position == 'bent':
      p.ChangeDutyCycle(2.5)
      p2.ChangeDutyCycle(7.5)
      time.sleep(0.5)
    else:
      p.ChangeDutyCycle(7.5)
      p2.ChangeDutyCycle(12.5)
      time.sleep(0.5)
  except KeyboardInterrupt:
    p.stop()
    p2.stop()
    GPIO.cleanup()


""" 
Move('bent')
time.sleep(1)
Move('str')
time.sleep(1)
Move('bent')
time.sleep(1)
Move('str')
time.sleep(1)
Move('bent')
time.sleep(1)
Move('str')
time.sleep(1)
Move('bent')
time.sleep(1)
Move('str')
time.sleep(1)
Move('bent')
time.sleep(1)
Move('str')
time.sleep(1)
Move('bent')
time.sleep(1)
Move('str')   """