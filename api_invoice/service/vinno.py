#!/usr/bin/env python3
#-*-encoding:utf-8-*-
import os,sys
import  img_process.utils.box as box
import api_invoice.service.text as text
import api_common.utils.vinno as check

field = "vinno"

def get_field_name():
    return field

def get_text_by_tesseract(im,file_name,img_dir,box_type,all_result,level):
    target_path = os.path.join(img_dir, str(box_type))
    if not os.path.exists(target_path):
        os.mkdir(target_path)
        img_box(im, target_path)
    text_file = os.path.join(target_path, field + '.jpg')
    result = text.text_field_by_tesseract(text_file, check, all_result, field, level)
    if not result:
        text_result_file = os.path.join(target_path, field + '.jpg_result.jpg')
        if not os.path.exists(text_result_file):
            img_box_step(text_file)
        result = text.text_field_by_tesseract(text_result_file, check, all_result, field, level)
    if result != None:
         all_result[field + "_file"] = os.path.join(target_path ,field + '.jpg_result.jpg')
         all_result[field + "_buildfile"] = os.path.join(target_path, field + '.jpg_result.jpgbuild.jpg')
    return result


def get_text_by_machine(im,file_name,img_dir,box_type,all_result,is_get_main_region=True):
    #暂不支持
    #return None
    target_path = os.path.join(img_dir, str(box_type))
    if not os.path.exists(target_path):
        os.makedirs(target_path)
        #os.mkdir(target_path)
    text_file = os.path.join(target_path ,field + '.jpg')
    if not os.path.exists(text_file):
        img_box(im, target_path)
    #机器学习识别
    img_box_step(text_file,is_get_main_region)
    cardno_text_result_file = os.path.join(target_path, field + '.jpg_result.jpg')
    result = text.text_field_by_machine(cardno_text_result_file, check,all_result, field,max_field_length=17,min_field_length=17)
    if result != None:
         all_result[field + "_file"] = os.path.join(target_path ,field + '.jpg_result.jpg')
         all_result[field + "_buildfile"] = os.path.join(target_path, field + '.jpg_result.jpgbuild.jpg')
    return result


def img_box(im,target_dir):
    width = im.size[0]
    height = im.size[1]
    x = width * 0.67
    w = width * 0.98
    y = height * 0.47
    h = height * 0.56
    traget_path = box.box(x, y, w, h, im, target_dir, field)
    return traget_path

def img_box_step(img_field,is_get_main_region):
    #logger.debug("img_box_step:target_dir:",target_dir)
    box.box_step(img_field, w=20, h=20,letter_pace=18,row_space=30,is_get_main_region=is_get_main_region)




