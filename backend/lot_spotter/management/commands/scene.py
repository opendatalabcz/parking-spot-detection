from common.rect import Rect
from kafka_consumer.models import ParkingSpotModel
from common.states import PENDING, BLOCKER, ACCEPTED, DECAYED

IOU_THRESHOLD = 0.3
TTL_INC = 1
TTL_DECAY = 0.3
class Scene(object):


    def __init__(self, lot, spots, accepted_threshold):
        self.spots = spots
        self.lot = lot
        self.accepted_threshold = accepted_threshold

    def find_best_matching(self, rect: Rect):
        current_spot = None
        current_iou = 0
        for spot in self.spots:
            iou = rect.iou(Rect.from_array(spot.coordinates))

            if iou > current_iou:
                current_iou = iou
                current_spot = spot

        return current_spot if current_iou > IOU_THRESHOLD else None

    def process_data(self, rects):
        updated = []
        for rect in rects:
            is_within_blocker = False
            for spot in self.spots:
                if spot.status == BLOCKER and Rect.from_array(spot.coordinates).intersect(rect):
                    is_within_blocker = True
                    break

            if is_within_blocker:
                continue

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
                self.update(spot, True)
            else:
                self.update(spot, False)

        return updated


    def update(self, spot, is_present):
        if spot.status == BLOCKER:
            return

        if spot.status == PENDING:
            if is_present:
                spot.ttl += TTL_INC
            else:
                spot.ttl -= TTL_DECAY

        if spot.ttl < 0:
            spot.status = DECAYED

        if spot.ttl > self.accepted_threshold:
            spot.status = ACCEPTED
