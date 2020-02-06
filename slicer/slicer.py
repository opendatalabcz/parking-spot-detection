from kafka import KafkaProducer
from common.producers import MessageProducer
from time import sleep

producer = MessageProducer()
producer.send('test', b'test from slicer2')

sleep(5)