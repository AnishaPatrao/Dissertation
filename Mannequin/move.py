#!/usr/bin/python3
import RPi.GPIO as GPIO
import pigpio
import time
 
servoPIN1 = 10
servoPIN2 = 19
 
# more info at http://abyz.me.uk/rpi/pigpio/python.html#set_servo_pulsewidth
 
pwm = pigpio.pi() 
pwm.set_mode(servoPIN1, pigpio.OUTPUT)
pwm.set_mode(servoPIN2, pigpio.OUTPUT)
 
pwm.set_PWM_frequency( servoPIN1, 50 )
pwm.set_PWM_frequency( servoPIN2, 50 )
 
def Move(position):
  try:
    print(position)
    if position == 'bent':
        pwm.set_servo_pulsewidth( servoPIN1, 750 ) 
        pwm.set_servo_pulsewidth( servoPIN2, 1500 ) 
        time.sleep(0.5)
    
    else:
        print( "90 deg" )
        pwm.set_servo_pulsewidth( servoPIN1, 1500 ) 
        pwm.set_servo_pulsewidth( servoPIN2, 2500 ) 
        time.sleep(0.5)
  except KeyboardInterrupt:
    pwm.set_PWM_dutycycle(servoPIN1, 0)
    pwm.set_PWM_frequency( servoPIN1, 0 )

    pwm.set_PWM_dutycycle(servoPIN2, 0)
    pwm.set_PWM_frequency( servoPIN2, 0 )

#Move('str')