import boto3
import cv2
import json


s3 = boto3.resource('s3')
sqs = boto3.resource('sqs')
queue_name = 'robot_arm'
image_file = 'capture.jpg'
order = {}

try:
    queue = sqs.get_queue_by_name(QueueName=queue_name)
except:
    queue = sqs.create_queue(QueueName=queue_name)


def lambda_handler(event, context):
    s3.Bucket('bento-robot').download_file(image_file, '/tmp/' + image_file)
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    img = cv2.imread('/tmp/' + image_file)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    height = img.shape[0]
    width = img.shape[1]
    img_center_x = width / 2
    img_center_y = height / 2

    for (x, y, w, h) in faces:
        # cv2.rectangle(image,(top-left point),(bottom-right point),(color),bold line)
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        obj_center_x = x + w / 2
        obj_center_y = y + h / 2


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
        response = queue.send_message(MessageBody=body)
        return response
    else:
        return "Nothing to do."
