from collections import defaultdict

import rx
import rx.operators as ops
from rx.scheduler import ThreadPoolScheduler
import cv2
from common import topics
from common.consumers import MessageConsumer
from common.producers import MessageProducer
from common.messages import DetectorMessage
from common.messages import DetectorMessage, ImageMessage, SpotterMesssage, LotStatusMessage
from common.rect import Rect
from PIL import Image, ImageDraw
import numpy as np
from park_model import ParkModel
import tensorflow as tf
from common.states import ACCEPTED, OCCUPIED, UNKNOWN, VACANT
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
    except RuntimeError as e:
        print(e)

consumer = MessageConsumer([topics.TOPIC_SPOT], value_deserializer=lambda val: val.decode("UTF-8"),
                           fetch_max_bytes=1024 * 1024 * 40, max_partition_fetch_bytes=1024 * 1024 * 50)
producer = MessageProducer(value_serializer=lambda val: val.encode("UTF-8"), max_request_size=3173440261)
model = ParkModel(ParkModel.from_file("alex_weights-93-cnr-pk"))

for msg in consumer:
    print("MODEL: Received update")

    msg = SpotterMesssage.from_serialized(msg.value)
    img = msg.image

    counts = [0, 0]
    states = [VACANT, OCCUPIED]
    print(msg.spots)
    for spot_id in msg.spots:

        data = msg.spots[spot_id]
        rect = Rect.from_array(data["coordinates"])

        crop_img = img[rect.top:rect.top + rect.height(), rect.left:rect.left + rect.width()]
        res = model.predict([crop_img])
        print(res)
        argmax = int(np.argmax(res[0]))
        # argmax = 1 if res[0][argmax] >= 0.99 else 0
        data["occupancy"] = states[argmax]
        data["last_eval"] = msg.timestamp
        counts[argmax] += 1

    msg = LotStatusMessage(msg.timestamp, msg.lot_id, counts[1], counts[0], msg.spots)
    print("MODEL: Sending result")
    producer.send(topics.TOPIC_STATUS, msg.serialize())
