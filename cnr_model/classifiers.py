from keras import Sequential
from keras.layers import Conv2D, BatchNormalization, Dense, Activation, Flatten, MaxPooling2D, Dropout, SpatialDropout2D, Input
from keras import optimizers
from keras.applications.vgg16 import VGG16
from keras.applications.vgg19 import VGG19
from keras.applications.resnet50 import ResNet50
from keras.applications.inception_v3 import InceptionV3
from keras.applications.xception import Xception
from keras.applications.densenet import DenseNet121
from keras.applications.mobilenet import MobileNet
from keras.applications.mobilenet_v2 import MobileNetV2
from keras.applications.nasnet import NASNetMobile
from park_model import W, H

C = 3


class Classifier:
    def build(self, input_shape=(W, H, 3), num_classes=2):
        pass


class CDenseNet121(Classifier):
    def build(self, input_shape=(W, H, 3), num_classes=2):
        model = DenseNet121(input_shape=input_shape, classes=2, weights=None, include_top=True)
        model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=['accuracy'])
        return model


class CMobileNet(Classifier):
    def build(self, input_shape=(W, H, 3), num_classes=2):
        model = MobileNet(input_shape=input_shape, classes=2, weights=None, include_top=True)
        model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=['accuracy'])
        return model


class CMobileNetV2(Classifier):
    def build(self, input_shape=(W, H, 3), num_classes=2):
        model = MobileNetV2(input_shape=input_shape, classes=2, weights=None, include_top=True)
        model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=['accuracy'])
        return model


class CNasNetMobile(Classifier):
    def build(self, input_shape=(W, H, 3), num_classes=2):
        model = NASNetMobile(input_shape=input_shape, classes=2, weights=None, include_top=True)
        model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=['accuracy'])
        return model


class CXception(Classifier):
    def build(self, input_shape=(W, H, 3), num_classes=2):
        model = Xception(input_shape=input_shape, classes=2, weights=None, include_top=True)
        model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=['accuracy'])
        return model


class CInceptionV3(Classifier):

    def build(self, input_shape=(W, H, 3), num_classes=2):
        model = InceptionV3(input_shape=input_shape, classes=2, weights=None, include_top=True)
        model.compile(optimizer="rmsprop", loss="categorical_crossentropy", metrics=['accuracy'])
        return model


class CVGG19(Classifier):
    def build(self, input_shape=(W, H, 3), num_classes=2):
        model = VGG19(input_shape=input_shape, classes=2, weights=None)
        model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=['accuracy'])
        return model


class CResNet50(Classifier):
    def build(self, input_shape=(W, H, 3), num_classes=2):
        model = ResNet50(input_shape=input_shape, classes=2, weights=None)
        model.compile(optimizer="adam", loss="categorical_crossenteropy", metrics=['accuracy'])


class CVGG16(Classifier):
    def build(self, input_shape=(W, H, 3), num_classes=2):
        model = VGG16(input_shape=input_shape, classes=2, weights=None)
        model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=['accuracy'])
        return model


class MyNet1(Classifier):
    def build(self, input_shape=(W, H, 3), num_classes=2):
        model = Sequential()
        model.add(Conv2D(16, (11, 11), input_shape=input_shape))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2)))

        model.add(Conv2D(32, (5, 5)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2)))

        model.add(Conv2D(64, (3, 3)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2)))

        model.add(Conv2D(128, (3, 3)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(3, 3), strides=(3, 3)))

        model.add(Flatten())

        model.add(Dense(128, activation='relu'))
        model.add(Dense(num_classes, activation='softmax'))
        model.compile(optimizer='adam', metrics=['accuracy'], loss='categorical_crossentropy')
        return model


