* Robotics Arm which have 4 servomotors
Raspberry Pi 3 manipulate those motors following orders by Amazon EC2.

* AWS backended
EC2 contiunausly polling to SQS,Then raspberry pi 3 Publish image to SQS, EC2 catch binary data,processing with Dlib.Processed data publish to SQS,Then Raspberry pi 3 get processed image.
