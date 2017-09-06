import base64
import json
from random import randint
from io import BytesIO

import boto3
import cv2
import dlib
import numpy as np
from skimage import io


s3 = boto3.resource('s3')
sqs = boto3.resource('sqs')
queue_name = 'robot_arm'

image_queue = sqs.get_queue_by_name(QueueName='robot_arm_image')
order_queue = sqs.get_queue_by_name(QueueName='robot_arm_order')

order = {}


# test comment
# test comment
while True:
    try:
        message = image_queue.receive_messages(
            AttributeNames=[
                'All'
            ],
            MessageAttributeNames=[
                'string',
            ],
            WaitTimeSeconds=20,
            MaxNumberOfMessages=1
        )
        response = image_queue.delete_messages(
            Entries=[
                {
                    'Id': '1',
                    'ReceiptHandle': message[0].receipt_handle
                },
            ]
        )

        img_info = message[0].body
        forward = img_info.rfind('key')
        backward = img_info.rfind('.jpg')
        img_name = img_info[forward+6:backward+4]
        img = BytesIO()
        s3.Bucket('bento-robot').download_fileobj(img_name, img)
        img = io.imread(img)
        detector = dlib.simple_object_detector("./train/circle_chip_detector.svm")
        dets = detector(img, 1)
        print ("Number of faces detected: {}".format(len(dets)))
        if len(dets) > 0:
            try:
                for i, d in enumerate(dets):
                    print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
                        i, d.left(), d.top(), d.right(), d.bottom()))

                    obj_center_x = d.left() + d.right() / 2
                    obj_center_y = d.top() + d.bottom() / 2
                height = img.shape[0] width = img.shape[1]img_center_x = width / 2
                img_center_y = height / 2

                x_distance = img_center_x - obj_center_x
                y_distance = img_center_y - obj_center_y

                if x_distance > 0:
                    order = {"turn_left": x_distance}
                if x_distance < 0:
                    order = {"turn_right": abs(x_distance)}
                if y_distance > 0:
                    order = {"turn_top": y_distance}
                if y_distance > 0:
                    order = {"turn_bottom": abs(y_distance)}

                if obj_center_x:
                    body = json.dumps(order)
                    response = order_queue.send_message(MessageBody=body)

            except:
                print "Processing section failed"
#        else:
#            print "Boss throw a dice!"
#            dice = randint(1, 4)
#            if dice == 1:
#                order = {"turn_left": randint(100, 1000)}
#            elif dice == 2:
#                order = {"turn_right": randint(100, 1000)}
#            elif dice == 3:
#                order = {"turn_top": randint(100, 1000)}
#            elif dice == 4:
#                order = {"turn_bottom": randint(100, 1000)}
#            print order
#            body = json.dumps(order)
#            response = order_queue.send_message(MessageBody=body)

    except (KeyboardInterrupt, SystemExit):
        raise

    except:
        print "Back To The Loop Top"
