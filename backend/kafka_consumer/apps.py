from django.apps import AppConfig
import logging
import asyncio
import rx
import rx.operators as ops
import multiprocessing
from common.consumers import MessageConsumer
from rx.scheduler import ThreadPoolScheduler
from common.messages import DetectorMessage
import threading
import json

consumer = MessageConsumer("topic.backend", value_deserializer=lambda val: val.decode("UTF-8"))
optimal_thread_count = multiprocessing.cpu_count()
pool_scheduler = ThreadPoolScheduler(2)
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
            msg = DetectorMessage.from_serialized(message.value)
            new = DetectorResult.objects.create(timestamp=msg.timestamp, rects=json.dumps(msg.rects), lot_id=msg.lot_id)
            print(new)

        print("ready")
        kafka_observer.pipe(
            ops.subscribe_on(pool_scheduler)
        ).subscribe(
            on_next=parse,
            scheduler=pool_scheduler
        )
