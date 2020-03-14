import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from .scene import Scene
from .state import PENDING, BLOCKER, ACCEPTED

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
            PENDING: "orange"
        }

        for spot in spots:
            left, top, right, bottom = spot.rect.to_array()
            draw.rectangle(
                [left, top, right, bottom],
                outline=colors[spot.state])
            draw.text((left, top), "id: {}\nttl: {}".format(spot.id, spot.ttl), fill=colors[spot.state])
        return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    def update(self, rects):
        self.scene.process_data(rects)
