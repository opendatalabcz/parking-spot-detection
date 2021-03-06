import base64
import json
import pickle

import numpy as np

# TODO: Refactor image serialization

class Serializable(object):

    def serialize(self):
        pass

    @staticmethod
    def from_serialized(serialized):
        pass


class SlicerMessage(Serializable):

    def __init__(self, source_url, lot_id, running):
        self.source_url = source_url
        self.lot_id = lot_id
        self.running = running

    def serialize(self):
        return json.dumps({
            "source_url": self.source_url,
            "lot_id": self.lot_id,
            "running": self.running
        })

    @staticmethod
    def from_serialized(serialized):
        data = json.loads(serialized)
        return SlicerMessage(data["source_url"], data["lot_id"], data["running"])

class SpotterMesssage(Serializable):

    def __init__(self, lot_id, image, spots, timestamp):
        self.timestamp = timestamp
        self.lot_id = lot_id
        self.image = image
        self.spots = spots  # { id: [1,2,3,4], ... }

    def serialize(self):
        return json.dumps({
            "lot_id": self.lot_id,
            "image": base64.b64encode(pickle.dumps(self.image)).decode("ascii"),
            "spots": self.spots,
            "timestamp": self.timestamp
        })

    @staticmethod
    def from_serialized(serialized):
        data = json.loads(serialized)
        decoded = base64.b64decode(data["image"])
        image = pickle.loads(decoded)
        return SpotterMesssage(data["lot_id"], image, data["spots"], data["timestamp"])


class DetectorMessage(Serializable):

    def __init__(self, timestamp, lot_id, rects, image):
        self.rects = rects
        self.lot_id = lot_id
        self.timestamp = timestamp
        self.image = image

    def serialize(self):
        print(self.rects)
        return json.dumps({
            "timestamp": self.timestamp,
            "lot_id": self.lot_id,
            "image": base64.b64encode(pickle.dumps(self.image)).decode("ascii"),
            "rects": self.rects
        })

    @staticmethod
    def from_serialized(serialized):
        data = json.loads(serialized)
        decoded = base64.b64decode(data["image"])
        image = pickle.loads(decoded)
        return DetectorMessage(data["timestamp"], data["lot_id"], data["rects"], image)

    def __repr__(self):
        return "Detector message: timestamp: %s -  %s" % (self.timestamp, self.rects)


class ImageMessage(Serializable):

    def __init__(self, target_topic: str, shape: tuple, image: np.ndarray, type: str, lot_id: int):
        self.target_topic = target_topic
        self.shape = shape
        self.image = image
        self.type = type
        self.lot_id = lot_id

    def serialize(self):
        return json.dumps({
            "target_topic": self.target_topic,
            "shape": self.shape,
            "image": base64.b64encode(pickle.dumps(self.image)).decode("ascii"),
            "type": self.type,
            "lot_id": self.lot_id
        })

    @staticmethod
    def from_serialized(serialized):
        data = json.loads(serialized)
        decoded = base64.b64decode(data["image"])
        image = pickle.loads(decoded)
        return ImageMessage(data["target_topic"], data["shape"], image, data["type"], data["lot_id"])

class LotStatusMessage(Serializable):

    def __init__(self, timestamp, lot_id, occupied, free, spots):
        self.timestamp = timestamp
        self.lot_id = lot_id
        self.occupied = occupied
        self.free = free
        self.spots = spots

    def serialize(self):
        return json.dumps({
            "timestamp": self.timestamp,
            "lot_id": self.lot_id,
            "occupied": self.occupied,
            "free": self.free,
            "spots": self.spots
        })

    @staticmethod
    def from_serialized(serialized):
        data = json.loads(serialized)
        return LotStatusMessage(data["timestamp"], data["lot_id"], data["occupied"], data["free"], data["spots"])
