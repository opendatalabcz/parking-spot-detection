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
from keras.callbacks import TensorBoard


def create_model(input_shape, num_classes) -> Sequential:
    model = Sequential()
    model.add(Conv2D(30, (11, 11), input_shape=input_shape, strides=(4, 4), padding='same'))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(5, 5), strides=(5, 5)))
    model.add(Dropout(0.25))
    model.add(Conv2D(20, (5, 5), strides=(1, 1), padding='same'))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
    model.add(Flatten())
    model.add(Dense(100, activation='relu'))
    model.add(Dense(100, activation='relu'))
    model.add(Dense(num_classes, activation='softmax'))
    model.compile(optimizer="adam", loss='binary_crossentropy', metrics=['accuracy'])
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


IMG_DIR = "data/PATCHES"
LABELS_DIR = "data/LABELS"

labels = list(load_labels(os.path.join(LABELS_DIR, "all.txt"), IMG_DIR))[:100000]
shuffle(labels)

logdir = "logs/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
logdir = "logs/training"
tensorboard = TensorBoard(log_dir=logdir)

for i in range(0, len(labels), 5000):
    current_labels = labels[i:i + 5000]
    data = np.array(load_images([path for path, _ in current_labels]))
    current_labels = np.array([label for _, label in current_labels])
    current_labels = np_utils.to_categorical(current_labels, 2)

    x_train = data
    y_train = current_labels

    MODEL_NAME = "cnr-weights.h5"

    try:
        model = keras.models.load_model("cnr-weights3.h5")
    except:
        model = create_model((W, H, 3), 2)

    print(x_train.shape)

    model.fit(x_train, y_train, epochs=3, validation_split=0.5, callbacks=[tensorboard])

    model.save_weights('cnr-weights3.h5')
    model.save('cnr-weights3.h5')

