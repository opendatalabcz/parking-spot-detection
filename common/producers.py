from kafka import KafkaProducer
from .settings import KAFKA_SERVERS
import logging

class MessageProducer(KafkaProducer):

    def __init__(self, **config):
        logging.error(config) 
        logging.error(KAFKA_SERVERS)
        KafkaProducer.__init__(self, bootstrap_servers=KAFKA_SERVERS, **config)
