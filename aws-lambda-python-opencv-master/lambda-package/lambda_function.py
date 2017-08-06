import boto3
import cv2


s3 = boto3.resource('s3')


def lambda_handler(event, context):
    s3.Bucket('bento-robot').download_file('girl_laugh_face.jpg', '/tmp/test.jpg')
    return "It works!"

# if __name__ == "__main__":
#     lambda_handler(42, 42)
