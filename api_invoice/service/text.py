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
import api_common.utils.log as logger
import  pickle

import json

#处理横竖问题
tesseract_exe_name = '/usr/local/bin/tesseract' # Name of executable to be called at command line
cleanup_scratch_flag = True  # Temporary files cleaned up after OCR operation

py_dir = os.path.dirname(os.path.realpath(__file__))
project_dir = os.path.dirname(os.path.dirname(py_dir))
import train.predictapi as predictapi
param_config_file= project_dir+"/data/invoice/param_config.txt"
param_config_file_json= project_dir+"/data/invoice/param_config.js"
global param_store
global cardno_chars
param_store = {}
param_store_keys=[]
if os.path.exists(param_config_file):
    param_store = d = pickle.load(open(param_config_file, 'rb'))
    #logger.debug("param_store:", param_store)

if os.path.exists(param_config_file_json):
    with open(param_config_file_json, 'r') as f:
        jons_str = f.read()
        if jons_str !=None:
            param_store = json.loads(jons_str)
    #logger.debug("json param_store:", param_store)


def write_param_config():
    with open(param_config_file_json, 'w') as f:
        str = json.dumps(param_store)
        f.write(str)

global thread_list
thread_list={}
thread_value_list={}


def text_try(cardno_text_file,param1,param2,lan='eng',check=cardno):
    result =None
    logger.debug(param1, param2,cardno_text_file)
    text_str = get_text(cardno_text_file, "eng", param1=param1, param2=param2)
    logger.debug("ori:", text_str)
    cardno_str = check.process(text_str)
    logger.debug("new:", cardno_str)
    if check.check(cardno_str):
        result = cardno_str
        param_key = str(param1) + '_' + str(param2)
        param_data = param_store.get(param_key)
        if param_data == None:
            param_data={}
            param_data["param"]=[param1, param2]
            param_store[param_key] = param_data

    return result

def get_text(path_img_src,lan='chi_sim',param1=11,param2=3):
    #param1 = 11
    #param2 = 3
    bulid_file_path=path_img_src+'.bulid_'+str(param1)+'_'+str(param2)+'.jpg'
    if os.path.exists(bulid_file_path):
        os.remove(bulid_file_path)
    img = cv2.imread(path_img_src,0)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    newimg = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, param1, param2)

    cv2.imwrite(bulid_file_path, newimg)
    text = tesseract(bulid_file_path, lan)
    #text1 = tesseract(path_img_src, lan)
    return text

def get_gray_text(path_img_src,lan='chi_sim',):
    #param1 = 11
    #param2 = 3
    bulid_file_path=path_img_src+'.bulid_gray.jpg'
    if os.path.exists(bulid_file_path):
        os.remove(bulid_file_path)
    img = cv2.imread(path_img_src,0)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    #newimg = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, param1, param2)
    cv2.imwrite(bulid_file_path, img)
    text = tesseract(bulid_file_path, lan)
    #text1 = tesseract(path_img_src, lan)
    return text

def tesseract(path_img_src,lan='chi_sim'):
    #param1 = 11
    #param2 = 3
    proc = subprocess.Popen(tesseract_exe_name + ' ' + path_img_src + ' ' + path_img_src + ' -l '+ lan + ' >/dev/null 2>&1', shell=True)
    retcode = proc.wait()
    if retcode != 0:
        logger.debug(retcode)
        # errors.check_for_errors()
    text_file_path=path_img_src+'.txt'
    inf = open(text_file_path, 'r')
    text = inf.read()
    inf.close()
    if os.path.exists(path_img_src):
        pass
        #os.remove(path_img_src)
    if os.path.exists(text_file_path):
        os.remove(text_file_path)
    return text


def text_field_by_machine(img_box_file,check,all_result,field,model_args=("architecture_upper_number_","weights_upper_number_"),model_type=0,max_field_length=0,min_field_length=0,try_num=1):
    #return None
    """
    
    使用机器学习的方式进行识别
    :param img_box_file: :识别的图片路径(切割后的精确图片部位,字符在一个图上),加上[_dir]是分割之后的子图片目录
    :param check: 检测模块
    :param all_result: 总结果
    :param field: 字段
    :return: 识别结果
    """
    result = None
    if result ==None :
        dir_path = img_box_file + "_dir";
        box_list =os.listdir(dir_path)
        if not (box_list is  None):
            box_length = len(box_list)
            if max_field_length:
                if box_length>max_field_length*1.3:
                    return None
            if min_field_length:
                 if box_length<min_field_length:
                     return None
        else:
            return None
        for i in range(0,try_num):
            predict_textarray,predict_class = predictapi.predictObjects(model_args[0]+str(i)+".json",model_args[1]+str(i)+".h5",img_box_file+"_dir",model_type)
            if predict_textarray:
                predict_text = get_default_result_by_machine(predict_textarray,check,all_result,field)
                if not predict_text:
                    predict_text = get_result_by_machine("", predict_textarray, 0, check)
                    predict_text = check.process(predict_text)
                    if predict_text and check.check(predict_text):
                        result = predict_text
                        all_result["log"][field + "_type"] = "machine try"
                        all_result["info"][field] = result
                        logger.debug("==========", predict_text)
                else:
                    result = predict_text
                    all_result["info"][field] = result
                    all_result["log"][field + "_type"] = "machine"
                    break

    return result


