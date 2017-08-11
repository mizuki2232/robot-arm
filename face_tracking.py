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
    order = ''

    def upload_image(self):
        """Capture image, then upload image to Amazon s3."""
        print ""
        print "=====Upload Process Start. ====="
        print ""
        print "Take Picture..."
        c = cv2.VideoCapture(0)
        r, img = c.read()
        cv2.imwrite('/tmp/' + capture_image, img)
        c.release()
        print ""
        print ""
        print "Upload Image To S3."
        s3.Bucket(bucket_name).upload_file('/tmp/' + capture_image, capture_image)
        print "======Upload Process Ended.======"

    def get_order(self):
        """Get Amazon SQS Message"""
        print ""
        print "=====Get Queue Process Start. ====="
        print ""
        try:
            message = queue.receive_messages(
                AttributeNames=[
                    'All'
                ],
                MessageAttributeNames=[
                    'string',
                ],
                WaitTimeSeconds=20,
                MaxNumberOfMessages=1
            )

            Worker.order = message[0].body

            print ""
            print "======order======"
            print Worker.order
            print "======order======"
            print ""
            response = queue.delete_messages(
                Entries=[
                    {
                        'Id':'1',
                        'ReceiptHandle': message[0].receipt_handle
                    },
                ]    
            )
            print ""
            print "======delete queue======"
            print response
            print "======delete queue======"
            print ""
        except:
            Worker.order = False
            print ""
            print "======order======"
            print "None"
            print "======order======"
            print ""

        print ""
        print "======Get Queue Process Ended.======"
        print ""

        if Worker.order:
            return True
        else:
            return False

    def control_servo(self):
        """Control Servo it subject to Amazon SQS orders"""
        print ""
        print "=====Control Servo Process Start.====="
        print ""
        servo1.start(0.0)
        servo2.start(0.0)
        servo3.start(0.0)
        servo4.start(0.0)

        try:
            if Worker.order in "turn right":
                print "turn right."
                servo1.ChangeDutyCycle(val[0])
            if Worker.order in "turn left":
                print "turn left."
                servo1.ChangeDutyCycle(val[8])
            if Worker.order in "turn bottom":
                print "turn bottom."
                servo4.ChangeDutyCycle(val[0])
            if Worker.order in "turn top":
                print "turn top."
                servo4.ChangeDutyCycle(val[8])
        except:
            print "Something error occuered."

        print ""
        print "=====Servo Motor Turn Off.====="
        print ""
        print ""
        print "=====Control Servo Process Ended.====="
        print ""
        print "Go Back to The Loop Top"
        print ""


while True:
    Worker().upload_image()
    time.sleep(1)
    if Worker().get_order() == True:
        Worker().control_servo()
    else:
        continue
