from django.apps import AppConfig
import logging
import asyncio
import rx
import rx.operators as ops
import multiprocessing
from common.consumers import MessageConsumer
from rx.scheduler import ThreadPoolScheduler
import json

consumer = MessageConsumer("topic.backend")
optimal_thread_count = multiprocessing.cpu_count()
pool_scheduler = ThreadPoolScheduler(1)
current_scheduler = rx.scheduler.CurrentThreadScheduler()

def observe_consumer(observer, scheduler):
    for msg in consumer:
        observer.on_next(msg)

kafka_observer = rx.create(observe_consumer)



class KafkaConsumerConfig(AppConfig):
    name = 'kafka_consumer'

    def ready(self):
        from .models import DetectorResult
        def parse(message):
            value = message.value
            data = json.loads(value.decode("UTF-8"))["message"]
            print(data["rects"])
            print(DetectorResult.objects.create(lot_id=data["lot_id"], rects=data["rects"]))

        print("ready")
        kafka_observer.pipe(
             ops.subscribe_on(pool_scheduler)

         ).subscribe(
             on_next=parse,
             scheduler=pool_scheduler
         )