def get_default_result_by_machine(predict_textarray,check,all_result,field):
    result=""
    for index in range(0,len(predict_textarray)):
        char_array = predict_textarray[index]
        if len(char_array)>0:
            char_text = char_array[0]["value"]
            probability = char_array[0]["probability"]
            if probability > 0.4:
                result += char_text
    process_text = check.process(result)
    print("====maching_text_default:" + result)
    all_result["debug"][field + "_machine_default"] = result
    if not check.check(process_text):
        process_text = None
    return process_text


def get_result_by_machine(pre_result,predict_textarray,index,check,index_str=""):
    result = pre_result
    array_length=len(predict_textarray)
    if index < array_length:
        char_array = predict_textarray[index]
        index += 1
        hava_text = 0

        if char_array:
            char_index = 0
            for char_text_obj in char_array:
                value = char_text_obj["value"]
                probability = char_text_obj["probability"]
                if probability > 0.5:
                    hava_text = 1
                    result += value
                    index_str += "["+str(char_index)+"]"
                    result = get_result_by_machine(result, predict_textarray, index, check,index_str)
                    process_text = check.process(result)
                    if result != None and check.check(process_text):
                        break
                char_index += 1
            pass
        if hava_text == 0:
            index_str += "[-1]"
            result += " "
            result = get_result_by_machine(result, predict_textarray, index, check,index_str)
    #print(result,index_str)
    return result




def text_field_by_tesseract(img_box_file,check,all_result,field,level=0):
    """
    使用tesseract进行识别
    1.原图
    2.灰图
    3.默认阈值
    4.历史阈值
    5.全部阈值
    :param img_box_file:  识别的图片路径(切割后的精确图片部位,字符在一个图上)
    :param check: 检测模块
    :param all_result: 总结果
    :param field: 字段
    :param level: 级别,0:[1,2,3],1:[4],2:[5]
    :return: 识别结果
    """
    result = None
    #tesseract整体识别
    min_param1 = 13
    max_param1 = 41
    min_param2 = 1
    max_param2 = 6
    param1 = 0
    param2 = 0
    file_index = 0
    param = all_result.get("param")
    if result == None and level == 0 :
        file_index =0
        tesseract_str = tesseract(img_box_file,"eng");
        info = all_result["info"]
        info[field + "_default"] = check.process(tesseract_str)
        if tesseract_str != None and check.check(info[field + "_default"]):
            result = info.get(field + "_default")
            all_result["log"][field + "_type"] = "tesseract src"
            info[field + "_default"] = ""
    if result == None and level == 0:
        file_index = 0
        tesseract_str = get_gray_text(img_box_file,lan='eng')
        info = all_result["info"]
        info[field + "_default"] = check.process(tesseract_str)
        if tesseract_str != None and check.check(info[field + "_default"]):
            all_result["log"][field + "_type"] = "tesseract gray"
            result = info[field + "_default"]
            info[field + "_default"]=""
    if result == None and level ==0:
        if param != None :
            param1 = param[0]
            param2 = param[1]
            result = text_try(img_box_file, param1, param2, lan='eng', check=check)
            if result:
                all_result["log"][field + "_type"] = "tesseract default param :"+str(param)

    if result == None and level ==1:
        file_index = 0
        if len(param_store) >0 :
            for param_data in param_store.values():
                param1=param_data['param'][0]
                param2=param_data['param'][1]
                result = text_try(img_box_file, param1, param2, lan='eng',check=check)
                if not result == None:
                    all_result["log"][field + "_type"] = "tesseract stor param:"+str(param_data['param'])
                    break
    if result==None and level == 2:
        param1 = min_param1
        param2 = min_param2
        while (param1 <= max_param1):
            while (param2 <= max_param2):
                param2 += 1
                param_key = str(param1) + '_' + str(param2)
                param_data = param_store.get(param_key)
                if param_data != None :
                    continue
                result = text_try(img_box_file,param1,param2,lan='eng',check=check)
                if not result == None:
                    all_result["log"][field + "_type"] = "tesseract all param:" + str([param1,param2])
                    break

            param1 += 4
            param2 = min_param2
            if not result == None:
                break
    if result!=None:
        all_result["info"][field] = result
        all_result["debug"][field + "_tesseract_default"] = result
        logger.info("========page_top",all_result.get("page_top"),result)
    if result == None:
        all_result["debug"][field + "_tesseract_default"] = tesseract_str
    if param1>0 and param2 >0:
        param = [param1, param2]
        all_result["param"]=param

    return result