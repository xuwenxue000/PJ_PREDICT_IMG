#!/usr/bin/env python3
#-*-encoding:utf-8-*-
#planA 通过长宽比例切出对应内容的图片
import os
import shutil
import subprocess

import cv2
from PIL import Image
import api_common.utils.vinno as vinno
import api_common.utils.cardno as cardno
import api_common.utils.organno as organno
import api_common.utils.engineno as engineno
import  pickle
import img_process.utils.resize as resize
import  api_invoice.service.box as box
import time, threading
import json

def text_all(file_path_box_dir,width,all_result):
    result = {}
    all_result["info"] = result
    if os.path.exists(file_path_box_dir):
        cardno_str = None
        cardno_str, param = text_cardno(file_path_box_dir,  all_result)
        if not cardno_str == None:
            result["cardno"] = cardno_str
        else:
            organno_str, param = text_organno(file_path_box_dir, all_result)
            if not organno_str == None:
                result["organno"] = organno_str
            else:
                result["cardno"] = result["cardno_default"]
    pass

def text_cardno(file_path_box_dir,all_result):
    pass


def text_organno(file_path_box_dir,all_result):
    pass