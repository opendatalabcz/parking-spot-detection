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
from keras_preprocessing.image.utils import  load_img, img_to_array
from matplotlib import pyplot as plt

def load_images(paths):
    imgs = []
    for path in paths:
        # imgs.append(ParkModel.reshaped_image(cv2.imread(path), W, H))
        imgs.append(np.array((load_img(path, target_size=(W, H), interpolation='bicubic'))))
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


    def __init__(self, labels, batch_size, generate_mutations=False):
        self.labels = labels
        self.batch_size = batch_size
        self.generate_mutations = generate_mutations

        self.image_gen = ImageDataGenerator(
            featurewise_center=True,
            rotation_range=90,
            vertical_flip=True,
            zca_whitening=True,
            featurewise_std_normalization=True
        )


    def __getitem__(self, index):
        curr_labels = self.labels[index * self.batch_size: (index + 1) * self.batch_size]
        x_train = np.array(load_images(path for path, _ in curr_labels))
        curr_labels = np.array([label for _, label in curr_labels])
        y_train = np_utils.to_categorical(curr_labels, 2)
        for X_batch, y_batch in self.image_gen.flow(x_train, y_train, batch_size=9):
            for i in range(0, 9):
                plt.imshow(X_batch[i])

        return x_train, y_train if not self.generate_mutations else self.image_gen.flow(x_train, y_train, self.batch_size)

    def __len__(self):
        return int(len(self.labels) / self.batch_size)


if __name__ == "__main__":

    BATCH_SIZE = 64
    pk_labels = list(load_pk_labels(PK_IMG_DIR))  # PKLot dataset
    cnr_labels = list(load_cnr_labels(os.path.join(LABELS_DIR, "all.txt"), IMG_DIR))  # CNR dataset
    image_gen = ImageDataGenerator(
            rotation_range=45,
            dtype=np.uint8
        )
    shuffle(pk_labels)
    curr_labels = pk_labels[100000:100010]
    x_train = np.array(load_images(path for path, _ in curr_labels))
    curr_labels = np.array([label for _, label in curr_labels])
    y_train = np_utils.to_categorical(curr_labels, 2)

    # x_train, y_train = image_gen.flow(x_train, y_train, batch_size=9, ).next()
    import matplotlib
    matplotlib.use('TkAgg')
    x_train = [cv2.GaussianBlur(x, (5, 5), 0) for x in x_train]

    for i in range(0, 9):
        # edges = cv2.Canny(x_train[i], 100, 200)


        plt.subplot(330 + 1 + i)
        # plt.subplot(121), plt.imshow(x_train[i], cmap='gray')
        # plt.title('Original Image'), plt.xticks([]), plt.yticks([])
        # plt.subplot(122), plt.imshow(edges, cmap='gray')
        # plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

        # plt.show()
        plt.imshow(x_train[i].astype(np.uint8))
    plt.show()
