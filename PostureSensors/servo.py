import RPi.GPIO as GPIO
import time

servoPIN = 10
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
p.start(7.5) # Initialization
time.sleep(0.5)
p.ChangeDutyCycle(7.5)
time.sleep(0.5)

def Move(position):
  try:
    print(position)
    if position == 'bent':
      p.ChangeDutyCycle(10)
      time.sleep(0.5)
    else:
      p.ChangeDutyCycle(7.5)
      time.sleep(0.5)
  except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()