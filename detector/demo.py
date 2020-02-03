
import os
import sys
import random
import math
import numpy as np
import skimage.io
import matplotlib
import matplotlib.pyplot as plt
from mrcnn import utils
import mrcnn.model as modellib
from mrcnn import visualize
import mrcnn.coco.coco as coco
import cv2
from models import MaskModel
from car_detectors import MaskCarDetector
matplotlib.use('TkAgg')
WEIGHTS_PATH = "mrcnn/mask_rcnn_coco.h5"


mask = MaskModel()
mask.load_weights(WEIGHTS_PATH)

car_detector = MaskCarDetector(mask.model)

image = skimage.io.imread("test1.jpg")

r, rects = car_detector.detect_cars(image)

car_detector.visualize(image, r)
print(rects)


