import RPi.GPIO as GPIO
import time

servoPIN2 = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN2, GPIO.OUT)

p2 = GPIO.PWM(servoPIN2, 50) # GPIO 14 for PWM with 50Hz
p2.start(7.5) # Initialization
time.sleep(0.5)
""" p.ChangeDutyCycle(7.5)
time.sleep(0.5) """


def Move(position):
  try:
    print(position)
    if position == 'bent':
      p2.ChangeDutyCycle(7.5)
      time.sleep(0.5)
    else:
      p2.ChangeDutyCycle(12.5)
      time.sleep(0.5)
  except KeyboardInterrupt:
    p.stop()
    p2.stop()
    GPIO.cleanup()



Move('str')
time.sleep(1)
""" Move('str')
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
Move('str') """