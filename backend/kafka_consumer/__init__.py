# from django.apps import AppConfig
# import logging
# import asyncio
# import rx
# import rx.operators as ops
# import multiprocessing
# from common.consumers import MessageConsumer
# from rx.scheduler import ThreadPoolScheduler
# from .models import DetectorResult
# import json
#
# consumer = MessageConsumer("topic.backend")
# optimal_thread_count = multiprocessing.cpu_count()
# pool_scheduler = ThreadPoolScheduler(optimal_thread_count)
# current_scheduler = rx.scheduler.CurrentThreadScheduler()
#
# def observe_consumer(observer, scheduler):
#     for msg in consumer:
#         observer.on_next(msg)
#
# kafka_observer = rx.create(observe_consumer)
#
# def parse(message):
#     value = message.value
#     data = json.loads(value.decode("UTF-8"))
#     DetectorResult.objects.create(**data)
#
