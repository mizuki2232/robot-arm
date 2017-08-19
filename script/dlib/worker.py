import json
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
bucket_name = "bento-robot"
s3 = boto3.resoure('s3')
sqs = boto3.resource('sqs')

try:
    order_queue = sqs.get_queue_by_name(QueueName='robot_arm_order')
except:
    order_queue = sqs.create_queue(QueueName='robot_arm_order')


class Worker:
    order = ''
    current_point = [6, 2]

    def publish_queue(self):
        """Publish Queue"""
        print "Take Picture..."
        c = cv2.VideoCapture(0)
        r, img = c.read()
        print "Image Processing..."
        r = 300.0 / img.shape[1]
        dimension = (300, int(img.shape[0] * r))
        resized_img = cv2.resize(img, dimension, interpolation = cv2.INTER_AREA)
        encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
        result, img = cv2.imencode('.jpg', resized_img, encode_param)
        c.release()
        print ""
        print "Upload Image To S3"
        s3.Bucket(bucket_name).upload_file(img, capture_image)
        print response

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
                WaitTimeSeconds=10,
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

        order = json.loads(Worker.order)

        for key, value in order.items():

            if key == "turn_right":
                print key, value
                Worker.current_point[0] = Worker.current_point[0] - value / float(1000)
                if Worker.current_point[0] < 2.5 or Worker.current_point[0] > 12:
                    Worker.current_point[0] = 6
                servo4.ChangeDutyCycle(Worker.current_point[0])
            if key == "turn_left":
                print key, value
                Worker.current_point[0] = Worker.current_point[0] - value / float(1000)
                if Worker.current_point[0] < 2.5 or Worker.current_point[0] > 12:
                    Worker.current_point[0] = 6
                servo4.ChangeDutyCycle(Worker.current_point[0])
            if key == "turn_top":
                print key, value
                Worker.current_point[1] = Worker.current_point[1] - value / float(1000)
                if Worker.current_point[1] < 2.5 or Worker.current_point[1] > 12:
                    Worker.current_point[1] = 2
                servo1.ChangeDutyCycle(Worker.current_point[0])
            if key == "turn_bottom":
                print key, value
                Worker.current_point[1] = Worker.current_point[1] - value / float(1000)
                if Worker.current_point[1] < 2.5 or Worker.current_point[1] > 12:
                    Worker.current_point[1] = 2
                servo1.ChangeDutyCycle(Worker.current_point[1])

        Worker.order = ''
        print "Current point is"
        print Worker.current_point[0], Worker.current_point[1]
        time.sleep(1)
        print "=====Servo Motor Turn Off.====="
        print "=====Control Servo Process Ended.====="
        print ""
        print "Go Back to The Loop Top"
        print ""


if __name__ == "__main__":
    while True:
        Worker().publish_queue()
        if Worker().get_order():
            Worker().control_servo()
        else:
            continue
