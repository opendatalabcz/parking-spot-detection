from park_model import ParkModel
from train import load_pk_labels, load_cnr_labels, PK_IMG_DIR, IMG_DIR, LABELS_DIR, load_images
import os
import numpy as np
from random import shuffle
import keras.utils as utils
from keras.utils.vis_utils import plot_model

if __name__ == "__main__":


    # model = ParkModel(ParkModel.from_file("net5-02_accuracy-0.9363_val-loss-0.1002_val-acc-0.8916.h5"))
    # model = ParkModel(ParkModel.from_file("net5-05_accuracy-0.9734_val-loss-0.0369_val-acc-0.9311.h5"))
    # model = ParkModel(ParkModel.from_file("net5-01_accuracy-0.9551_val-loss-0.3001_val-acc-0.9008.h5"))
    # model = ParkModel(ParkModel.from_file("net5-01_accuracy-0.9212_val-loss-0.1682_val-acc-0.9430.h5"))
    # model = ParkModel(ParkModel.from_file("net5-02_accuracy-0.9432_val-loss-0.1246_val-acc-0.9588.h5"))
    model = ParkModel(ParkModel.from_file("net5-01_accuracy-0.9603_val-loss-0.2144_val-acc-0.9276.h5"))

    pk_labels = list(load_pk_labels(PK_IMG_DIR))  # PKLot dataset
    cnr_labels = list(load_cnr_labels(os.path.join(LABELS_DIR, "all.txt"), IMG_DIR))  # CNR dataset
    shuffle(pk_labels)
    shuffle(cnr_labels)

    total = 10000
    curr_labels = pk_labels[:total]
    x_train = np.array(load_images(path for path, _ in curr_labels))
    curr_labels = np.array([label for _, label in curr_labels])
    y_train = utils.to_categorical(curr_labels, 2)

    x_train = x_train / 255

    correct = 0

    preds = model.predict(x_train)

    model.model.summary()



    for i in range(len(preds)):
        answer = np.argmax(preds[i])
        print(preds[i], y_train[i])
        if y_train[i][answer] == 1:
            correct += 1

    print(correct, "/", total)
    print(correct/total*100, "%")




