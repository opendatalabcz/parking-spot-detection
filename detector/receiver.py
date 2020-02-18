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

consumer = MessageConsumer("topic.detector", value_deserializer=lambda val: val.decode("UTF-8"), fetch_max_bytes=1024*1024*40, max_partition_fetch_bytes=1024*1024*50)
producer = MessageProducer(value_serializer=lambda val: val.encode("UTF-8"))

for msg in consumer:
    image_msg = ImageMessage.from_serialized(msg.value)

    cv2.imshow("window", image_msg.image)
    cv2.waitKey(1)
    r, rects = car_detector.detect_cars(image_msg.image)

    detector_msg = DetectorMessage(datetime.now().timestamp(), image_msg.lot_id, [rect.to_native_array() for rect in rects])

    producer.send(image_msg.target_topic, detector_msg.serialize())
    print(rects)
