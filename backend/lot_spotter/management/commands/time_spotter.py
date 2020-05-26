from django.core.management.base import BaseCommand

from django.core.management.base import BaseCommand

from common import topics
from common.consumers import MessageConsumer
from common.messages import DetectorMessage, ImageMessage, SpotterMesssage, LotStatusMessage
from common.producers import MessageProducer
from common.rect import Rect
from common.states import DECAYED
from kafka_consumer.models import LotModel, ParkingSpotModel, LotHistoryModel, SpotHistoryModel, SettingsModel
from .scene import Scene
from .scene_manager import SceneManager
from datetime import *
from common.states import ACCEPTED, BLOCKER
from common.settings import CLASSIFY_PERIOD_SECONDS

consumer = MessageConsumer([topics.TOPIC_DETECT, topics.TOPIC_IMAGE, topics.TOPIC_STATUS],
                           value_deserializer=lambda val: val.decode("UTF-8"),
                           fetch_max_bytes=1024 * 1024 * 40, max_partition_fetch_bytes=1024 * 1024 * 50)
producer = MessageProducer(value_serializer=lambda val: val.encode("UTF-8"), max_request_size=3173440261)


def handle_detect_message(message):
    msg = DetectorMessage.from_serialized(message.value)
    lot = LotModel.objects.get(id=msg.lot_id)
    settings = SettingsModel.objects.get(lot_id=msg.lot_id)
    spots = ParkingSpotModel.objects.filter(lot=lot)

    scene = Scene(lot, list(spots), settings.ttl_to_accept)
    updated = scene.process_data([Rect.from_array(r) for r in msg.rects])

    for spot in updated:
        if spot.status == DECAYED and spot.id is not None:
            spot.delete()
        else:
            spot.save()

    for spot in spots:
        spot.save()

    print("Updating ParkingSpotModels")
    # msg = SpotterMesssage(msg.timestamp, msg.lot_id, msg.image, serialized_rects)
    # producer.send(topics.TOPIC_SPOT, msg.serialize())

    import cv2
    manager = SceneManager(scene)
    cv2.imshow("win", manager.visualize(msg.image, scene))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        pass


LAST_CLASSIFICATION: datetime = None


def handle_image_message(message):
    global LAST_CLASSIFICATION
    if not LAST_CLASSIFICATION or datetime.now() - LAST_CLASSIFICATION >= timedelta(seconds=CLASSIFY_PERIOD_SECONDS):
        msg = ImageMessage.from_serialized(message.value)
        lot = LotModel.objects.get(id=msg.lot_id)

        spots = list(ParkingSpotModel.objects.filter(lot=lot, status=ACCEPTED).values('id', 'coordinates'))
        spots = {spot["id"]: {"coordinates": spot["coordinates"]} for spot in spots}
        print(spots)
        msg = SpotterMesssage(lot.id, msg.image, spots, str(datetime.now()))
        producer.send(topics.TOPIC_SPOT, msg.serialize())
        LAST_CLASSIFICATION = datetime.now()


def handle_status_message(message):
    msg = LotStatusMessage.from_serialized(message.value)
    print(msg.free)
    for key in msg.spots:
        id = int(key)
        spot_history = SpotHistoryModel(spot_id=id, timestamp=msg.timestamp, occupancy=msg.spots[key]['occupancy'])
        spot_history.save()

    lot_history = LotHistoryModel(lot_id=msg.lot_id,
                                  num_occupied=msg.occupied,
                                  num_vacant=msg.free,
                                  timestamp=msg.timestamp)
    lot_history.save()


class Command(BaseCommand):
    help = 'Starts listening for kafka messages'

    def handle(self, *args, **options):
        for message in consumer:
            if message.topic == topics.TOPIC_DETECT:
                handle_detect_message(message)
            if message.topic == topics.TOPIC_IMAGE:
                handle_image_message(message)
            if message.topic == topics.TOPIC_STATUS:
                handle_status_message(message)
