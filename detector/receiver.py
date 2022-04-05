import logging
from datetime import datetime

import cv2
import matplotlib
import tensorflow as tf
from common import topics
from common.common_utils import timed
from common.consumers import MessageConsumer
from common.messages import DetectorMessage, ImageMessage
from common.producers import MessageProducer

from car_detectors import MaskCarDetector
from models import MaskModel

gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
  try:
    for gpu in gpus:
      tf.config.experimental.set_memory_growth(gpu, True)
  except RuntimeError as e:
    print(e)

WEIGHTS_PATH = "detector/mrcnn/mask_rcnn_coco.h5"

mask = MaskModel()
mask.load_weights(WEIGHTS_PATH)

car_detector = MaskCarDetector(mask.model)

logging.error("Creating consumer")
consumer = MessageConsumer([topics.TOPIC_IMAGE], value_deserializer=lambda val: val.decode("UTF-8"), fetch_max_bytes=1024*1024*40, max_partition_fetch_bytes=1024*1024*50)
logging.error("Creating producer")
producer = MessageProducer(value_serializer=lambda val: val.encode("UTF-8"), max_request_size=3173440261)
logging.error("Producer & consumer created")

@timed
def handle_image_message(msg):
    image_msg = ImageMessage.from_serialized(msg.value)

    r, rects = car_detector.detect_cars(image_msg.image)

    detector_msg = DetectorMessage(datetime.now().timestamp(), image_msg.lot_id,
                                   [rect.to_native_array() for rect in rects], image_msg.image)
    producer.send(topics.TOPIC_DETECT, detector_msg.serialize())

for msg in consumer:
    handle_image_message(msg)
