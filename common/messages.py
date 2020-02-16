import numpy as np
import json
import base64


class Serializable(object):

    def serialize(self):
        pass

    @staticmethod
    def from_serialized(serialized: bytes):
        pass


class DetectorMessage(Serializable):

    def __init__(self, timestamp, lot_id, rects):
        self.rects = rects
        self.lot_id = lot_id
        self.timestamp = timestamp

    def serialize(self):
        return json.dumps({
            "timestamp": self.timestamp,
            "lot_id": self.lot_id,
            "rects": self.rects
        })

    @staticmethod
    def from_serialized(serialized: bytes):
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
            "image": base64.encodebytes(self.image.tobytes()).decode("UTF-8"),
            "type": self.type,
            "lot_id": self.lot_id
        })

    @staticmethod
    def from_serialized(serialized: bytes):
        data = json.loads(serialized)
        decoded = base64.decodebytes(data["image"].encode("UTF-8"))
        image = np.reshape(np.frombuffer(decoded, data["type"]), data["shape"])
        return ImageMessage(data["target_topic"], data["shape"], image, data["type"], data["lot_id"])
