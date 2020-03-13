from common.rect import Rect
from .state import DECAYED, PENDING, BLOCKER, ACCEPTED

ACCEPTED_THRESHOLD = 30

class Spot(object):
    id_seed = 0

    def __init__(self, rect, state, ttl):
        self.rect = rect
        self.state = state
        self.id = Spot.id_seed
        self.ttl = ttl
        Spot.id_seed += 1
        self.time = 0

    def update(self, is_present):

        if self.state == BLOCKER:
            return

        if self.state == PENDING:
            if is_present:
                self.ttl += 1
            else:
                self.ttl -= 0.5

        if self.ttl < 0:
            self.state = DECAYED

        if self.ttl > ACCEPTED_THRESHOLD:
            self.state = ACCEPTED

        self.time += 1

    def serialize(self):
        return {
            "rect": self.rect.to_native_array(),
            "ttl": self.ttl,
            "state": self.state
        }



class Scene(object):
    IOU_THRESHOLD = 0.5

    def __init__(self, spots):
        self.spots = spots

    def find_best_matching(self, rect: Rect) -> Spot:
        current_spot = None
        current_iou = 0
        for spot in self.spots:
            iou = rect.iou(spot.rect)

            if iou > current_iou:
                current_iou = iou
                current_spot = spot

        return current_spot if current_iou > Scene.IOU_THRESHOLD else None

    def process_data(self, rects):
        updated = []
        for rect in rects:
            best = self.find_best_matching(rect)



            if best is None:
                new_spot = Spot(rect, PENDING, 1)
                self.spots.append(new_spot)
                updated.append(new_spot)
            else:
                if best.state == BLOCKER:
                    continue
                updated.append(best)

        for spot in self.spots:
            if spot in updated:
                spot.update(True)
            else:
                spot.update(False)

        self.spots = [spot for spot in self.spots if spot.state != DECAYED]
