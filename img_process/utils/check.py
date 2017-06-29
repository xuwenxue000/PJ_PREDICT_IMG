#!/usr/bin/env python3
#-*-encoding:utf-8-*-

import os,sys
from PIL import Image
import subprocess
import api_common.utils.log as logger
import cv2
import numpy as np
import shutil
#处理横竖问题

default_params={
    "11_3": {"param": [11, 3]},
    #"13_1": {"param": [13, 3]},
    #"29_1": {"param": [29, 3]},


}

min_param1 = 5
max_param1 = 35
min_param2 = 0
max_param2 = 5
def check_rect(src_path,out_path,level='simple'):
    if os.path.exists(out_path):
        os.remove(out_path)
    result = None
    max_area = 0
    max_params = None
    max_result = None
    if level == 'simple' or level == 'hard':
        for params_key in default_params.keys():
            param1 = default_params[params_key]["param"][0]
            param2 = default_params[params_key]["param"][1]
            result_temp = check_try(src_path, out_path+"_"+str(param1)+"_"+str(param2)+'.jpg', param1, param2)
            area = result_temp["area"]
            all_area = result_temp["all_area"]
            if area > max_area:
                max_params = [param1, param2]
                max_area = area
                max_result = result_temp

            #if area > all_area*0.4 :
                #shutil.copy(out_path+"_"+str(param1)+"_"+str(param2)+'.jpg',out_path)
                #print(out_path + "_" + str(param1) + "_" + str(param2) + '.jpg')
                #result=result_temp
                #break

    if not result and level == 'hard':
        param1 = min_param1
        param2 = min_param2
        while param1 <= max_param1:
            while param2 <= max_param2:
                param2 += 1
                param_key = str(param1) + '_' + str(param2)
                param_data = default_params.get(param_key)
                if param_data:
                    continue
                result_temp = check_try(src_path, out_path + "_" + str(param1) + "_" + str(param2) + '.jpg', param1, param2)
                area = result_temp["area"]
                all_area = result_temp["all_area"]
                if area >max_area:
                    max_params = [param1,param2]
                    max_area = area
                    max_result = result_temp
                #if area > all_area * 0.4:
                #    #shutil.copy(out_path + "_" + str(param1) + "_" + str(param2)+'.jpg', out_path)
                #    print(str(param1) + "_" + str(param2))
                #    result = result_temp
                #    break
            param1 += 4
            param2 = min_param2
            if result:
                break
    if not result:
        result = max_result
        print("area param:",max_area,result["all_area"],max_params)
    if result:
        img = result["img"]
        c = result["c"]
        img_height = img.shape[0]
        img_width = img.shape[1]
        (x, y, w, h) = cv2.boundingRect(c)
        if h > w:
            # M = cv2.getRotationMatrix2D((img_height/2,img_width/2), 90, 1)
            pts1 = np.float32([[0, 0], [img_width, 0], [0, img_height]])
            pts2 = np.float32([[img_width, 0], [img_width, img_height], [0, 0]])
            M = cv2.getAffineTransform(pts1, pts2)
            img = cv2.warpAffine(img, M, (img_width, img_height))
            img = cv2.resize(img, (img_height, img_width), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(out_path, img)
        cv2.imwrite(out_path + "_test.jpg", result_temp["img_new"])
    return result


def check_try(src_path,out_path,param1,param2):
    out_dir_path = os.path.dirname(out_path)
    if not os.path.exists(out_dir_path) :
        os.makedirs(out_dir_path)

    img = cv2.imread(src_path)

    img_new = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #img_new = cv2.copyMakeBorder(img_new, 5, 5, 5, 5, cv2.BORDER_CONSTANT, value=(255, 255, 255))
    img_new = cv2.copyMakeBorder(img_new, 5, 5, 5, 5, cv2.BORDER_REPLICATE)
    #logger.info(avg_gray_1,avg_gray_2)
    #logger.info(param1,param2)
    kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    #img_new = cv2.morphologyEx(img_new, cv2.MORPH_OPEN, kernel2)
    img_new = cv2.adaptiveThreshold(img_new, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, param1, param2)
    img_new = cv2.morphologyEx(img_new, cv2.MORPH_OPEN, kernel2)
    image, cnts, hierarchy = cv2.findContours(img_new, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    img_new = cv2.cvtColor(img_new, cv2.COLOR_GRAY2RGB)
    area_map = {}
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        area = cv2.contourArea(c)
        area_map[area]=c
    sort_keys = sorted(area_map.keys())
    min_x_y = 10000000
    max_x_y = -1
    max_x = -10000000
    max_y = -10000000

    LT_point = -1
    RB_point = -1
    RT_point = -1
    LB_point = -1
    area = 0
    c=None
    for i in range(-2, -1):
        area = sort_keys[i]
        c = area_map.get(sort_keys[i])
        for cc in c:
            # logger.debug(cc)
            x = cc[0][0]
            y = cc[0][1]
            if x + y < min_x_y:
                min_x_y = x + y
                LT_point = [x, y]
            if x + y > max_x_y:
                max_x_y = x + y
                RB_point = [x, y]
            if x - y > max_x:
                max_x = x - y
                RT_point = [x, y]
            if y - x > max_y:
                max_y = y - x
                LB_point = [x, y]

        img_new=cv2.drawContours(img_new, c, -1, (0, 255, 0), 10)

    #logger.debug(LT_point, LB_point, RT_point, RB_point)
    if os.path.exists(out_path+'test.jpg'):
        os.remove(out_path+'test.jpg')
    cv2.imwrite(out_path+'test.jpg', img_new)
    height, width, channels = img.shape
    try:

        pts1 = np.float32([LT_point, RT_point, LB_point, RB_point])
        pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
        PerspectiveMatrix = cv2.getPerspectiveTransform(pts1, pts2)
        img = cv2.warpPerspective(img, PerspectiveMatrix, (width, height))
        #area = cv2.contourArea(img)
        #cv2.imwrite(out_path, img)
    #except Exception as err:
    #    pass
    finally:
        pass
    result = {}
    result["area"] = (LB_point[1]-LT_point[1])*(RB_point[0]-LB_point[0])
    result["all_area"] = height * width
    result["img"] = img
    result["img_new"] = img_new
    result["c"] = c
    #print(result["area"],result["all_area"],area/(height * width))
    return result



"""
    if avg_gray_1>100 and avg_gray_1 < 110 and  avg_gray_2 >40 and avg_gray_2 < 45:
        #test_name.append("22095360-8730-425b-2e1b-n204a2hbbkh1")
        param1 = 9
        param2=5
    if avg_gray_1 > 110 and avg_gray_1 < 120 and avg_gray_2 > 25 and avg_gray_2 < 30:
        #test_name.append("32115380-7378-1bml-b6m1-n202atcfcedb")
        param1 = 17
        param2 =3
    if avg_gray_1 > 110 and avg_gray_1 < 120 and avg_gray_2 > 55 and avg_gray_2 < 60:
        #test_name.append("41586520-7668-chbe-1gce-n204abm4cf7d")
        param1 = 19
        param2 = 3
    if avg_gray_1>120 and avg_gray_1 < 130 and  avg_gray_2 >25 and avg_gray_2 < 30:
        param1 = 13
        param2=3
    if avg_gray_1>120 and avg_gray_1 < 130 and  avg_gray_2 >35 and avg_gray_2 < 40:
        #test_name.append("17272160-7352-b3fm-ng24-n202a5nf69bm")
        param1 = 11
        param2=4
    if avg_gray_1 > 130 and avg_gray_1 < 140 and avg_gray_2 > 10 and avg_gray_2 < 15:
        #51293840-7829-1meb-1e17-n204abd3hl5l
        param1 = 99
        param2 = 3
    if avg_gray_1>150 and avg_gray_1 < 160 and  avg_gray_2 >20 and avg_gray_2 < 25:
        #test_name.append("28215270-6525-kt4t-gbnb-n204a3t47dtf")
        param1 = 33
        param2=3
    if avg_gray_1 > 150 and avg_gray_1 < 160 and avg_gray_2 > 25 and avg_gray_2 < 30:
        #51026630-7828-3gln-7t8t-n204acc9ggel
        param1 = 27
        param2 = 3
    if avg_gray_1 > 170 and avg_gray_1 < 180 and avg_gray_2 > 25 and avg_gray_2 < 30:
        #test_name.append("48049350-7428-37ed-7gh7-n204ahg3t79e")
        param1 = 11
        param2 = 5
    if avg_gray_1>170 and avg_gray_1 < 180 and  avg_gray_2 >40 and avg_gray_2 < 50:
        param1 = 11
        param2=5
"""