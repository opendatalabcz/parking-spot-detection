from kafka import KafkaProducer


class MessageProducer(KafkaProducer):

    def __init__(self, **config):
        KafkaProducer.__init__(self, bootstrap_servers=["localhost:9092"], **config)
