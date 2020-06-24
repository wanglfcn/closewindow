import logging
from time import sleep
import cv2
import datetime
import random
from tornado.options import options

class CameraService:
    def __init__(self):
        pass

    def takePhoto(self):
        camera_port = 0
        camera = cv2.VideoCapture(camera_port)
        fileName = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
        while True:
            return_value, image = camera.read()
            if cv2.waitKey(1) & 0xFF == ord('s'):
                break
            sleep(2)
            break

        filePath = options.image_dir + '/' + fileName + str(random.randrange(1, 10000)) + '.jpg'
        cv2.imwrite(filePath, image)
        camera.release()
        cv2.destroyAllWindows()
        return filePath

if __name__ == '__main__':
    c = CameraService()
    c.takePhoto()
