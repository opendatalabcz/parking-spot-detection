import os
import datetime
import cv2
import keras
import numpy as np
import tensorflow as tf
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
from classifiers import CustomAlex1, CVGG16, CResNet50, CVGG19, CInceptionV3, CDenseNet121, CXception, MyNet2, MyNet1, \
    MyNet3, MyNet4, MyNet5, CMobileNet, CMobileNetV2
from matplotlib import pyplot
from keras_preprocessing.image.utils import load_img, img_to_array
from keras.callbacks import EarlyStopping, ModelCheckpoint, ProgbarLogger

config = tf.ConfigProto(device_count={'GPU': 1, 'CPU': 6})
sess = tf.Session(config=config)
keras.backend.set_session(sess)


def load_images(paths):
    imgs = []
    for path in paths:
        imgs.append(np.array((load_img(path, target_size=(W, H), interpolation='bicubic'))))
        # imgs.append(ParkModel.reshaped_image(cv2.imread(path), W, H))
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
        super(Generator).__init__()

        self.labels = labels
        self.batch_size = batch_size
        self.generate_mutations = generate_mutations

        self.image_gen = ImageDataGenerator(
            rotation_range=45,
            horizontal_flip=True
        )

    def __getitem__(self, index):
        curr_labels = self.labels[index * self.batch_size: (index + 1) * self.batch_size]
        x_train = np.array(load_images(path for path, _ in curr_labels))
        curr_labels = np.array([label for _, label in curr_labels])
        y_train = np_utils.to_categorical(curr_labels, 2)

        if self.generate_mutations:
            return self.image_gen.flow(x_train, y_train, self.batch_size).next()
        else:
            return x_train, y_train

    def __len__(self):
        return int(len(self.labels) / self.batch_size)


if __name__ == "__main__":
    MODEL_NAME = "weights-pk-alex.h5"

    factory = CMobileNetV2()
    model = factory.build()

    model.summary()

    logdir = "logs/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + "-pk-alex"
    tensorboard = TensorBoard(log_dir=logdir)

    es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=15)
    mc = ModelCheckpoint(
        'alex_epoch-{epoch:02d}_accuracy-{accuracy:.4f}_val-loss-{val_loss:.4f}_val-acc-{val_accuracy:.4f}.h5',
        monitor='val_loss', mode='min', save_best_only=True, verbose=1, period=4)
    # model = ResNet50(input_shape=(W,H,3),classes=2, weights=None)
    # model = VGG16(input_shape=(W,H,3),classes=2, weights=None)

    BATCH_SIZE = 32
    pk_labels = list(load_pk_labels(PK_IMG_DIR))  # PKLot dataset
    cnr_labels = list(load_cnr_labels(os.path.join(LABELS_DIR, "all.txt"), IMG_DIR))  # CNR dataset

    # half = int(len(labels) / 2)
    # print(f"half:{half}")
    shuffle(pk_labels)
    shuffle(cnr_labels)
    shuffle(pk_labels)
    shuffle(cnr_labels)
    shuffle(pk_labels)
    shuffle(cnr_labels)
    train_gen = Generator(cnr_labels, BATCH_SIZE)
    val_gen = Generator(pk_labels, BATCH_SIZE)

    ratio = 1 / 20
    model.fit_generator(train_gen, validation_data=val_gen, callbacks=[tensorboard, mc], shuffle=True, verbose = 1, max_queue_size = 5, workers = 6,
                        steps_per_epoch=len(cnr_labels)/200,epochs=200)
