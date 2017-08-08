import time
import sys


import boto3
import cv2
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)

PIN = 23
GPIO.setup(PIN, GPIO.OUT)
servo1 = GPIO.PWM(PIN, 50)

PIN = 24
GPIO.setup(PIN, GPIO.OUT)
servo2 = GPIO.PWM(PIN, 50)

PIN = 25
GPIO.setup(PIN, GPIO.OUT)
servo3 = GPIO.PWM(PIN, 50)


PIN = 8
GPIO.setup(PIN, GPIO.OUT)
servo4 = GPIO.PWM(PIN, 50)

val = [2.5,3.6875,4.875,6.0625,7.25,8.4375,9.625,10.8125,12]


capture_image = "test.png"
bucket_name = "bento_robot"
s3 = boto3.resource('s3')


class worker():
    def upload_image():
        """Capture image, then upload image to Amazon s3."""
        print "take picture..."
        c = cv2.VideoCapture(0)
        r, img = c.read()
        cv2.imwrite('./' + capture_image, img)
        c.release()
        print "uploading to S3..."
        s3.Bucket(bucket_name).upload_file('./' + capture_image, capture_image)

        time.sleep(10)

    def check_order():
        """check Amazon sqs queue"""
        # check sqs job
        #if job in queue
        if 1 """sqs has order""" == True:
            order1 = 1
            order2 = 1
            order3 = 1
            order4 = 1
            time.sleep(3)
            return True

    def control_servo():
        """Control Servo it subject to sqs orders"""
        servo1.start(0.0)
        servo2.start(0.0)
        servo3.start(0.0)
        servo4.start(0.0)

        servo1.ChangeDutyCycle(val[check_order.order1])
        time.sleep(0.3)
        servo2.ChangeDutyCycle(val[check_order.order2])
        time.sleep(0.3)
        servo3.ChangeDutyCycle(val[check_order.order3])
        time.sleep(0.3)
        servo4.ChangeDutyCycle(val[check_order.order4])
        time.sleep(0.3)


while True:
    worker.upload_image()
    while True:
        if worker.check_order() == True:
            worker.control_servo()
            break;
