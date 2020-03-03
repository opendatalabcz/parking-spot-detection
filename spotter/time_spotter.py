from collections import defaultdict

import rx
import rx.operators as ops
from rx.scheduler import ThreadPoolScheduler

from common.consumers import MessageConsumer
from common.producers import MessageProducer
from common.messages import DetectorMessage, SpotterMesssage
from scene_manager import SceneManager
from common import topics
from common.rect import Rect
import cv2

lot_spotters = defaultdict(SceneManager)
consumer = MessageConsumer([topics.TOPIC_DETECT], value_deserializer=lambda val: val.decode("UTF-8"),
                           fetch_max_bytes=1024 * 1024 * 40, max_partition_fetch_bytes=1024 * 1024 * 50)
producer = MessageProducer(value_serializer=lambda val: val.encode("UTF-8"), max_request_size=3173440261)

if __name__ == "__main__":

    for message in consumer:
        msg = DetectorMessage.from_serialized(message.value)
        spotter = lot_spotters[msg.lot_id]
        spotter.update([Rect.from_array(r) for r in msg.rects])

        occupied_rects = [spot.rect.to_native_array() for spot in spotter.scene.get_occupied_spots()]
        free_rects = [spot.rect.to_native_array() for spot in spotter.scene.get_free_spots()]
        detected_rects = [spot.rect.to_native_array() for spot in spotter.scene.get_detected_spots()]
        accepted_rects = [spot.rect.to_native_array() for spot in spotter.scene.get_accepted_spots()]

        msg = SpotterMesssage(msg.timestamp, msg.lot_id, msg.image, occupied_rects, free_rects, accepted_rects, detected_rects)
        print("Spotter: sending message")
        print(accepted_rects)
        producer.send(topics.TOPIC_SPOT, msg.serialize())
        producer.flush()
