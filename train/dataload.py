#!/usr/bin/python
#-*- encoding:utf-8 -*-

import os,sys
from PIL import Image
import numpy as np
import cv2
#import api_common.utils.log as logger
# public define
numbers = ['0','1','2','3','4','5','6','7','8','9']
letters_up = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
letters_low =['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
numbers_and_letters={'0':'0','1':'1','2':'2','3':'3','4':'4','5':'5','6':'6','7':'7','8':'8','9':'9'
    ,'A':'10','B':'11','C':'12','D':'13','E':'14','F':'15','G':'16','H':'17','I':'18','J':'19','K':'20','L':'21','M':'22'
    ,'N':'23','O':'24','P':'25','Q':'26','R':'27','S':'28','T':'29','U':'30','V':'31','W':'32','X':'33','Y':'34','Z':'35'
    ,'a':'36','b':'37','c':'38','d':'39','e':'40','f':'41','g':'42','h':'43','i':'44','j':'45','k':'46','l':'47','m':'48'
    ,'n':'49','o':'50','p':'51','q':'52','r':'53','s':'54','t':'55','u':'56','v':'57','w':'58','x':'59','y':'60','z':'61'}
numbers_and_X={'0':'0','1':'1','2':'2','3':'3','4':'4','5':'5','6':'6','7':'7','8':'8','9':'9','X':'10'}


#读取文件夹filesoutput下的42000张图片，图片为灰度图，所以为1通道
#如果是将彩色图作为输入,则将1替换为3,图像大小28*28
def load_data(path):
    imgs = os.listdir(path)
    num = len(imgs)

    data = np.empty((num, 1, 28, 28), dtype="float32")
    label = np.empty((num,), dtype="uint8")

    #print num
    for i in range(num):
        img = cv2.imread(path + imgs[i], 0)  # 直接读为灰度图像
        #img = cv2.resize(img,None,fx=1,fy=1,interpolation=cv2.INTER_CUBIC)
        #cv2.imwrite(img_from_dir + "/number/" + imgs[i],img)
        im = Image.fromarray(img, None)
        #arr = np.asarray(im, dtype="float32")
        arr = np.array(im, dtype="float32")
        data[i, :, :, :] = arr
        label[i] = int(imgs[i].split('.')[0])

        """      
        #img = Image.open(img_from_dir+"/number/"+imgs[i])
        #print img.shape
        #arr = np.asarray(im,dtype="float32")
        print arr
        data[i,:,:,:] = arrzzzzz
        label[i] = int(imgs[i].split('.')[0])
        """
    return data,label

def loadAll_data(trainpath,trainnum,testpath,testnum):
    # 训练样本
    imgs = os.listdir(trainpath)
    num = len(imgs)
    if num > trainnum:
        num = trainnum

    x_train = np.empty((num, 1, 28, 28), dtype="float32")
    y_train = np.empty((num,), dtype="uint8")
    for i in range(num):
        img = cv2.imread(trainpath + imgs[i], 0)  # 直接读为灰度图像
        if img is None:
            print(imgs[i])
            os.remove(trainpath + imgs[i])
        im = Image.fromarray(img, None)
        #arr = np.asarray(im, dtype="float32")
        arr = np.array(im, dtype="float32")
        x_train[i, :, :, :] = arr
        y_train[i] = int(imgs[i].split('.')[0][0])

    # 测试样本
    imgs_test = os.listdir(testpath)
    num_test = len(imgs_test)
    #print num_test
    if num_test > testnum:
        num_test = testnum

    x_test = np.empty((num_test, 1, 28, 28), dtype="float32")
    y_test = np.empty((num_test,), dtype="uint8")

    for i in range(num_test):
        img = cv2.imread(testpath + imgs_test[i], 0)  # 直接读为灰度图像
        if img is None:
            print(imgs_test[i])
            #os.remove(trainpath + imgs[i])
        else:
            im = Image.fromarray(img, None)
            # arr = np.asarray(im, dtype="float32")
            arr = np.array(im, dtype="float32")
            x_test[i, :, :, :] = arr
            y_test[i] = int(imgs_test[i].split('.')[0][0])

    return (x_train,y_train),(x_test,y_test)

def load_X_data(path):
    #logger.debug(path)
    imgs = os.listdir(path)

    #logger.debug(imgs)
    num = len(imgs)
    if num==0:
        return None
    x = np.empty((num, 1, 28, 28), dtype="float32")
    filenames =[]
    for i in range(num):
        img = cv2.imread(path +"/"+ imgs[i], 0)  # 直接读为灰度图像
        filenames.append(imgs[i])
        img = cv2.resize(img, (28, 28), interpolation=cv2.INTER_CUBIC)
        im = Image.fromarray(img, None)
        #arr = np.asarray(im, dtype="float32")
        arr = np.array(im, dtype="float32")
        x[i, :, :, :] = arr

    return x,filenames

def load_img_data(imgpath):
    x = np.empty((1, 1, 28, 28), dtype="float32")
    img = cv2.imread(imgpath, 0)  # 直接读为灰度图像
    #img = ~img
    img = cv2.resize(img, (28, 28), interpolation=cv2.INTER_CUBIC)
    im = Image.fromarray(img, None)
    #arr = np.asarray(im, dtype="float32")
    arr = np.array(im, dtype="float32")
    x[0, :, :, :] = arr

    return x

def loadNumberAndAlphabet_data(trainpaths,testpaths):
    # 训练样本
    num_train=0
    for trainpath in trainpaths:
        path = trainpath[0]
        trainnum=trainpath[1]
        imgs = os.listdir(path)
        num = len(imgs)
        if trainnum is not None and num > trainnum:
            num = trainnum
        num_train = num_train+num
    x_trains = np.empty((num_train, 1, 28, 28), dtype="float32")
    y_trains = np.empty((num_train,), dtype="uint8")


    num_train_tmp=-1
    for trainpath in trainpaths:
        path = trainpath[0]
        trainnum=trainpath[1]
        imgs = os.listdir(path)
        num = len(imgs)
        if trainnum is not None and num > trainnum:
            num = trainnum
        for i in range(num):
            img = cv2.imread(path + imgs[i], 0)  # 直接读为灰度图像
            if(img is None):
                print(imgs[i])
            im = Image.fromarray(img, None)
            #arr = np.asarray(im, dtype="float32")
            arr = np.array(im,dtype="float32")
            num_train_tmp = num_train_tmp + 1
            x_trains[num_train_tmp, :, :, :] = arr
            y_trains[num_train_tmp] = numbers_and_letters[imgs[i].split('.')[0][0]]


    #测试样本
    num_test = 0
    for testpath in testpaths:
        path = testpath[0]
        testnum = testpath[1]
        imgs = os.listdir(path)
        num = len(imgs)
        if testnum is not None and num > testnum:
            num = testnum
        num_test = num_test + num
    x_tests = np.empty((num_test, 1, 28, 28), dtype="float32")
    y_tests = np.empty((num_test,), dtype="uint8")

    num_test_tmp = -1
    for testpath in testpaths:
        path = testpath[0]
        testnum = testpath[1]
        imgs = os.listdir(path)
        num = len(imgs)
        if testnum is not None and num > testnum:
            num = testnum
        for i in range(num):
            img = cv2.imread(path + imgs[i], 0)  # 直接读为灰度图像
            if (img is None):
                print(imgs[i])
            im = Image.fromarray(img, None)
            # arr = np.asarray(im, dtype="float32")
            arr = np.array(im, dtype="float32")
            num_test_tmp = num_test_tmp + 1
            x_tests[num_test_tmp, :, :, :] = arr
            y_tests[num_test_tmp] = numbers_and_letters[imgs[i].split('.')[0][0]]

    return (x_trains,y_trains),(x_tests,y_tests)

def loadNumberAndX_data(trainpaths,testpaths):
    # 训练样本
    num_train=0
    for trainpath in trainpaths:
        path = trainpath[0]
        imgs = os.listdir(path)
        num = len(imgs)
        #print(len(trainpath))
        if len(trainpath)==2:
            trainnum=trainpath[1]
            if num > trainnum:
                num = trainnum
        num_train = num_train+num
    x_trains = np.empty((num_train, 1, 28, 28), dtype="float32")
    y_trains = np.empty((num_train,), dtype="uint8")


    num_train_tmp=-1
    for trainpath in trainpaths:
        path = trainpath[0]
        imgs = os.listdir(path)
        num = len(imgs)

        if len(trainpath)==2:
            trainnum=trainpath[1]
            if num > trainnum:
                num = trainnum

        for i in range(num):
            img = cv2.imread(path + imgs[i], 0)  # 直接读为灰度图像
            if(img is None):
                print(imgs[i])
            im = Image.fromarray(img, None)
            #arr = np.asarray(im, dtype="float32")
            arr = np.array(im,dtype="float32")
            num_train_tmp = num_train_tmp + 1
            x_trains[num_train_tmp, :, :, :] = arr
            y_trains[num_train_tmp] = numbers_and_X[imgs[i].split('.')[0][0]]

    #测试样本
    num_test = 0
    for testpath in testpaths:
        path = testpath[0]
        imgs = os.listdir(path)
        num = len(imgs)
        if len(testpath)==2:
            testnum = testpath[1]
            if testnum is not None and num > testnum:
                num = testnum
        num_test = num_test + num
    x_tests = np.empty((num_test, 1, 28, 28), dtype="float32")
    y_tests = np.empty((num_test,), dtype="uint8")

    num_test_tmp = -1
    for testpath in testpaths:
        path = testpath[0]
        imgs = os.listdir(path)
        num = len(imgs)

        if len(testpath)==2:
            testnum = testpath[1]
            if num > testnum:
                num = testnum

        for i in range(num):
            img = cv2.imread(path + imgs[i], 0)  # 直接读为灰度图像
            if (img is None):
                print(imgs[i])
            im = Image.fromarray(img, None)
            # arr = np.asarray(im, dtype="float32")
            arr = np.array(im, dtype="float32")
            num_test_tmp = num_test_tmp + 1
            x_tests[num_test_tmp, :, :, :] = arr
            y_tests[num_test_tmp] = numbers_and_X[imgs[i].split('.')[0][0]]

    return (x_trains,y_trains),(x_tests,y_tests)