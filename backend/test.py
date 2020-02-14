from kafka import KafkaConsumer, KafkaProducer
from common.consumers import MessageConsumer
consumer = MessageConsumer("topic.backend")

print(consumer.topics())

for msg in consumer:
    print(msg)

