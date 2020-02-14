from common.producers import MessageProducer

from time import sleep
producer = MessageProducer()
msg = b'{"type":"detector_result","version":1,"message":{"rects": [[1,2,3,4], [5,6,8,3]], "lot_id":1337}}'
producer.send("topic.backend", msg)

sleep(1)
