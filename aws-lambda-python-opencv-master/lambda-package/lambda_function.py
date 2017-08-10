import boto3
import cv2


s3 = boto3.resource('s3')
sqs = boto3.resource('sqs')
queue_name = 'robot_arm'

try:
    queue = sqs.get_queue_by_name(QueueName=queue_name)
except:
    queue = sqs.create_queue(QueueName=queue_name)


def lambda_handler(event, context):
    s3.Bucket('bento-robot').download_file('capture.jpg', '/tmp/capture.jpg')
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    img = cv2.imread('/tmp/capture.jpg')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    height = img.shape[0]
    width = img.shape[1]
    frame_top = height/4
    frame_left = width/4
    frame_right = width - width/4
    frame_bottom = height - height/4
    order = "order="

    for (x, y, w, h) in faces:
        # cv2.rectangle(image,(top-left point),(bottom-right point),(color),bold line)
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    if x < frame_left:
        order += "turn right!, "
    if x + w > frame_right:
        order += "turn left!, "
    if y < frame_top:
        order += "turn bottom!, "
    if y + h > frame_bottom:
        order += "turn top!"

    response = queue.send_message(MessageBody=order)

    return response
