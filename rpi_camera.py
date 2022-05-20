import cv2
from imutils.video.pivideostream import PiVideoStream
import imutils
import time
import numpy as np
from aiymakerkit import vision
from aiymakerkit import utils
import models

#load face detection model
face_detector = vision.Detector(models.FACE_DETECTION_MODEL)

# object detection model
object_detector = vision.Detector(models.OBJECT_DETECTION_MODEL)

labels = utils.read_labels_from_metadata(models.OBJECT_DETECTION_MODEL)

class RPiCamera(object):

    def __init__(self):
        self.stream = PiVideoStream().start()
        time.sleep(2.0)

    def __del__(self):
        self.stream.stop()

    def get_frame(self):
        frame = self.stream.read()
        result, jpeg = cv2.imencode('.jpg', frame)

        return jpeg


    def get_frame_with_face_detect(self):
        frame = self.stream.read()

        #detect faces before converting to jpeg
        faces = face_detector.get_objects(frame, threshold=0.1)
        vision.draw_objects(frame, faces)
        result, jpeg = cv2.imencode('.jpg', frame)

        return jpeg

    def get_frame_with_object_detect(self):
        frame = self.stream.read()

        objects = object_detector.get_objects(frame, threshold=0.4)
        vision.draw_objects(frame, objects, labels)

        result, jpeg = cv2.imencode('.jpg', frame)

        return jpeg

