import django
django.setup()

from kafka_consumer.models import SettingsModel
import cv2
import os

from time import sleep
import six
from django.core.management.base import BaseCommand
from common.consumers import MessageConsumer
from common.messages import SlicerMessage, ImageMessage
from common.producers import MessageProducer
from common import topics
from django.utils import text
import multiprocessing as mp
import codecs

consumer = MessageConsumer([topics.TOPIC_SLICE], value_deserializer=lambda val: val.decode("UTF-8"),
                           group_id="slice-group", auto_commit_interval_ms=1000, enable_auto_commit=True,
                           auto_offset_reset='earliest')
producer = MessageProducer(value_serializer=lambda val: val.encode("UTF-8"), max_request_size=3173440261)
procs = {}

def slice(url, lot_id):
    # url = url.replace("\\", "/")
    print(f"starting on URL {url}")
    capture = cv2.VideoCapture(url, cv2.CAP_FFMPEG)
    if capture and capture.isOpened():
        fps = int(capture.get(cv2.CAP_PROP_FPS))
        spf = 1 / fps
        counter = 0
        print("FPS:  %d" % fps)
        while capture.isOpened():
            ret, frame = capture.read()
            counter += 1
            if not ret:
                print(ret)
                capture = None
                continue

            if counter % fps == 0:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                msg = ImageMessage(topics.TOPIC_BACKEND, frame.shape, frame, str(frame.dtype), lot_id)

                print("Slicer: sending message")
                counter = 0
                producer.send(topics.TOPIC_IMAGE, msg.serialize())
                producer.flush()

def set_settings_running(lot_id, running):
    settings = SettingsModel.objects.get(lot_id=lot_id)
    settings.running = running
    settings.save()

def start_process(url, lot_id):
    print("starting new process")
    proc = mp.Process(target=slice, args=(url, lot_id))
    proc.start()
    procs[lot_id] = proc

def update_procs():
    all_settings = SettingsModel.objects.all()

    for settings in all_settings:
        if settings.running:
            if settings.lot_id in procs:
                if not procs[settings.lot_id].is_alive():
                    start_process(settings.video_src, settings.lot_id)
            else:
                start_process(settings.video_src, settings.lot_id)
        else:
            if settings.lot_id in procs:
                if procs[settings.lot_id].is_alive():
                    print("killing a process")
                    procs[settings.lot_id].terminate()
                del procs[settings.lot_id]





class Command(BaseCommand):
    help = 'Manages slicers for lots'
    def handle(self, *args, **options):
        while True:
            sleep(4)

            update_procs()


            # msg = consumer.poll(max_records=1)
            #
            # if msg:
            #     for item in six.iteritems(msg):
            #         _, msgs = item
            #
            #         for msg in msgs:
            #             print(msg)
            #             if msg.topic == topics.TOPIC_SLICE:
            #                 message = SlicerMessage.from_serialized(msg.value)
            #                 if message.running:
            #                     if message.lot_id not in procs or not procs[message.lot_id].is_alive():
            #                         start_process(message.source_url, message.lot_id)
            #                         print(procs)
            #                         set_settings_running(message.lot_id, True)
            #                 else:
            #                     if message.lot_id in procs and procs[message.lot_id].is_alive():
            #                         procs[message.lot_id].terminate()
            #                         del procs[message.lot_id]
            #                         set_settings_running(message.lot_id, False)
