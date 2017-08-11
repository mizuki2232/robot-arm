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

val = [2.5, 3.6875, 4.875, 6.0625, 7.25, 8.4375, 9.625, 10.8125, 12]


capture_image = "capture.jpg"
bucket_name = "bento-robot"
s3 = boto3.resource('s3')
sqs = boto3.resource('sqs')
queue_name = 'robot_arm'

try:
    queue = sqs.get_queue_by_name(QueueName=queue_name)
except:
    queue = sqs.create_queue(QueueName=queue_name)


class Worker:
    def upload_image(self):
        """Capture image, then upload image to Amazon s3."""
        print "take picture..."
        c = cv2.VideoCapture(0)
        r, img = c.read()
        cv2.imwrite('/tmp/' + capture_image, img)
        c.release()
        print "uploading to S3..."
        s3.Bucket(bucket_name).upload_file('/tmp/' + capture_image, capture_image)

    def get_order(self):
        """Get Amazon SQS Message."""
        order = False
        try:
            order = queue.receive_message()
            print "Receive Queue Message"
        except:
            pass

        if order == True:
            return True
        else:
            return False

    def control_servo(self):
        """Control Servo it subject to Amazon SQS orders"""
        print "Servo Motor Turn On."
        servo1.start(0.0)
        servo2.start(0.0)
        servo3.start(0.0)
        servo4.start(0.0)

        if get_order.order in "turn right":
            servo1.ChangeDutyCycle(val[0])
        if get_order.order in "turn left":
            servo1.ChangeDutyCycle(val[8])
        if get_order.order in "turn bottom":
            servo4.ChangeDutyCycle(val[0])
        if get_order.order in "turn top":
            servo4.ChangeDutyCycle(val[8])


while True:
    Worker().upload_image()
    time.sleep(1)
    if Worker().get_order() == True:
        Worker().control_servo()
    else:
        continue
