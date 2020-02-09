from kafka import KafkaConsumer
from common.consumers import MessageConsumer
from common.producers import MessageProducer
from time import sleep

import cv2
import numpy as np

consumer = MessageConsumer("topic.detector")


for msg in consumer:
    arr = np.frombuffer(msg.value, dtype="uint8")
    arr = arr.reshape((160, 240, 3))
    print(arr.shape)
    print(arr.dtype)

    cv2.imshow('VIDEO', arr)
    cv2.waitKey(1)







