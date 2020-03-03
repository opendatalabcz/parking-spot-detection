from collections import defaultdict

import rx
import rx.operators as ops
from rx.scheduler import ThreadPoolScheduler
import cv2
from common import topics
from common.consumers import MessageConsumer
from common.messages import DetectorMessage
from common.messages import DetectorMessage, ImageMessage, SpotterMesssage
from common.rect import Rect
from PIL import Image, ImageDraw
import numpy as np

consumer = MessageConsumer([topics.TOPIC_SPOT], value_deserializer=lambda val: val.decode("UTF-8"), fetch_max_bytes=1024*1024*40, max_partition_fetch_bytes=1024*1024*50)

def pil_img_to_cv2(pil_image):
    return cv2.cvtColor(np.array(pil_image), cv2.COLOR_BGR2RGB)

def visualize(image, free, occupied, detected):
    image = Image.fromarray(image)
    draw = ImageDraw.Draw(image)

    for rect in free:
        left, top, right, bottom = rect
        draw.rectangle(
            [left, top, right, bottom],
            outline="green")  # spot.get_draw_color())

    for rect in occupied:
        left, top, right, bottom = rect
        draw.rectangle(
            [left, top, right, bottom],
            outline="red")  # spot.get_draw_color())

    for rect in detected:
        left, top, right, bottom = rect
        draw.rectangle(
            [left, top, right, bottom],
            outline="blue")  # spot.get_draw_color())
    cv2.imshow("frame", pil_img_to_cv2(image))

for msg in consumer:
        print("DEBUG: Received update")
        msg = SpotterMesssage.from_serialized(msg.value)
        last_occupied_rects = msg.occupied_rects
        last_free_rects = msg.free_rects
        last_detected_rects = msg.detected_rects
        image = msg.image

        print("incoming image")

        if last_occupied_rects is not None and last_free_rects is not None and last_detected_rects is not None:
            visualize(image, last_free_rects, last_occupied_rects, last_detected_rects)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
