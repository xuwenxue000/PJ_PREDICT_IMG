#!/usr/bin/env python3
#-*-encoding:utf-8-*-
import os,sys
from PIL import Image
import subprocess
import cv2
import numpy as np
import  img_process.utils.box as box
import api_invoice.service.text as text
import api_common.utils.organno as organno
import shutil

field = "organno"

def get_field_name():
    return field

def get_text_by_tesseract(im,file_name,img_dir,box_type,all_result,level):
    target_path = os.path.join(img_dir, str(box_type))
    if not os.path.exists(target_path):
        os.mkdir(target_path)
        img_box(im, target_path)
    text_file = os.path.join(target_path, field + '.jpg')
    result = text.text_field_by_tesseract(text_file, organno, all_result, field, level)
    if not result:
        text_result_file = os.path.join(target_path, field + '.jpg_result.jpg')
        if not os.path.exists(text_result_file):
            img_box_step(text_file)
        result = text.text_field_by_tesseract(text_result_file, organno, all_result, field, level)

    if result != None:
         all_result[field + "_file"] = os.path.join(target_path ,field + '.jpg_result.jpg')
         all_result[field + "_buildfile"] = os.path.join(target_path, field + '.jpg_result.jpgbuild.jpg')
    return result


def get_text_by_machine(im,file_name,img_dir,box_type,all_result,is_get_main_region=True):
    target_path = os.path.join(img_dir, str(box_type))
    if not os.path.exists(target_path):
        os.makedirs(target_path)
        #os.mkdir(target_path)
    cardno_text_file = os.path.join(target_path ,field + '.jpg')
    if not os.path.exists(cardno_text_file):
        img_box(im, target_path)
    #机器学习识别
    img_box_step(cardno_text_file,is_get_main_region)
    # 暂不支持
    return None
    cardno_text_result_file = os.path.join(target_path, field + '.jpg_result.jpg')
    result = text.text_field_by_machine(cardno_text_result_file, organno,all_result, field,max_field_length=20,min_field_length=5)
    if result != None:
         all_result[field + "_file"] = os.path.join(target_path ,field + '.jpg_result.jpg')
         all_result[field + "_buildfile"] = os.path.join(target_path, field + '.jpg_result.jpgbuild.jpg')
    return result


def img_box(im,target_dir):
    width = im.size[0]
    height = im.size[1]
    #x =0
    #y =height*0.26
    #w = width*0.12
    #h = height*0.32
    #filename = "cardno_pre"
    #traget_path = box.box(x,y,w,h,im,target_dir,filename)
    #box.box_step(traget_path,20,30)
    x = width * 0.14
    w = width * 0.47
    y = height * 0.26
    h = height * 0.34
    traget_path = box.box(x, y, w, h, im, target_dir, field)
    return  traget_path

def img_box_step(img_field,is_get_main_region):
    #logger.debug("img_box_step:target_dir:",target_dir)
    box.box_step(img_field, w=16, h=20, letter_pace=10,is_get_main_region=is_get_main_region)




