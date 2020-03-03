from django.apps import AppConfig
import logging
import asyncio
import rx
import rx.operators as ops
import multiprocessing
from common.consumers import MessageConsumer
from rx.scheduler import ThreadPoolScheduler
from common.messages import SpotterMesssage, LotStatusMessage
from datetime import datetime
import pickle
from django.utils.timezone import make_aware
import threading
import json
import common.topics as topics
consumer = MessageConsumer([topics.TOPIC_SPOT, topics.TOPIC_STATUS], value_deserializer=lambda val: val.decode("UTF-8"),
                           fetch_max_bytes=1024 * 1024 * 40, max_partition_fetch_bytes=1024 * 1024 * 50)
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
        from .models import SpotterModel, LotStateModel, LotModel
        def parse(message):
            print("BACKEND: Recv spots")
            if message.topic == topics.TOPIC_SPOT:
                msg = SpotterMesssage.from_serialized(message.value)
                print(msg.timestamp)
                print(msg.lot_id)
                print(msg.accepted_rects)
                lot = LotModel.objects.get(id=msg.lot_id)
                SpotterModel.objects.update_or_create(lot_id=lot, defaults={
                    "rects": json.dumps(msg.accepted_rects),
                    "image": pickle.dumps(msg.image),
                    "timestamp": make_aware(datetime.fromtimestamp(msg.timestamp))
                })
            elif message.topic == topics.TOPIC_STATUS:
                print("BACKEND: Recv status")
                msg = LotStatusMessage.from_serialized(message.value)
                lot = LotModel.objects.get(id=msg.lot_id)

                LotStateModel.objects.create(lot_id=lot,
                                             full_spots=msg.occupied,
                                             available_spots=msg.free,
                                             timestamp=make_aware(datetime.fromtimestamp(msg.timestamp)))


        print("ready")
        # kafka_observer.subscribe(
        #     on_next=parse,
        #     scheduler=pool_scheduler
        # )
