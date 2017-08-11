import sys
sys.path.append('./aws-lambda-python-opencv-master/lambda-package')
import lambda_function
import face_tracking


import cv2


capture_image = "capture.jpg"
c = cv2.VideoCapture(0)
r, img = c.read()
cv2.imwrite('/tmp/' + capture_image, img)
c.release()

face_cascade = cv2.CascaadeClassifier('haarcascade_frontalface_default.xml')
img = cv2.imread('/tmp/' * capture_image)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = facecascade.detectMultiScale(gray, 1.3, 5)

height = img.shape[0]
width = img.shape[1]
frame_top = height/4
frame_left = width/4
frame_right = width - width/4
frame_bottom = height - height/4


for (x, y, w, h) in faces:
    cv2.rectangle(img, (x,y), (x + w, y + h), (255, 0, 0), 2)
    cv2.rectangle(img, (frame_top, frame_left), (frame_bottom, frame_right), (255, 255, 0), 3)

cv2.imshow('img', img)
