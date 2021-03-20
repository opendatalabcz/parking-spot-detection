from kafka import KafkaConsumer
import logging
from .settings import KAFKA_SERVERS


class MessageConsumer(KafkaConsumer):

    def __init__(self, topic, **config):
        logging.error(config) 
        logging.error(KAFKA_SERVERS)
        KafkaConsumer.__init__(self, *topic, bootstrap_servers=KAFKA_SERVERS, consumer_timeout_ms=float('inf'),
                               **config)
