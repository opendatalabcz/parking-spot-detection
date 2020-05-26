from kafka import KafkaConsumer
from .settings import KAFKA_SERVERS


class MessageConsumer(KafkaConsumer):

    def __init__(self, topic, **config):
        KafkaConsumer.__init__(self, *topic, bootstrap_servers=KAFKA_SERVERS, consumer_timeout_ms=float('inf'),
                               **config)
