import base64
import json
import pickle

import numpy as np


class Serializable(object):

    def serialize(self):
        pass

    @staticmethod
    def from_serialized(serialized):
        pass


class SlicerMessage(Serializable):

    def __init__(self, target_topic, source_url, lot_id):
        self.target_topic = target_topic
        self.source_url = source_url
        self.lot_id = lot_id

    def serialize(self):
        return json.dumps({
            "target_topic": self.target_topic,
            "source_url": self.source_url,
            "lot_id": self.lot_id
        })

    @staticmethod
    def from_serialized(serialized):
        data = json.loads(serialized)
        return SlicerMessage(data["target_topic"], data["source_url"], data["lot_id"])


class DetectorMessage(Serializable):

    def __init__(self, timestamp, lot_id, rects):
        self.rects = rects
        self.lot_id = lot_id
        self.timestamp = timestamp

    def serialize(self):
        print(self.rects)
        return json.dumps({
            "timestamp": self.timestamp,
            "lot_id": self.lot_id,
            "rects": self.rects
        })

    @staticmethod
    def from_serialized(serialized):
        data = json.loads(serialized)
        return DetectorMessage(data["timestamp"], data["lot_id"], data["rects"])

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
