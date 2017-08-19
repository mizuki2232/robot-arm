import base64
import sys

import boto3
import dlib
import json
from skimage import io


s3 = boto3.resource('s3')
sqs = boto3.resource('sqs')
queue_name = 'robot_arm'
image_file = 'capture.jpg'
order = {}

try:
    order_queue = sqs.get_queue_by_name(QueueName='robot_arm_order')
except:
    order_queue = sqs.create_queue(QueueName='robot_arm_order')

try:
    image_queue = sqs.get_queue_by_name(QueueName='robot_arm_image')
except:
    image_queue = sqs.create_queue(QueueName='robot_arm_image')

try:
    message = image_queue.receive_messages(
        AttributeNames=[
            'All'
        ],
        MessageAttributeNames=[
            'string',
        ],
        WaitTimeSeconds=10,
        MaxNumberOfMessages=1
    )
except:
    print None

try:
    encoded_img = message[0].body
    img = encoded_img.decode('base64')
    detector = dlib.get_frontal_face_detector()
    dets = detector(img, 1)
    print ("Number of faces detected: {}".format(len(dets)))

    for i, d in enumerate(dets):
        print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
            i, d.left(), d.top(), d.right(), d.bottom()))

        obj_center_x = d.left() + d.right() / 2
        obj_center_y = d.top() + d.bottom() / 2

    height = img.shape[0]
    width = img.shape[1]
    img_center_x = width / 2
    img_center_y = height / 2

    x_distance = img_center_x - obj_center_x
    y_distance = img_center_y - obj_center_y

    if x_distance > 0:
        order = {"turn_left" : x_distance}
    if x_distance < 0:
        order = {"turn_right" : abs(x_distance)}
    if y_distance > 0:
        order = {"turn_top" : y_distance}
    if y_distance > 0:
        order = {"turn_bottom" : abs(y_distance)}

    if obj_center_x:
        body = json.dumps(order)
        response = order_queue.send_message(MessageBody=body)
        print response
except:
    print "Nothing to do."
