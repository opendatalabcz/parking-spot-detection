import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from .scene import Scene
from common.states import PENDING, BLOCKER, ACCEPTED, DECAYED

def pil_img_to_cv2(pil_image):
    return cv2.cvtColor(np.array(pil_image), cv2.COLOR_BGR2RGB)


class SceneManager:

    def __init__(self, scene):
        self.scene = scene

    def visualize(self, image, scene: "Scene"):
        image = Image.fromarray(image)
        draw = ImageDraw.Draw(image)

        spots = scene.spots
        colors = {
            ACCEPTED: "green",
            BLOCKER: "red",
            PENDING: "orange",
            DECAYED: "black"
        }

        for spot in spots:

            if spot.status == DECAYED:
                continue
            left, top, right, bottom = spot.coordinates
            draw.rectangle(
                [left, top, right, bottom],
                outline=colors[spot.status])
            draw.text((left, top), "id: {}\nttl: {}".format(spot.id, spot.ttl), fill=colors[spot.status])
        return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    def update(self, rects):
        self.scene.process_data(rects)
