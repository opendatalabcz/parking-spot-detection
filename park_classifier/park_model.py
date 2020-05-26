import keras
import numpy as np
from skimage import transform

W = H = 32
C = 3

class ParkModel(object):

    def __init__(self, keras_model):
        self.model = keras_model

    def predict(self, what):
        x = [self.reshaped_image(i, W, H) for i in what]
        x = np.array(x)
        return self.model.predict(x)

    @staticmethod
    def from_file(path):
        return keras.models.load_model(path)

    @staticmethod
    def reshaped_image(image, width=W, height=H):
        return transform.resize(image, (width, height, C))
