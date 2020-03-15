import json
import pickle
from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware
from datetime import datetime

from common import topics
from common.consumers import MessageConsumer
from common.messages import DetectorMessage, SpotterMesssage, LotStatusMessage
from common.producers import MessageProducer
from common.rect import Rect
from kafka_consumer.models import SpotterModel, LotModel, LotStateModel
from .scene import Spot, Scene
from .scene_manager import SceneManager

consumer = MessageConsumer([topics.TOPIC_DETECT, topics.TOPIC_STATUS],
                           value_deserializer=lambda val: val.decode("UTF-8"),
                           fetch_max_bytes=1024 * 1024 * 40, max_partition_fetch_bytes=1024 * 1024 * 50)
producer = MessageProducer(value_serializer=lambda val: val.encode("UTF-8"), max_request_size=3173440261)


class Command(BaseCommand):
    help = 'Starts listening for kafka messages'

    def handle(self, *args, **options):
        for message in consumer:

            if message.topic == topics.TOPIC_DETECT:

                msg = DetectorMessage.from_serialized(message.value)

                record = list(SpotterModel.objects.filter(lot_id_id=msg.lot_id))
                if not record:
                    data = []
                else:
                    data = record[-1].rects

                spots = [Spot(Rect.from_array(d["rect"]), d["state"], d["ttl"]) for d in data]

                scene = Scene(spots)
                scene.process_data([Rect.from_array(r) for r in msg.rects])

                img_bytes = BytesIO()
                img = Image.fromarray(msg.image)

                img.save(img_bytes, format="JPEG")
                img_bytes.seek(0)
                django_file = ContentFile(img_bytes.getvalue())

                lot = LotModel.objects.get(id=msg.lot_id)
                serialized_rects = [spot.serialize() for spot in scene.spots]
                model, _ = SpotterModel.objects.update_or_create(lot_id=lot, defaults={
                    "rects": serialized_rects,
                    "image": pickle.dumps(msg.image),
                    "image_file": django_file,
                    "timestamp": make_aware(datetime.fromtimestamp(msg.timestamp))
                })
                model.image_file.save('lot_image_%d.jpg' % msg.lot_id, django_file)

                print("Updating Lot Rectangles")

                msg = SpotterMesssage(msg.timestamp, msg.lot_id, msg.image, serialized_rects)

                producer.send(topics.TOPIC_SPOT, msg.serialize())
            else:
                print("Updating Lot Status")
                msg = LotStatusMessage.from_serialized(message.value)

                lot = LotModel.objects.get(id=msg.lot_id)

                LotStateModel.objects.create(lot_id=lot,
                                             full_spots=msg.occupied,
                                             available_spots=msg.free,
                                             timestamp=make_aware(datetime.fromtimestamp(msg.timestamp)))

        # import cv2
        # manager = SceneManager(scene)
        # cv2.imshow("win", manager.visualize(msg.image, scene))
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
