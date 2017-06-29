#!/usr/bin/env python3
#-*-encoding:utf-8-*-

import os,sys
from PIL import Image
import subprocess
import cv2
import numpy as np
#将图片设置为宽度必须等于width的图片


def gray(src_path,out_path):
    #print("src_path:"+src_path)
    img = cv2.imread(src_path)
    img_height = img.shape[0]
    img_width = img.shape[1]
    #print("width:",img_width)
    #print("height:",img_height)
    img = cv2.imread(src_path, 0)  # 直接读为灰度图像
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 10)
    cv2.imwrite(out_path,img)
