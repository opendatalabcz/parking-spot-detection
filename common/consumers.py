from kafka import KafkaConsumer


class MessageConsumer(KafkaConsumer):

    def __init__(self, topic):
        KafkaConsumer.__init__(self, topic, bootstrap_servers="localhost:9092")