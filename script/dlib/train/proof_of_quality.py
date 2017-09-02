import base64
from io import BytesIO
import json
from random import randint

import boto3
import cv2
import numpy as np
from  skimage import io


proof_image = "proof.jpg"
bucket_name = "bento-robot"
s3 = boto3.resource('s3')
sqs = boto3.resource('sqs')
queue_name = 'robot_arm'
order = {}


try:
    image_queue = sqs.get_queue_by_name(QueueName='robot_arm_image')
except:
    image_queue = sqs.create_queue(QueueName='robot_arm_image')

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

        # debug point
        print message[0].body
        img = base64.b64decode(message[0].body)
        # debug point
#        print type(img)
        img = np.fromstring(img, dtype=int)
        r, img = cv2.imencode('.jpg', img)
        img = BytesIO(img)
        response = s3.Bucket(bucket_name).upload_fileobj(img, proof_image)
        print "Uploaded decode image to S3"

    except (KeyboardInterrupt, SystemExit):
        raise
#     except:
#         print "Back To The Loop Top"
