from time import sleep

import cv2

import os

from common.consumers import MessageConsumer
from common.messages import ImageMessage
from common.producers import MessageProducer

consumer = MessageConsumer("topic.slicer", value_deserializer=lambda val: val.decode("UTF-8"))
producer = MessageProducer(value_serializer=lambda val: val.encode("UTF-8"), max_request_size=3173440261)
stream = "movie2.mp4"
# stream = "rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov"
capture = cv2.VideoCapture(stream)

def poll_message():
    return consumer.poll(max_records=1)

def get_message_value(msg):
    if msg != {}:
        return list(msg.values())[0][0].value.decode("UTF-8")
    return None

while True:
    sleep(1)
    # msg = poll_message()
    # value = get_message_value(msg)
    value = stream
    if value is not None:
        stream = value
        capture = cv2.VideoCapture(stream)


    if capture is not None:
        ret, frame = capture.read()
        
        if not ret:
            capture = None
            continue

        cv2.imwrite("test.jpg", frame)
        msg = ImageMessage("topic.backend", frame.shape, frame, str(frame.dtype), 1)

        print(msg.serialize())

        producer.send("topic.detector", msg.serialize())
        producer.flush()







