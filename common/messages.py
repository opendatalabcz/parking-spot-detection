import numpy as np
import json
import base64

class ImageMessage():

    def __init__(self, target_topic: str, shape: tuple, image: np.ndarray, type: str):
        self.target_topic = target_topic
        self.shape = shape
        self.image = image
        self.type = type

    def serialize(self):
        return json.dumps({
            "target_topic": self.target_topic,
            "shape": self.shape,
            "image": base64.encodebytes(self.image.tobytes()).decode("UTF-8"),
            "type": self.type
        }).encode("UTF-8")

    @staticmethod
    def from_serialized(serialized: bytes):
        data = json.loads(serialized.decode("UTF-8"))
        bytes = base64.decodebytes(data["image"].encode("UTF-8"))
        image = np.reshape(np.frombuffer(bytes, data["type"]), data["shape"])
        return ImageMessage(data["target_topic"], data["shape"], image, data["type"])


