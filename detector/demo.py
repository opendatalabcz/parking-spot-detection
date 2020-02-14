import matplotlib
import skimage.io
from car_detectors import MaskCarDetector

from models import MaskModel

matplotlib.use('TkAgg')
WEIGHTS_PATH = "mrcnn/mask_rcnn_coco.h5"


mask = MaskModel()
mask.load_weights(WEIGHTS_PATH)

car_detector = MaskCarDetector(mask.model)

image = skimage.io.imread("test1.jpg")

r, rects = car_detector.detect_cars(image)

print(rects)


