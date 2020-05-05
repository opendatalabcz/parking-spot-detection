from time import sleep

import cv2

import os

from common.consumers import MessageConsumer
from common.messages import ImageMessage
from common.producers import MessageProducer
from common import topics

consumer = MessageConsumer([topics.TOPIC_SLICE], value_deserializer=lambda val: val.decode("UTF-8"))
producer = MessageProducer(value_serializer=lambda val: val.encode("UTF-8"), max_request_size=3173440261)
stream = "realhd.mp4"
# stream = "rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov"
capture = cv2.VideoCapture(stream)
capture = None


def poll_message():
    return consumer.poll(max_records=1)


def get_message_value(msg):
    if msg != {}:
        return list(msg.values())[0][0].value.decode("UTF-8")
    return None

os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"

counter = 0
fps = 1

if __name__ == "__main__":
    while True:
        # msg = poll_message()
        # value = get_message_value(msg)
        value = stream

        if value is not None and capture is None:
            stream = value
            capture = cv2.VideoCapture(stream, cv2.CAP_FFMPEG)
            fps = int(capture.get(cv2.CAP_PROP_FPS))
            spf = 1 / fps
            counter = 0
            print("FPS:  %d" % fps)

        if capture is not None:
            ret, frame = capture.read()
            counter += 1
            if not ret:
                print(ret)
                capture = None
                continue

            if counter % fps == 0:

                # cv2.imwrite("snapshot2.jpg", frame)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                msg = ImageMessage(topics.TOPIC_BACKEND, frame.shape, frame, str(frame.dtype), 4)

                print("Slicer: sending message")
                counter = 0
                producer.send(topics.TOPIC_IMAGE, msg.serialize())
                producer.flush()
