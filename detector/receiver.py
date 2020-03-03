import cv2
import matplotlib
from car_detectors import MaskCarDetector
from models import MaskModel
from common import topics
from common.consumers import MessageConsumer
from common.messages import ImageMessage, DetectorMessage
from common.producers import MessageProducer
from datetime import datetime
import tensorflow as tf

gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
  try:
    for gpu in gpus:
      tf.config.experimental.set_memory_growth(gpu, True)
  except RuntimeError as e:
    print(e)

matplotlib.use('TkAgg')
WEIGHTS_PATH = "mrcnn/mask_rcnn_coco.h5"

mask = MaskModel()
mask.load_weights(WEIGHTS_PATH)

car_detector = MaskCarDetector(mask.model)

consumer = MessageConsumer([topics.TOPIC_IMAGE], value_deserializer=lambda val: val.decode("UTF-8"), fetch_max_bytes=1024*1024*40, max_partition_fetch_bytes=1024*1024*50)
producer = MessageProducer(value_serializer=lambda val: val.encode("UTF-8"), max_request_size=3173440261)

for msg in consumer:
    image_msg = ImageMessage.from_serialized(msg.value)

    r, rects = car_detector.detect_cars(image_msg.image)

    detector_msg = DetectorMessage(datetime.now().timestamp(), image_msg.lot_id, [rect.to_native_array() for rect in rects], image_msg.image)
    producer.send(topics.TOPIC_DETECT, detector_msg.serialize())
    print(rects)
