
class IState:
    def update(self, is_present):
        pass


class DecayedState(IState):
    def update(self, is_present):
        pass


class PendingState(IState):
    TTL_DECAY = 1
    TTL_INC = 1
    START_TTL = 1
    TTL_TO_ACCEPTED = 20 * 20

    def __init__(self):
        self.ttl = PendingState.START_TTL


    def update(self, is_present):
        if not is_present:
            self.ttl -= PendingState.TTL_DECAY
        else:
            self.ttl += PendingState.TTL_INC

        if self.ttl > PendingState.TTL_TO_ACCEPTED:
            return AcceptedOccupiedState()

        if self.ttl < 0:
            return DecayedState()

        return self


class AcceptedOccupiedState(IState):
    THRESHOLD = 100

    def __init__(self):
        self.not_detected_count = 0

    def update(self, is_present):
        if not is_present:
            self.not_detected_count += 1
        else:
            self.not_detected_count = 0

        if self.not_detected_count >= AcceptedOccupiedState.THRESHOLD:
            return AcceptedFreeState()
        else:
            return self


class AcceptedFreeState(IState):
    THRESHOLD = 5

    def __init__(self):
        self.detected_count = 0

    def update(self, is_present):
        if is_present:
            self.detected_count += 1
        else:
            self.detected_count = 0

        if self.detected_count >= AcceptedFreeState.THRESHOLD:
            return AcceptedOccupiedState()
        else:
            return self
