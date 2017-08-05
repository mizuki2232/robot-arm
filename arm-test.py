#!/usr/bin/python
# coding: utf-8 

import RPi.GPIO as GPIO
import time
import sys 


PIN = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.OUT)
servo = GPIO.PWM(PIN, 50)

val = [2.5,3.6875,4.875,6.0625,7.25,8.4375,9.625,10.8125,12]


if __name__ == '__main__':
    try:
        servo.start(0.0)

        servo.ChangeDutyCycle(val[0])
        print("servo.ChangeDutyCycle(val[0])")
        time.sleep(1)
        servo.ChangeDutyCycle(val[8])
        print("servo.ChangeDutyCycle(val[8])")
 	print(val[8])
        time.sleep(1)
        servo.ChangeDutyCycle(val[0])
        print("servo.ChangeDutyCycle(val[0])")
        time.sleep(1)

        servo.ChangeDutyCycle(val[8])
        print("servo.ChangeDutyCycle(val[8])")
 	print(val[8])
        time.sleep(1)
        servo.ChangeDutyCycle(val[0])
        print("servo.ChangeDutyCycle(val[0])")
        time.sleep(1)

        servo.ChangeDutyCycle(val[8])
        print("servo.ChangeDutyCycle(val[8])")
 	print(val[8])
        time.sleep(1)
        servo.ChangeDutyCycle(val[0])
        print("servo.ChangeDutyCycle(val[0])")
        time.sleep(1)


        servo.ChangeDutyCycle(val[8])
        print("servo.ChangeDutyCycle(val[8])")
 	print(val[8])
        time.sleep(1)
        servo.ChangeDutyCycle(val[0])
        print("servo.ChangeDutyCycle(val[0])")
        time.sleep(1)


       # while True:
       # while True:

       # while True:

       # while True:
       #     for i, dc in enumerate(val):
       #         servo.ChangeDutyCycle(dc)
       #         print("Angle:" + str(i*22.5)+"  dc = %.4f" % dc) 
       #         time.sleep(0.5)
       #     for i, dc in enumerate( reversed(val) ):
       #         servo.ChangeDutyCycle(dc)
       #         print("Angle:" + str(180 - i*22.5)+"  dc = %.4f" % dc) 
       #         time.sleep(0.5)

    except KeyboardInterrupt:
        pass

time.sleep(1.5)
servo.stop()
GPIO.cleanup()
