from kafka import KafkaConsumer
from ..common.consumers import MessageConsumer
consumer = MessageConsumer("test")

while True:
    for msg in consumer:
        print(msg.value)