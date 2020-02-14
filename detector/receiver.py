from kafka import KafkaConsumer
from common.consumers import MessageConsumer
from common.producers import MessageProducer
from common.messages import ImageMessage
from time import sleep

import cv2
import numpy as np
import matplotlib
import skimage.io
from car_detectors import MaskCarDetector

from models import MaskModel

matplotlib.use('TkAgg')
WEIGHTS_PATH = "mrcnn/mask_rcnn_coco.h5"

mask = MaskModel()
mask.load_weights(WEIGHTS_PATH)

car_detector = MaskCarDetector(mask.model)

consumer = MessageConsumer("topic.detector")


def poll_message():
    return consumer.poll(max_records=1)


def get_message_value(msg):
    if msg != {}:
        return list(msg.values())[0][0].value
    return None



for msg in consumer:
    image_msg = ImageMessage.from_serialized(msg.value)

    cv2.imshow("window", image_msg.image)
    cv2.waitKey(1)
    # r, rects = car_detector.detect_cars(image_msg.image)
    value = None
