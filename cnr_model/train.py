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


def create_model(input_shape, num_classes) -> Sequential:
    model = Sequential()
    model.add(Conv2D(16, (11, 11), input_shape=input_shape, strides=(4, 4), padding='same'))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2)))

    model.add(Conv2D(20, (5, 5), strides=(1, 1), padding='same'))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2)))

    model.add(Conv2D(30, (3, 3), strides=(1, 1), padding='same'))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2)))

    model.add(Flatten())
    model.add(Dense(48, activation='relu'))

    model.add(Dense(num_classes, activation='softmax'))

    sgd = optimizers.SGD(lr=0.01, decay=5e-4, momentum=0.9, nesterov=True)

    model.compile(optimizer=sgd, loss='binary_crossentropy', metrics=['accuracy'])
    return model


def load_images(paths):
    imgs = []
    for path in paths:
        imgs.append(ParkModel.reshaped_image(cv2.imread(path), W, H))
    return imgs


def load_labels(file, img_root):
    with open(file, "r") as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    for line in lines:
        split = line.split(" ")
        yield os.path.join(img_root, split[0]), split[1]


def load_pk_images(path):
    for path, subdirs, files in os.walk(path):

        for name in files:
            img_path = os.path.join(path, name)
            yield img_path, 1 if "occupied" in img_path.lower() else 0




IMG_DIR = "data/PATCHES"
LABELS_DIR = "data/LABELS"

PK_IMG_DIR = "pklot\\"

# labels = list(load_labels(os.path.join(LABELS_DIR, "all.txt"), IMG_DIR))
labels = list(load_labels(os.path.join(LABELS_DIR, "all.txt"), IMG_DIR))
shuffle(labels)

logdir = "logs/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard = TensorBoard(log_dir=logdir)


class Generator(Sequence):

    def __init__(self, labels, batch_size):
        self.labels = labels
        self.batch_size = batch_size

    def __getitem__(self, index):
        curr_labels = labels[index * self.batch_size: (index + 1) * self.batch_size]
        x_train = np.array(load_images(path for path, _ in curr_labels))
        curr_labels = np.array([label for _, label in curr_labels])
        y_train = np_utils.to_categorical(curr_labels, 2)
        return x_train, y_train

    def __len__(self):
        return int(len(self.labels) / self.batch_size)


MODEL_NAME = "cnr-weights15.h5"

try:
    model = keras.models.load_model(MODEL_NAME)
except:
    model = create_model((W, H, 3), 2)

BATCH_SIZE = 64
# labels = list(load_pk_images(PK_IMG_DIR))
half = int(len(labels) / 2)
print(f"half:{half}")
train_gen = Generator(labels[half:], BATCH_SIZE)
val_gen = Generator(labels[:half], BATCH_SIZE)
model.fit_generator(train_gen, validation_data=val_gen, epochs=2, callbacks=[tensorboard], workers=6, shuffle=True)

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
