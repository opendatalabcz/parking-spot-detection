from collections import defaultdict

import rx
import rx.operators as ops
from rx.scheduler import ThreadPoolScheduler

from common.consumers import MessageConsumer
from common.messages import DetectorMessage
from scene_manager import SceneManager
from common.rect import Rect


lot_spotters = defaultdict(SceneManager)
consumer = MessageConsumer("topic.backend", value_deserializer=lambda val: val.decode("UTF-8"))
pool_scheduler = ThreadPoolScheduler(1)
current_scheduler = rx.scheduler.CurrentThreadScheduler()


def observe_consumer(observer, scheduler):
    for msg in consumer:
        observer.on_next(msg)


kafka_observer = rx.create(observe_consumer)


def handle(message):
    msg = DetectorMessage.from_serialized(message.value)
    spotter = lot_spotters[msg.lot_id]
    spotter.update([Rect.from_array(r) for r in msg.rects])
    print([ spot.rect.to_native_array() for spot in spotter.scene.get_detected_spots()])


kafka_observer.pipe(
    ops.subscribe_on(pool_scheduler)
).subscribe(
    on_next=handle,
    on_error=lambda err: print(err),
    scheduler=pool_scheduler
)
