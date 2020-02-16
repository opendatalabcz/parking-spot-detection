from kafka import KafkaConsumer
from common.consumers import MessageConsumer
from common.producers import MessageProducer
from time import sleep
from common.messages import ImageMessage
import json

import cv2
import numpy as np

consumer = MessageConsumer("topic.slicer", value_deserializer=lambda val: val.decode("UTF-8"))
producer = MessageProducer(value_serializer= lambda val: val.encode("UTF-8"))
stream = "rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov"
capture = cv2.VideoCapture(stream)

def poll_message():
    return consumer.poll(max_records=1)

def get_message_value(msg):
    if msg != {}:
        return list(msg.values())[0][0].value.decode("UTF-8")
    return None

while True:
    sleep(1)
    msg = poll_message()
    value = get_message_value(msg)

    if value is not None:
        stream = value
        capture = cv2.VideoCapture(stream)
        print(value)

    if capture is not None:
        ret, frame = capture.read()
        msg = ImageMessage("topic.backend", frame.shape, frame, str(frame.dtype), 1)

        producer.send("topic.detector", msg.serialize())