class MyNet2(Classifier):
    def build(self, input_shape=(W, H, 3), num_classes=2):
        model = Sequential()
        model.add(Conv2D(16, (11, 11), input_shape=input_shape))
        model.add(Activation('relu'))
        model.add(SpatialDropout2D(0.1))
        model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2)))

        model.add(Conv2D(32, (5, 5)))
        model.add(Activation('relu'))
        model.add(SpatialDropout2D(0.1))
        model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2)))

        model.add(Conv2D(64, (3, 3)))
        model.add(Activation('relu'))
        model.add(SpatialDropout2D(0.1))
        model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2)))

        model.add(Conv2D(128, (3, 3)))
        model.add(Activation('relu'))
        model.add(SpatialDropout2D(0.1))
        model.add(MaxPooling2D(pool_size=(3, 3), strides=(3, 3)))

        model.add(Flatten())

        model.add(Dense(256, activation='relu'))
        model.add(Dropout(0.4))
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.2))
        model.add(Dense(num_classes, activation='softmax'))
        model.compile(optimizer='adam', metrics=['accuracy'], loss='categorical_crossentropy')
        return model


class MyNet3(Classifier):
    def build(self, input_shape=(W, H, 3), num_classes=2):
        model = Sequential()
        model.add(Conv2D(16, (11, 11), input_shape=input_shape))
        model.add(BatchNormalization())
        model.add(Activation('relu'))
        model.add(SpatialDropout2D(0.5))
        model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2)))

        model.add(Conv2D(32, (5, 5)))
        model.add(BatchNormalization())
        model.add(Activation('relu'))
        model.add(SpatialDropout2D(0.5))
        model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2)))

        model.add(Conv2D(64, (3, 3)))
        model.add(BatchNormalization())
        model.add(Activation('relu'))
        model.add(SpatialDropout2D(0.5))
        model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2)))

        model.add(Conv2D(128, (3, 3)))
        model.add(BatchNormalization())
        model.add(Activation('relu'))
        model.add(SpatialDropout2D(0.5))
        model.add(MaxPooling2D(pool_size=(3, 3), strides=(3, 3)))

        model.add(Flatten())

        model.add(Dense(256, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(num_classes, activation='softmax'))
        model.compile(optimizer='adam', metrics=['accuracy'], loss='categorical_crossentropy')
        return model


class MyNet4(Classifier):
    def build(self, input_shape=(W, H, 3), num_classes=2):
        model = Sequential()

        model.add(Conv2D(16, (11, 11), input_shape=input_shape, strides=(4, 4), padding='same'))
        model.add(BatchNormalization())
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2)))
        model.add(Dropout(0.5))

        model.add(Conv2D(20, (5, 5), strides=(1, 1), padding='same'))
        model.add(BatchNormalization())
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2)))
        model.add(Dropout(0.5))

        model.add(Conv2D(30, (3, 3), strides=(1, 1), padding='same'))
        model.add(BatchNormalization())
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2)))
        model.add(Dropout(0.5))

        model.add(Flatten())

        model.add(Dense(64, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(num_classes, activation='softmax'))
        model.compile(optimizer='adam', metrics=['accuracy'], loss='categorical_crossentropy')
        return model


class MyNet5(Classifier):
    def build(self, input_shape=(W, H, 3), num_classes=2):
        model = Sequential()
        model.add(Conv2D(16, (11, 11), input_shape=input_shape, strides=(4, 4), padding='same'))
        model.add(BatchNormalization())
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2)))

        model.add(Conv2D(20, (5, 5), strides=(1, 1), padding='same'))
        model.add(BatchNormalization())
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2)))

        model.add(Flatten())
        model.add(Dense(64, activation='relu'))
        model.add(Dropout(0.25))
        model.add(Dense(32, activation='relu'))
        model.add(Dropout(0.25))
        model.add(Dense(num_classes, activation='softmax'))

        sgd = optimizers.SGD(lr=0.01, decay=5e-4, momentum=0.9, nesterov=True)

        model.compile(optimizer="adam", loss='categorical_crossentropy', metrics=['accuracy'])
        return model


class CustomAlex2(Classifier):
    def build(self, input_shape=(W, H, 1), num_classes=2) -> Sequential:
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

        model.compile(optimizer="adam", loss='categorical_crossentropy', metrics=['accuracy'])
        return model

class CustomAlex1(Classifier):
    def build(self, input_shape=(W, H, 3), num_classes=2) -> Sequential:
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

        model.compile(optimizer="adam", loss='categorical_crossentropy', metrics=['accuracy'])
        return model
