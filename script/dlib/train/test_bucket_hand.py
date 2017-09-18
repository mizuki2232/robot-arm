import time
import RPi.GPIO as GPIO


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

PIN = 26
GPIO.setup(PIN, GPIO.OUT)
servo1 = GPIO.PWM(PIN, 50)

val = [2.5, 3.6875, 4.875, 6.0625, 7.25, 8.4375, 9.625, 10.8125, 12]


def control_servo():
    """controle servo method."""
    print ""
    print "=====Control Servo Process Start.====="
    print ""
    servo1.start(0.0)
    servo1.ChangeDutyCycle(val[0])
    time.sleep(3)
    servo1.ChangeDutyCycle(val[4])
    time.sleep(3)
    servo1.ChangeDutyCycle(val[0])
    print "=====Servo Motor Turn Off.====="
    print "=====Control Servo Process Ended.====="
    print ""
    print "Go Back to The Loop Top"
    print ""


if __name__ == "__main__":
    control_servo()
