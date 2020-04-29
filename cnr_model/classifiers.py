from keras import Sequential
from keras.layers import Conv2D, BatchNormalization, Dense, Activation, Flatten, MaxPooling2D, Dropout
from keras import optimizers
from keras.applications.vgg16 import VGG16
from keras.applications.vgg19 import VGG19
from keras.applications.resnet50 import ResNet50
from keras.applications.inception_v3 import InceptionV3

W = H = 150
C = 3


class Classifier:
    def build(self, input_shape=(W,H,3), num_classes=2):
       pass

class CInceptionV3(Classifier):

    def build(self, input_shape=(W,H,3), num_classes=2):
        model = InceptionV3(input_shape=input_shape, classes=2, weights=None, include_top=True)
        model.compile(optimizer="rmsprop", loss="categorical_crossentropy", metrics=['accuracy'])
        return model

class CVGG19(Classifier):
    def build(self, input_shape=(W,H,3), num_classes=2):
        model = VGG19(input_shape=input_shape, classes=2, weights=None)
        model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=['accuracy'])
        return model

class CResNet50(Classifier):
    def build(self, input_shape=(W,H,3), num_classes=2):
        return ResNet50(input_shape=input_shape, classes=2, weights=None)

class CVGG16(Classifier):
    def build(self, input_shape=(W,H,3), num_classes=2):
        model = VGG16(input_shape=input_shape, classes=2, weights=None)
        model.compile(optimizer="rmsprop", loss="categorical_crossentropy", metrics=['accuracy'])
        return model

class CustomAlex1(Classifier):
    def build(self, input_shape=(W,H,3), num_classes=2) -> Sequential:
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

            model.compile(optimizer=sgd, loss='categorical_crossentropy', metrics=['accuracy'])
            return model
