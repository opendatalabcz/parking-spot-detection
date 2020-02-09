from kafka import KafkaConsumer


class MessageConsumer(KafkaConsumer):

    def __init__(self, topic):
        KafkaConsumer.__init__(self, topic, bootstrap_servers="localhost:9092", consumer_timeout_ms=500,  request_timeout_ms=500)