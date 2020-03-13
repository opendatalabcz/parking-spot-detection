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
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile

consumer = MessageConsumer([topics.TOPIC_SPOT, topics.TOPIC_STATUS], value_deserializer=lambda val: val.decode("UTF-8"),
                           fetch_max_bytes=1024 * 1024 * 40, max_partition_fetch_bytes=1024 * 1024 * 50)
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
        from .models import SpotterModel, LotStateModel, LotModel
        def parse(message):
            print("BACKEND: Recv spots")
            if message.topic == topics.TOPIC_SPOT:
                msg = SpotterMesssage.from_serialized(message.value)
                print(msg.timestamp)
                print(msg.lot_id)
                print(msg.accepted_rects)

                img_bytes = BytesIO()
                img = Image.fromarray(msg.image)

                img.save(img_bytes, format="JPEG")
                img_bytes.seek(0)
                django_file = ContentFile(img_bytes.getvalue())
                print("DJANGO FILE")
                print(django_file)

                lot = LotModel.objects.get(id=msg.lot_id)
                model, _ = SpotterModel.objects.update_or_create(lot_id=lot, defaults={
                    "rects": json.dumps(msg.accepted_rects),
                    "image": pickle.dumps(msg.image),
                    "image_file": django_file,
                    "timestamp": make_aware(datetime.fromtimestamp(msg.timestamp))
                })

                model.image_file.save('lot_image_%d.jpg' % msg.lot_id, django_file)
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
