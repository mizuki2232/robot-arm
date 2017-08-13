import cv2
import sys


while True:
    capture_image = "capture.jpg"
    c = cv2.VideoCapture(0)
    r, img = c.read()
    cv2.imwrite('/tmp/' + capture_image, img)
    c.release()

    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    img = cv2.imread('/tmp/' + capture_image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    height = img.shape[0]
    width = img.shape[1]
    frame_top = height/4
    frame_left = width/4
    frame_right = width - width/4
    frame_bottom = height - height/4
    order = ''
    flag = False

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x,y), (x + w, y + h), (255, 0, 0), 2)
        cv2.rectangle(img, (frame_left, frame_top), (frame_right, frame_bottom), (255, 255, 0), 3)


        if x < frame_left:
            order += "turn right!, "
        if x + w > frame_right:
            order += "turn left!, "
        if y < frame_top:
            order += "turn bottom!, "
        if y + h > frame_bottom:
            order += "turn top!"

    if "turn top" in order:
        print "turn top"
    if "turn right"in order:
        print "turn right"
    if "turn left" in order:
        print "turn left"
    if "turn bottom" in order:
        print "turn bottom"

    if "turn" in order:
        flag = True
        cv2.imwrite('./' + capture_image, img)

        print "========================="
        print order
        print "========================="

    if flag == True:
        break
