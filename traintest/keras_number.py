#!/usr/bin/python
#-*- encoding:utf-8 -*-
'''Trains a simple convnet on the MNIST dataset.
Gets to 99.25% test accuracy after 12 epochs
(there is still a lot of margin for parameter tuning).
16 seconds per epoch on a GRID K520 GPU.
'''


from __future__ import print_function
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K

#公共参数
import os,sys
py_dir = os.path.dirname(os.path.realpath(__file__))
project_dir = os.path.dirname(py_dir)
sys.path.append(project_dir)
import train.dataload as dataload

import numpy as np
import matplotlib.pyplot as plt
import h5py
import creatTrainDataSet.mydataset as mydataset
# public define

def trainnumber(trainpath,testpath):
    batch_size = 128
    num_classes = 10
    epochs = 12
    # input image dimensions
    img_rows, img_cols = 28, 28

    #加载数据
    (x_train, y_train), (x_test, y_test) = dataload.loadAll_data(trainpath,60000,testpath,2000)
    print (x_train[0],y_train[0])

    if K.image_data_format() == 'channels_first':
        x_train = x_train.reshape(x_train.shape[0], 1, img_rows, img_cols)
        x_test = x_test.reshape(x_test.shape[0], 1, img_rows, img_cols)
        input_shape = (1, img_rows, img_cols)
    else:
        x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
        x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
        input_shape = (img_rows, img_cols, 1)

    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')
    x_train /= 255
    x_test /= 255

    print('x_train shape:', x_train.shape)
    print(x_train.shape[0], 'train samples')
    print(x_test.shape[0], 'test samples')

    print(y_test)

    # convert class vectors to binary class matrices
    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_test = keras.utils.to_categorical(y_test, num_classes)
    print("hello")
    print(x_test[200], y_test[200])

    for n in range(0,10):
        for i in x_test[n * 100]:
            for j in i:
                print("%0.1f " % j, end='')
            print()
        print(y_test[n * 100])

    model = Sequential()
    model.add(Conv2D(32, kernel_size=(3, 3),activation='relu', input_shape=input_shape))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(64, kernel_size=(3, 3),activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dense(num_classes, activation='softmax'))

    model.compile(loss=keras.losses.categorical_crossentropy,
                  optimizer=keras.optimizers.Adadelta(),
                  metrics=['accuracy'])

    model.fit(x_train, y_train,
              batch_size=batch_size,
              epochs=epochs,
              verbose=2,
              validation_data=(x_test, y_test))
    score = model.evaluate(x_test, y_test, verbose=0)
    print('Test loss:', score[0])
    print('Test accuracy:', score[1])

    #保存神经网络的结构与训练好的参数
    json_string = model.to_json()#等价于 json_string = model.get_config()
    open('number_architecture.json','w').write(json_string)
    model.save_weights('number_weights.h5')

(img_from_dir,img_to_dir) = mydataset.getmydatasetdir(0)
trainnumber(img_to_dir+'/number_train_3/',img_to_dir+'/number_test_3/')