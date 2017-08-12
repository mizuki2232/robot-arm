import cv2
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)

PIN = 23
GPIO.setup(PIN, GPIO.OUT)
servo1 = GPIO.PWM(PIN, 50)

PIN = 24
GPIO.setup(PIN, GPIO.OUT)
servo2 = GPIO.PWM(PIN, 50)

PIN = 25
GPIO.setup(PIN, GPIO.OUT)
servo3 = GPIO.PWM(PIN, 50)

PIN = 8
GPIO.setup(PIN, GPIO.OUT)
servo4 = GPIO.PWM(PIN, 50)

val = [2.5, 3.6875, 4.875, 6.0625, 7.25, 8.4375, 9.625, 10.8125, 12]


capture_image = "capture.jpg"


class Worker:
    order = ''

    def capture_image(self):
        print "Take Picture..."
        c = cv2.VideoCapture(0)
        r, img = c.read()
        cv2.imwrite('/tmp/' + capture_image, img)
        c.release()

    def make_order(self):
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        img = cv2.imread('/tmp/' + capture_image)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        height = img.shape[0]
        width = img.shape[1]
        frame_top = height/3
        frame_left = width/3
        frame_right = width - width/3
        frame_bottom = height - height/3
        Worker.order = "order="

        for (x, y, w, h) in faces:
            # cv2.rectangle(image,(top-left point),(bottom-right point),(color),bold line)
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

            if x < frame_left:
                Worker.order += "turn right!, "
            if x + w > frame_right:
                Worker.order += "turn left!, "
            if y < frame_top:
                Worker.order += "turn bottom!, "
            if y + h > frame_bottom:
                Worker.order += "turn top!"

        print ""
        print "=====order====="
        print Worker.order
        print "=====order====="

        if "turn" in Worker.order:
            return True

    def control_servo(self):
        """Control Servo it subject to Amazon SQS orders"""
        print ""
        print "=====Control Servo Process Start.====="
        print ""
        servo1.start(0.0)
        servo2.start(0.0)
        servo3.start(0.0)
        servo4.start(0.0)

	if "turn right" in Worker.order:
            print "turn right."
            servo1.ChangeDutyCycle(val[3])
        if "turn left" in Worker.order:
            print "turn left."
            servo1.ChangeDutyCycle(val[5])
        if "turn bottom" in Worker.order:
            print "turn bottom."
            servo4.ChangeDutyCycle(val[3])
        if  "turn top" in Worker.order:
            print "turn top."
            servo4.ChangeDutyCycle(val[5])

        print "=====Control Servo Process Ended.====="
        print ""
        print "Go Back to The Loop Top"
        print ""


if __name__ == "__main__":
    while True:
        Worker().capture_image()
        if Worker().make_order() is True:
            Worker().control_servo()
        else:
            continue
