from .rect import Rect
from parker.states.state import AcceptedOccupiedState, AcceptedFreeState, DecayedState, PendingState


class Spot(object):
    id_seed = 0

    def __init__(self, rect):
        self.rect = rect
        self.state = PendingState()
        self.id = Spot.id_seed
        Spot.id_seed += 1
        self.time = 0

    def is_occupied(self):
        return isinstance(self.state, AcceptedOccupiedState)

    def get_draw_color(self):
        if isinstance(self.state, AcceptedOccupiedState):
            return "blue"

        if isinstance(self.state, AcceptedFreeState):
            return "green"

        return "orange"

    def update(self, is_present):
        self.state = self.state.update(is_present)
        self.time += 1


class Scene(object):
    IOU_THRESHOLD = 0.5
    spots = []

    def get_free_spots(self):
        return list(filter(lambda s: isinstance(s.state, AcceptedFreeState), self.spots))

    def get_detected_spots(self):
        return list(filter(lambda s: not isinstance(s.state, AcceptedFreeState) and not isinstance(s.state, AcceptedOccupiedState),
                           self.spots))

    def get_occupied_spots(self):
        return list(filter(lambda s: isinstance(s.state, AcceptedOccupiedState), self.spots))

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
                new_spot = Spot(rect)
                self.spots.append(new_spot)
                updated.append(new_spot)
            else:
                updated.append(best)

        for spot in self.spots:
            if spot in updated:
                spot.update(True)
            else:
                spot.update(False)

        self.spots = [spot for spot in self.spots if not isinstance(spot.state, DecayedState)]
