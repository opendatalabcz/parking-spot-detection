import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scene import Scene


def pil_img_to_cv2(pil_image):
    return cv2.cvtColor(np.array(pil_image), cv2.COLOR_BGR2RGB)


class SceneManager:

    def __init__(self):
        self.scene = Scene()

    def visualize(self, image, scene: "Scene"):
        image = Image.fromarray(image)
        draw = ImageDraw.Draw(image)

        spots = scene.spots
        detected_spots = scene.get_detected_spots()
        free_spots = scene.get_free_spots()
        occupied_spots = scene.get_occupied_spots()

        print("{} candidates, {} occupied, free: {}".format(len(detected_spots), len(occupied_spots), len(free_spots)))
        for spot in spots:
            left, top, right, bottom = spot.rect.to_array()
            draw.rectangle(
                [left, top, right, bottom],
                outline=spot.get_draw_color())
            draw.text((left, top), "id: {}\ntime: {}".format(spot.id, spot.time), fill=spot.get_draw_color())
        return image

    def visualize1(self, image, datas, spots, color="red", spots_color="green"):
        font = ImageFont.truetype(font='font/FiraMono-Medium.otf',
                                  size=np.floor(3e-2 * image.size[1] + 0.5).astype('int32'))
        thickness = (image.size[0] + image.size[1]) // 500
        draw = ImageDraw.Draw(image)

        for data in datas:

            predicted_class = data["class"]
            label = data["label"]  # + f", {predicted_class}"

            label_size = draw.textsize(label, font)

            left, top, right, bottom = data["box"]
            if top - label_size[1] >= 0:
                text_origin = np.array([left, top - label_size[1]])
            else:
                text_origin = np.array([left, top + 1])

        for spot in spots:
            thickness = 2
            left, top, right, bottom = spot.rect.to_array()
            for i in range(thickness):
                draw.rectangle(
                    [left + i, top + i, right - i, bottom - i],
                    outline=spot.get_draw_color())
        return image

    def update(self, rects):
        self.scene.process_data(rects)
