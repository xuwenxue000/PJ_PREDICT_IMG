#!/usr/bin/env python3
#-*-encoding:utf-8-*-

import os,sys
from PIL import Image
import subprocess
import api_common.utils.log as logger
import cv2
import numpy as np
#处理横竖问题
def change_wh(src_path,out_path):
    if os.path.exists(out_path):
        os.remove(out_path)
    out_dir_path = os.path.dirname(out_path)
    if not os.path.exists(out_dir_path) :
        os.makedirs(out_dir_path)
    logger.debug("src_path:"+src_path)
    #logger.debug("out_path:"+out_path)
    img = cv2.imread(src_path)

    img_height = img.shape[0]
    img_width = img.shape[1]
    img_new = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_new = cv2.adaptiveThreshold(img_new, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 3)
    img_new, cnts, hierarchy = cv2.findContours(img_new, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    img_new = cv2.cvtColor(img_new, cv2.COLOR_GRAY2BGR)
    area_map = {}
    index=0

    for c in cnts:
        area = cv2.contourArea(c)
        area_map[area] = c
        #img_new = cv2.rectangle(img_new,(x,y),(x+w,y+h),(255,0,0))
    sort_keys = sorted(area_map.keys())
    c = area_map.get(sort_keys[-2])
    (x, y, w, h) = cv2.boundingRect(c)
    #print("wh======(x, y, w, h):",(x, y, w, h))
    img_new = cv2.rectangle(img_new, (x, y), (x + w, y + h), (255, 0, 0),10)
    cv2.imwrite(out_path+"_01.jpg", img_new)


    #logger.debug("width:",img_width)
    #logger.debug("height:",img_height)
#如果长宽比错误,进行90度的处理
    #if img_height>img_width :
    if h>w :
        #M = cv2.getRotationMatrix2D((img_height/2,img_width/2), 90, 1)
        pts1 = np.float32([[0, 0], [img_width, 0], [0, img_height]])
        pts2 = np.float32([[img_width, 0], [img_width, img_height], [0, 0]])
        M = cv2.getAffineTransform(pts1, pts2)
        img = cv2.warpAffine(img, M, (img_width,img_height))
        img = cv2.resize(img, (img_height,img_width ), interpolation=cv2.INTER_CUBIC)
    cv2.imwrite(out_path,img)

def change_tb(src_path,out_path):
    if os.path.exists(out_path):
        os.remove(out_path)
    out_dir_path = os.path.dirname(out_path)
    if not os.path.exists(out_dir_path):
        os.makedirs(out_dir_path)
    # 如果上线颠倒,进行180度的处理
    logger.debug("src_path:"+src_path)
    logger.debug("out_path:"+out_path)
    img = cv2.imread(src_path)

    img_height = img.shape[0]
    img_width = img.shape[1]

    logger.debug("width:",img_width)
    logger.debug("height:",img_height)
    pts1 = np.float32([[0, 0], [img_width, img_height], [0, img_height]])
    pts2 = np.float32([[img_width, img_height], [0, 0], [img_width, 0]])
    M = cv2.getAffineTransform(pts1, pts2)
    img = cv2.warpAffine(img, M, (img_width, img_height))
    cv2.imwrite(out_path, img)

