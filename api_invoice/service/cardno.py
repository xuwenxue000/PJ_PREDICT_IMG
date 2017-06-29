#!/usr/bin/env python3
#-*-encoding:utf-8-*-
import os,sys
from PIL import Image
import subprocess
import cv2
import numpy as np
import  img_process.utils.box as box
import api_invoice.service.text as text
import api_common.utils.cardno as cardno
import shutil

field = "cardno"


def get_field_name():
    return field

def get_text_by_tesseract(im,file_name,img_dir,box_type,all_result,level):
    target_path = os.path.join(img_dir, str(box_type))
    if not os.path.exists(target_path):
        os.mkdir(target_path)
        img_box(im, target_path)
    text_file = os.path.join(target_path, field + '.jpg')
    result = text.text_field_by_tesseract(text_file, cardno, all_result, field, level)
    if not result:
        text_result_file = os.path.join(target_path, field + '.jpg_result.jpg')
        if not os.path.exists(text_result_file):
            img_box_step(text_file)
        result = text.text_field_by_tesseract(text_result_file, cardno, all_result, field, level)

    if result != None:
         all_result[field + "_file"] = os.path.join(target_path ,field + '.jpg_result.jpg')
         all_result[field + "_buildfile"] = os.path.join(target_path, field + '.jpg_result.jpgbuild.jpg')
    return result


def get_text_by_machine(im,file_name,img_dir,box_type,all_result,is_get_main_region=True):
    try_num = ""
    target_path = os.path.join(img_dir, str(box_type))
    if not os.path.exists(target_path):
        os.makedirs(target_path)
        #os.mkdir(target_path)
    cardno_text_file = os.path.join(target_path ,field + '.jpg')
    if not os.path.exists(cardno_text_file):
        img_box(im, target_path)
    #机器学习识别
    img_box_step(cardno_text_file,is_get_main_region)
    cardno_text_result_file = os.path.join(target_path, field + '.jpg_result.jpg')
    result = text.text_field_by_machine(cardno_text_result_file, cardno,all_result, field,("architecture_number_X","weights_number_X"),model_type=3,max_field_length=18,min_field_length=15,try_num=3)

    if not result:
        try_num="1"
        img_box_step(cardno_text_file,is_get_main_region= not is_get_main_region,try_num=try_num)
        cardno_text_result_file = os.path.join(target_path, field + '.jpg_result'+str(try_num)+'.jpg')
        result = text.text_field_by_machine(cardno_text_result_file, cardno, all_result, field,
                                            ("architecture_number_X", "weights_number_X"), model_type=3,
                                            max_field_length=18, min_field_length=15,try_num=3)

    if result != None:
         all_result[field + "_file"] = cardno_text_result_file
         all_result[field + "_buildfile"] = os.path.join(target_path, field + '.jpg_result'+str(try_num)+'.jpgbuild.jpg')
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
    x = width*0.135
    w = width * 0.47
    y = height * 0.27
    h = height * 0.34
    filename = "cardno"
    traget_path = box.box(x, y, w, h, im, target_dir, filename)
    return  traget_path

def img_box_step(img_field,is_get_main_region=True,try_num=""):
    #logger.debug("img_box_step:target_dir:",target_dir)
    box.box_step(img_field, w=18, h=20,letter_pace=20,is_get_main_region=is_get_main_region,try_num=try_num)




