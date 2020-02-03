

import mrcnn.model as model
import mrcnn.coco.coco as coco

class MaskModel(object):
    class InferenceConfig(coco.CocoConfig):
        GPU_COUNT = 1
        IMAGES_PER_GPU = 1


    def __init__(self):
        self.model = model.MaskRCNN(mode="inference", model_dir="logs/", config=self.InferenceConfig())

    def load_weights(self, weights_path):
        self.model.load_weights(weights_path, by_name=True)
