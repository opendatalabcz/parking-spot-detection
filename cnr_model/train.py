import os
import datetime
import cv2
import keras
import numpy as np
from keras.utils import np_utils
from skimage import transform
from keras.models import Sequential
from keras.optimizers import SGD
from keras.layers import Conv2D, BatchNormalization, Dense, Activation, Flatten, MaxPooling2D, Dropout
from park_model import ParkModel, H, W
from random import shuffle
from keras import optimizers
from keras.callbacks import TensorBoard
from keras.utils import Sequence
from keras.applications.resnet50 import ResNet50
from keras.applications.vgg16 import VGG16
from keras.preprocessing.image import ImageDataGenerator
from classifiers import CustomAlex1, CVGG16, CResNet50, CVGG19, CInceptionV3

def load_images(paths):
    imgs = []
    for path in paths:
        imgs.append(ParkModel.reshaped_image(cv2.imread(path), W, H))
    return imgs


def load_cnr_labels(file, img_root):
    with open(file, "r") as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    for line in lines:
        split = line.split(" ")
        yield os.path.join(img_root, split[0]), split[1]


def load_pk_labels(path):
    for path, subdirs, files in os.walk(path):

        for name in files:
            img_path = os.path.join(path, name)
            yield img_path, 1 if "occupied" in img_path.lower() else 0




IMG_DIR = "data/PATCHES"
LABELS_DIR = "data/LABELS"

PK_IMG_DIR = "pklot\\"

# labels = list(load_labels(os.path.join(LABELS_DIR, "all.txt"), IMG_DIR))





class Generator(Sequence):

    def __init__(self, labels, batch_size):
        self.labels = labels
        self.batch_size = batch_size

    def __getitem__(self, index):
        curr_labels = self.labels[index * self.batch_size: (index + 1) * self.batch_size]
        x_train = np.array(load_images(path for path, _ in curr_labels))
        curr_labels = np.array([label for _, label in curr_labels])
        y_train = np_utils.to_categorical(curr_labels, 2)
        return x_train, y_train

    def __len__(self):
        return int(len(self.labels) / self.batch_size)

MODEL_NAME = "cnr-weights-vgg16.h5"


try:
    model = keras.models.load_model(MODEL_NAME)
except:
    factory = CVGG16()
    model = factory.build()


logdir = "logs/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + "-CVGG19"
tensorboard = TensorBoard(log_dir=logdir)



# model = ResNet50(input_shape=(W,H,3),classes=2, weights=None)
# model = VGG16(input_shape=(W,H,3),classes=2, weights=None)

BATCH_SIZE = 64
pk_labels = list(load_pk_labels(PK_IMG_DIR)) # PKLot dataset
cnr_labels = list(load_cnr_labels(os.path.join(LABELS_DIR, "all.txt"), IMG_DIR)) #CNR dataset



# half = int(len(labels) / 2)
# print(f"half:{half}")
train_gen = Generator(cnr_labels, BATCH_SIZE)
val_gen = Generator(pk_labels, BATCH_SIZE)
model.fit_generator(train_gen, validation_data=val_gen, epochs=3, callbacks=[tensorboard], workers=6, shuffle=True)

model.save_weights(MODEL_NAME)
model.save(MODEL_NAME)
#
# for i in range(0, len(labels), 512):
#     current_labels = labels[i:i + 512]
#     data = np.array(load_images([path for path, _ in current_labels]))
#     current_labels = np.array([label for _, label in current_labels])
#     current_labels = np_utils.to_categorical(current_labels, 2)
#
#     x_train = data
#     y_train = current_labels
#
#     MODEL_NAME = "cnr-weights.h5"
#
#     try:
#         model = keras.models.load_model("cnr-weights4.h5")
#     except:
#         model = create_model((W, H, 3), 2)
#
#     print(x_train.shape)
#
#     model.fit(x_train, y_train, epochs=1, validation_split=0.5, callbacks=[tensorboard], batch_size=64)
#
#     del x_train
#     del y_train
#     del current_labels
#     del data
#     model.save_weights('cnr-weights4.h5')
#     model.save('cnr-weights4.h5')
