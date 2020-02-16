import cv2
import matplotlib
from car_detectors import MaskCarDetector
from models import MaskModel

from common.consumers import MessageConsumer
from common.messages import ImageMessage, DetectorMessage
from common.producers import MessageProducer
from datetime import datetime

matplotlib.use('TkAgg')
WEIGHTS_PATH = "mrcnn/mask_rcnn_coco.h5"

mask = MaskModel()
mask.load_weights(WEIGHTS_PATH)

car_detector = MaskCarDetector(mask.model)

consumer = MessageConsumer("topic.detector", value_deserializer=lambda val: val.decode("UTF-8"))
producer = MessageProducer(value_serializer=lambda val: val.encode("UTF-8"))
#
# def poll_message():
#     return consumer.poll(max_records=1)
#
#
# def get_message_value(msg):
#     if msg != {}:
#         return list(msg.values())[0][0].value
#     return None


for msg in consumer:
    image_msg = ImageMessage.from_serialized(msg.value)

    cv2.imshow("window", image_msg.image)
    cv2.waitKey(1)
    r, rects = car_detector.detect_cars(image_msg.image)

    detector_msg = DetectorMessage(datetime.now().timestamp(), image_msg.lot_id, rects)

    print(image_msg.target_topic)
    print(detector_msg.serialize())
    producer.send(image_msg.target_topic, detector_msg.serialize())
    print(rects)
