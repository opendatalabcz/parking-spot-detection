import skimage.io
from PIL import Image, ImageDraw
from common.rect import Rect
import cv2
import numpy as np


def pil_img_to_cv2(pil_image):
    return cv2.cvtColor(np.array(pil_image), cv2.COLOR_BGR2RGB)


class IDetector:
    def detect_cars(self, image):
        pass

    def visualize(self, image, result):
        pass


class MaskCarDetector(IDetector):

    def __init__(self, model):
        self.model = model
        self.class_names = ['BG', 'person', 'bicycle', 'car', 'motorcycle', 'airplane',
                            'bus', 'train', 'truck', 'boat', 'traffic light',
                            'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird',
                            'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear',
                            'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie',
                            'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
                            'kite', 'baseball bat', 'baseball glove', 'skateboard',
                            'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup',
                            'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
                            'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
                            'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed',
                            'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote',
                            'keyboard', 'cell phone', 'microwave', 'oven', 'toaster',
                            'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors',
                            'teddy bear', 'hair drier', 'toothbrush']


    def detect_cars(self, image):
        r = self.model.detect([image], verbose=0)
        r = r[0]
        rects = [Rect.from_array([r['rois'][i][1], r['rois'][i][0], r['rois'][i][3], r['rois'][i][2]]) for i in range(len(r['rois']))
                 if r["class_ids"][i] in [3, 8, 9]]
        return r, rects

    def visualize(self, image, r):
        image = Image.fromarray(image)
        draw = ImageDraw.Draw(image)

        for spot in r['rois']:
            top, left, bottom, right = spot
            draw.rectangle(
                [left, top, right, bottom],
                outline="red")  # spot.get_draw_color())
        cv2.imshow("frame", pil_img_to_cv2(image))

        # visualize.display_instances(image, r['rois'], r['masks'], r['class_ids'],
        #                           self.class_names, r['scores'])

