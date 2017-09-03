import cv2
from random import randint


while True:
    capture_image = "capture.jpg"
    print "Take Picture..."
    c = cv2.VideoCapture(1)
    r, img = c.read()
    print "Image Processing..."
    r = 500.0 / img.shape[1]
    dimension = (500, int(img.shape[0] * r))
    resized_img = cv2.resize(img, dimension, interpolation=cv2.INTER_AREA)
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    img = cv2.imwrite('./train_data/test_' + str(randint(1, 10000)) + '.jpg', resized_img, encode_param)
    c.release()
