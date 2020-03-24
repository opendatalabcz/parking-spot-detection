from common.rect import Rect
from kafka_consumer.models import ParkingSpotModel
from common.states import PENDING, BLOCKER, ACCEPTED, DECAYED

ACCEPTED_THRESHOLD = 30
TTL_INC = 1
TTL_DECAY = 0.3

def update(spot, is_present):
    if spot.status == BLOCKER:
        return

    if spot.status == PENDING:
        if is_present:
            spot.ttl += TTL_INC
        else:
            spot.ttl -= TTL_DECAY

    if spot.ttl < 0:
        spot.status = DECAYED

    if spot.ttl > ACCEPTED_THRESHOLD:
        spot.status = ACCEPTED


class Scene(object):
    IOU_THRESHOLD = 0.3

    def __init__(self, lot, spots):
        self.spots = spots
        self.lot = lot

    def find_best_matching(self, rect: Rect):
        current_spot = None
        current_iou = 0
        for spot in self.spots:
            iou = rect.iou(Rect.from_array(spot.coordinates))

            if iou > current_iou:
                current_iou = iou
                current_spot = spot

        return current_spot if current_iou > Scene.IOU_THRESHOLD else None

    def process_data(self, rects):
        updated = []
        for rect in rects:
            #TODO: Add intersection with blocker logic
            best = self.find_best_matching(rect)

            if best is None:
                new_spot = ParkingSpotModel(lot=self.lot, coordinates=rect.to_native_array())
                self.spots.append(new_spot)
                updated.append(new_spot)
            else:
                if best.status == BLOCKER:
                    continue
                updated.append(best)

        for spot in self.spots:
            if spot in updated:
                update(spot, True)
            else:
                update(spot, False)

        return updated
