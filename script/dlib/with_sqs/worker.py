import base64
import json
import io
from random import randint
import time

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
sqs = boto3.resource('sqs')

try:
    order_queue = sqs.get_queue_by_name(QueueName='robot_arm_order')
except:
    order_queue = sqs.create_queue(QueueName='robot_arm_order')
try:
    image_queue = sqs.get_queue_by_name(QueueName='robot_arm_image')
except:
    image_queue = sqs.create_queue(QueueName='robot_arm_image')


class Worker:
    order = ''
    current_point = [6, 6]

    def upload_image(self):
        """Publish Image To SQS"""
        print "Take Picture..."
        c = cv2.VideoCapture(0)
        r, img = c.read()
        print "Image Processing..."
        r = 200.0 / img.shape[1]
        dimension = (200, int(img.shape[0] * r))
        resized_img = cv2.resize(img, dimension, interpolation = cv2.INTER_AREA)
        body = base64.b64encode(resized_img)
        c.release()
        print ""
        print "Publish Image To SQS"
        response = image_queue.send_message(MessageBody=body)

    def get_order(self):
        """Get Amazon SQS Message"""
        print ""
        try:
            message = order_queue.receive_messages(
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
            response = order_queue.delete_messages(
                Entries=[
                    {
                        'Id':'1',
                        'ReceiptHandle': message[0].receipt_handle
                    },
                ]
            )

        except:
            print "======order======"
            print "None"
            print "======order======"


        if Worker.order:
            return response
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

        order = json.loads(Worker.order)

        for key, value in order.items():

            if key == "turn_right":
                print key, value
                Worker.current_point[0] = Worker.current_point[0] - value / float(1000)
                if Worker.current_point[0] < 2.5 or Worker.current_point[0] > 12:
                    print "Activate safety mode"
                    Worker.current_point[0] = 6
                servo4.ChangeDutyCycle(Worker.current_point[0])
            if key == "turn_left":
                print key, value
                Worker.current_point[0] = Worker.current_point[0] - value / float(1000)
                if Worker.current_point[0] < 2.5 or Worker.current_point[0] > 12:
                    print "Activate safety mode"
                    Worker.current_point[0] = 6
                servo4.ChangeDutyCycle(Worker.current_point[0])
            if key == "turn_top":
                print key, value
                Worker.current_point[1] = Worker.current_point[1] - value / float(1000)
                if Worker.current_point[1] < 2.5 or Worker.current_point[1] > 12:
                    print "Activate safety mode"
                    Worker.current_point[1] = 6
                print "Worker throw a dice!"
                dice = randint(1, 3)
                if dice == 1:
                    servo1.ChangeDutyCycle(Worker.current_point[1])
                elif dice == 2:
                    servo2.ChangeDutyCycle(Worker.current_point[1])
                elif dice == 3:
                    servo3.ChangeDutyCycle(Worker.current_point[1])
            if key == "turn_bottom":
                print key, value
                Worker.current_point[1] = Worker.current_point[1] - value / float(1000)
                if Worker.current_point[1] < 2.5 or Worker.current_point[1] > 12:
                    print "Activate safety mode"
                    Worker.current_point[1] = 6
                print "Worker throw a dice!"
                dice = randint(1, 3)
                if dice == 1:
                    servo1.ChangeDutyCycle(Worker.current_point[1])
                elif dice == 2:
                    servo2.ChangeDutyCycle(Worker.current_point[1])
                elif dice == 3:
                    servo3.ChangeDutyCycle(Worker.current_point[1])

        Worker.order = ''
        print "Current point is"
        print Worker.current_point[0], Worker.current_point[1]
        print "=====Servo Motor Turn Off.====="
        print "=====Control Servo Process Ended.====="
        print ""
        print "Go Back to The Loop Top"
        print ""


if __name__ == "__main__":
    worker = Worker()
    while True:
        worker.upload_image()
        if worker.get_order():
            worker.control_servo()
