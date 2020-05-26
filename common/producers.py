from kafka import KafkaProducer
from .settings import KAFKA_SERVERS


class MessageProducer(KafkaProducer):

    def __init__(self, **config):
        KafkaProducer.__init__(self, bootstrap_servers=KAFKA_SERVERS, **config)
