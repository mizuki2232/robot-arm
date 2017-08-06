import boto3
import cv2


s3 = boto3.resource('s3')


def lambda_handler(event, context):
    s3.Bucket('bento-robot').download_file('girl_laugh_face.jpg', '/tmp/test.jpg')
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    img = cv2.imread('/tmp/test.jpg')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

    cv2.imwrite('/tmp/modified.jpg', img)
    data = open('/tmp/modified.jpg', 'rb')
    s3.Bucket('bento-robot').put_object('girl_laugh_face_modifie.jpg', data)

    return "It works!"
