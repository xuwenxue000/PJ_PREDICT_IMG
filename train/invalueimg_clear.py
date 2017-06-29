#!/usr/bin/python
#-*- encoding:utf-8 -*-

import os
from PIL import Image
import numpy as np
import cv2
import re



# 清楚无效图片
def clear(path):
    imgs = os.listdir(path)
    num = len(imgs)
    for i in range(num):
        img = cv2.imread(path + imgs[i], 0)  # 直接读为灰度图像
        if (img is None):
            print(imgs[i])
            os.remove(path + imgs[i])

# 清楚无效图片
def copyImgs(source, target):
    imgs = os.listdir(source)
    num = len(imgs)
    for i in range(num):
        img = cv2.imread(source + imgs[i], 0)  # 直接读为灰度图像
        if (img is None):
            #print(imgs[i])
            os.remove(path + imgs[i])
        else:
            cv2.imwrite(target+ imgs[i],img)


# 清楚无效图片
def mkimgxt(path,txt):
    imgs = os.listdir(path)
    num = len(imgs)
    for i in range(num):
        img = cv2.imread(path + imgs[i], 0)  # 直接读为灰度图像
        if (img is None):
            print(imgs[i])
            os.remove(path + imgs[i])



#copyImgs('/Volumes/Transcend/ijob/filesoutput/number_test/','/Volumes/Transcend/ijob/filesoutput/all_test/')
path = '/Volumes/Transcend/ijob/filesoutput/tmp/'
#path = '/Volumes/Transcend/ijob/original/lower/'
clear(path)