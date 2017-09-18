import time
import json
import io
from random import randint

import boto3
import cv2
import RPi.GPIO as GPIO


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

PIN = 23
GPIO.setup(PIN, GPIO.OUT)
servo_turn_table = GPIO.PWM(PIN, 50)

PIN = 24
GPIO.setup(PIN, GPIO.OUT)
servo_second = GPIO.PWM(PIN, 50)

PIN = 25
GPIO.setup(PIN, GPIO.OUT)
servo_third = GPIO.PWM(PIN, 50)

PIN = 8
GPIO.setup(PIN, GPIO.OUT)
servo_fourth = GPIO.PWM(PIN, 50)

PIN = 26
GPIO.setup(PIN, GPIO.OUT)
servo_bucket = GPIO.PWM(PIN, 50)

val = [2.5, 3.6875, 4.875, 6.0625, 7.25, 8.4375, 9.625, 10.8125, 12]

bucket_name = "bento-robot"
capture_image = "capture.jpg"
sqs = boto3.resource('sqs')
s3 = boto3.resource('s3')

order_queue = sqs.get_queue_by_name(QueueName='robot_arm_order')
image_queue = sqs.get_queue_by_name(QueueName='robot_arm_image')


class Worker:
    """Working on Rasbperry Pi3."""
    order = ''
    current_point = [6, 6]

    def upload_image(self):
        """Upload Image To S3."""
        print "Take Picture..."
        c = cv2.VideoCapture(0)
        r, img = c.read()
        print "Image Processing..."
        r = 500.0 / img.shape[1]
        dimension = (500, int(img.shape[0] * r))
        resized_img = cv2.resize(img, dimension, interpolation = cv2.INTER_AREA)
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        result, img = cv2.imencode('.jpg', resized_img, encode_param)
        c.release()
        print ""
        print "Upload Image To S3"
        img = io.BytesIO(img)
        response = s3.Bucket(bucket_name).upload_fileobj(img, capture_image)

    def get_order(self):
        """Get Amazon SQS Message."""
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
        """Control Servo it subject to Amazon SQS orders."""
        print ""
        print "=====Control Servo Process Start.====="
        print ""
        servo_turn_table.start(0.0)
        servo_second.start(0.0)
        servo_third.start(0.0)
        servo_fourth.start(0.0)
        servo_bucket.start(0.0)

        order = json.loads(Worker.order)

        for key, value in order.items():

            if key == "turn_right":
                print key, value
                Worker.current_point[0] = Worker.current_point[0] - value / float(1000)
                if Worker.current_point[0] < 2.5 or Worker.current_point[0] > 12:
                    print "Activate safety mode"
                    Worker.current_point[0] = 6
                servo_turn_table.ChangeDutyCycle(Worker.current_point[0])
            if key == "turn_left":
                print key, value
                Worker.current_point[0] = Worker.current_point[0] - value / float(1000)
                if Worker.current_point[0] < 2.5 or Worker.current_point[0] > 12:
                    print "Activate safety mode"
                    Worker.current_point[0] = 6
                servo_turn_table.ChangeDutyCycle(Worker.current_point[0])
            if key == "turn_top":
                print key, value
                Worker.current_point[1] = Worker.current_point[1] - value / float(1000)
                if Worker.current_point[1] < 2.5 or Worker.current_point[1] > 12:
                    print "Activate safety mode"
                    Worker.current_point[1] = 6
                print "Worker throw a dice!"
                dice = randint(1, 3)
                if dice == 1:
                    servo_second.ChangeDutyCycle(Worker.current_point[1])
                elif dice == 2:
                    servo_third.ChangeDutyCycle(Worker.current_point[1])
                elif dice == 3:
                    servo_fourth.ChangeDutyCycle(Worker.current_point[1])
            if key == "turn_bottom":
                print key, value
                Worker.current_point[1] = Worker.current_point[1] - value / float(1000)
                if Worker.current_point[1] < 2.5 or Worker.current_point[1] > 12:
                    print "Activate safety mode"
                    Worker.current_point[1] = 6
                print "Worker throw a dice!"
                dice = randint(1, 3)
                if dice == 1:
                    servo_second.ChangeDutyCycle(Worker.current_point[1])
                elif dice == 2:
                    servo_third.ChangeDutyCycle(Worker.current_point[1])
                elif dice == 3:
                    servo_fourth.ChangeDutyCycle(Worker.current_point[1])

        print "glab a object"
        servo_bucket.ChangeDutyCycle(val[3])
        time.sleep(1)
        servo_bucket.ChangeDutyCycle(val[0])

        print "bring desired point"
        time.sleep(1)
        servo_second.ChangeDutyCycle(val[1])
        servo_turn_table.ChangeDutyCycle(val[0])

        print "then release a object.Done"
        servo_bucket.ChangeDutyCycle(val[3])

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
