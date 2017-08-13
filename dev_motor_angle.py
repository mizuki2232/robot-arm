#!/usr/bin/python
# coding: utf-8 

import RPi.GPIO as GPIO
import time
import sys 


GPIO.setmode(GPIO.BCM)


PIN = 23
GPIO.setup(PIN, GPIO.OUT)
servo = GPIO.PWM(PIN, 50)

PIN = 24
GPIO.setup(PIN, GPIO.OUT)
servo1 = GPIO.PWM(PIN, 50)

PIN = 25
GPIO.setup(PIN, GPIO.OUT)
servo2 = GPIO.PWM(PIN, 50)


PIN = 8
GPIO.setup(PIN, GPIO.OUT)
servo3 = GPIO.PWM(PIN, 50)

val = [2.5,3.6875,4.875,6.0625,7.25,8.4375,9.625,10.8125,12]


if __name__ == '__main__':
    try:
        servo.start(0.0)
        servo1.start(0.0)
        servo2.start(0.0)
        servo3.start(0.0)

        servo.ChangeDutyCycle(val[0])
        time.sleep(1)
        servo.ChangeDutyCycle(val[0] + 0.1)
        time.sleep(1)
        servo.ChangeDutyCycle(val[0] + 0.3)
        time.sleep(1)
        servo.ChangeDutyCycle(val[0] + 0.5)
        time.sleep(1)
        servo.ChangeDutyCycle(val[0] + 1)
        time.sleep(1)
        servo.ChangeDutyCycle(val[0])
        time.sleep(1)
    except KeyboardInterrupt:
        pass

time.sleep(1.5)
servo.stop()
GPIO.cleanup()
