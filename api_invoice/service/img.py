#!/usr/bin/env python3
#-*-encoding:utf-8-*-
#planA 通过长宽比例切出对应内容的图片
import cv2
import sys,os
import numpy as np
import threading
import img_process.utils.resize as resize
import img_process.utils.change as change
import img_process.utils.check as check
import img_process.utils.box as box
import api_common.utils.log as logger
import datetime
import threadpool
import time
import re
import PIL.Image as Image
#公共参数
import api_invoice.service.cardno as cardno_service
import api_invoice.service.organno as organno_service
import api_invoice.service.vinno as vinno_service
import api_invoice.service.engineno as engineno_service
import api_invoice.service.price as price_service

import api_invoice.dao.invoice_dao as invoice_dao
import api_invoice.dao.log_dao as log_dao
import tornado.httpclient
import json
import  math
import shutil

width=2048
def img_process(filepath,config):
    logger.debug(filepath)
    begin = datetime.datetime.now()
    data_dir =config["data_dir"]
    file_dir_img_root = data_dir
    img ={}
    re_str = '.*/(.*)\.(.*)'
    re_pat = re.compile(re_str)
    search_ret = re_pat.search(filepath)
    if search_ret:
        file_name = search_ret.groups()[0]
        file_suffix = search_ret.groups()[1]
        img = {}
        img['name'] = file_name
        img['suffix'] = file_suffix
        img['path'] = filepath
    file_name = img["name"]
    file_suffix = img["suffix"]
    # 原图
    file_path_src = file_dir_img_root + file_name + '.' + file_suffix

    pil_img = Image.open(file_path_src)
    if pil_img.size[0] * pil_img.size[1] < 480000:
        invoice_dao.update_error_status_by_id("图片分辨率太低,至少大于800*600", id)
        return
    file_path_src_copy = file_dir_img_root + file_name + '/000_src_copy' + file_name + '.' + file_suffix
    # 横竖调整图
    file_path_change_wh = file_dir_img_root + file_name + '/001_change_wh' + file_name + '.' + file_suffix
    # 检测发票表格图
    file_path_rect = file_dir_img_root + file_name + '/002_rect' + file_name + '.' + file_suffix
    # 大小调整
    file_path_resize = file_dir_img_root + file_name + '/003_resize' + file_name + '.' + file_suffix
    # 灰度二值图
    # file_path_gray = file_dir_img_root + file_name + '/gray' + file_name + '.' + file_suffix
    # 上下调整图
    file_path_change_tb = file_dir_img_root + file_name + '/004_change_tb' + file_name + '.' + file_suffix

    file_path_box_dir = file_dir_img_root + file_name + '/box'

    cv2.imwrite(file_path_src_copy, cv2.imread(file_path_src))
    # 横竖处理
    # change.change_wh(file_path_src, file_path_change_wh)

    # 上下重置
    # change.change_tb(file_path_resize,file_path_change_tb)
    # 矫正并抽出中心内容

    check_result = check.check_rect(file_path_src, file_path_rect)
    if check_result:
        area = check_result["all_area"]
        check_result_new = check.check_rect(file_path_rect, file_path_rect + "_new.jpg", level='simple')
        area_new = check_result_new["area"]
        """
        if area_new > area * 0.55:
            file_path_rect = file_path_rect + "_new.jpg"
            print("========= check_reck twice")
        print("===========area", area, area_new)
        """
    # 大小重置
    resize.resize(file_path_rect, file_path_resize, width)

    change.change_tb(file_path_resize, file_path_change_tb)

    result = {}
    result["info"] = {}
    result["log"] = {}
    result["debug"] = {}



    #get_text(cardno_service, file_path_resize, file_path_change_tb, file_name, file_path_box_dir, result)

    try:
        get_text(cardno_service, file_path_resize, file_path_change_tb, file_name, file_path_box_dir, result,file_dir_img_root)
    except Exception as e:
        print(e)
    info = result.get("info")

    result["file_path_src"] = file_path_src
    cardno = info.get("cardno")
    if not cardno:
        try:
            get_text(organno_service, file_path_resize, file_path_change_tb, file_name, file_path_box_dir,result,file_dir_img_root)
        except Exception as e:
            print(e)

    # vinno
    try:
        get_text(vinno_service, file_path_resize, file_path_change_tb, file_name, file_path_box_dir, result,file_dir_img_root)
    except Exception as e:
        print(e)

    # engineno
    try:
        get_text(engineno_service, file_path_resize, file_path_change_tb, file_name, file_path_box_dir, result,file_dir_img_root)
    except Exception as e:
        print(e)

    # price
    try:
        get_text(price_service, file_path_resize, file_path_change_tb, file_name, file_path_box_dir, result,
                 file_dir_img_root)
    except Exception as e:
        print(e)
    if "param" in result["info"]:
        result["info"].pop("param")
    end = datetime.datetime.now()
    result["time"]=(end-begin).seconds
    del_fields=[]
    for field in info:
        if "_default" in field:
            del_fields.append(field)
    for del_field in del_fields:
            del info[del_field]
    #logger.debug(result)
    return result


def get_text(service,file_path_resize,file_path_change_tb,file_name,file_path_box_dir,result,file_dir_img_root,level="simple"):
    file_src = os.path.join(file_dir_img_root,file_name+".jpg")
    # 图片正反
    page_top = result["debug"].get("page_top")
    # 正向
    im0 = result["debug"].get("im0")
    # 反向
    im1 = result["debug"].get("im1")
    #dk_line
    im2 = result["debug"].get("im2")

    # dk_src
    im3 = result["debug"].get("im3")
    text_str = None
    predict_type = None
    im_src = Image.open(file_src)
    # 机器学习
    if page_top == None:
        if not im0 and os.path.exists(file_path_resize):
            im0 = Image.open(file_path_resize)
            result["debug"]["im0"]=im0
        if im0:
            text_str = service.get_text_by_machine(im0, file_name, file_path_box_dir, 0, result)
        if (text_str == None):
            # 反向识别
            if not im1 and os.path.exists(file_path_change_tb):
                im1 = Image.open(file_path_change_tb)
                result["debug"]["im1"] = im1
            if im1:
                text_str = service.get_text_by_machine(im1, file_name, file_path_box_dir, 1, result)
            if text_str:
                predict_type = "machine_cvfind"
                page_top = 1
            else:
                if im2==None:
                    init_dk(result, file_path_box_dir, file_dir_img_root, file_name,is_src=True)
                    result["debug"]["im2"] = im_src
                    im2 = im_src
                text_str = service.get_text_by_machine(im_src, file_name, file_path_box_dir, 2, result,is_get_main_region=False)
                if text_str != None:
                    page_top = 2
                    predict_type = "machine_autofind_src"
                else:
                    if im3 == None:
                        init_dk(result, file_path_box_dir, file_dir_img_root, file_name,is_src=False)
                        im3=im_src
                        result["debug"]["im3"] = im_src
                    text_str = service.get_text_by_machine(im_src, file_name, file_path_box_dir, 3, result,
                                                           is_get_main_region=False)
                    if text_str != None:
                        page_top = 3
                        predict_type = "machine_autofind_turn"
        else:
            page_top = 0
            predict_type = "machine_cvfind"
    elif page_top == 0:
        text_str = service.get_text_by_machine(im0, file_name, file_path_box_dir, page_top, result)
    elif page_top == 1:
        text_str = service.get_text_by_machine(im1, file_name, file_path_box_dir, page_top, result)
    elif page_top == 2:
        text_str = service.get_text_by_machine(im2, file_name, file_path_box_dir, page_top, result,is_get_main_region=False)
    elif page_top == 3:
        text_str = service.get_text_by_machine(im3, file_name, file_path_box_dir, page_top, result,is_get_main_region=False)

    if (not text_str) and level in ["simple","normal","hard"]:
        text_str = get_text_by_tesseract(service, im0, im1,im2,im3, page_top, file_path_resize, file_path_change_tb, file_name,file_path_box_dir, result, 0,file_dir_img_root)
        if text_str:
            predict_type = "tesseract_cvfind_simple"

    if (not text_str) and level in ["normal","hard"]:
        text_str =get_text_by_tesseract(service, im0, im1,im2,im3, page_top, file_path_resize, file_path_change_tb, file_name,file_path_box_dir, result, 1,file_dir_img_root)
        if text_str:
            predict_type = "tesseract_cvfind_normal"
    if (not text_str) and level in ["hard"]:
        text_str =get_text_by_tesseract(service, im0, im1,im2,im3, page_top, file_path_resize, file_path_change_tb, file_name,file_path_box_dir, result, 2,file_dir_img_root)
        if text_str:
            predict_type = "tesseract_cvfind_hard"
    if predict_type:
        result["debug"]["predict_type_" + service.get_field_name()] = predict_type
    if result["debug"].get("page_top")==None:
        result["debug"]["page_top"]=page_top
    return text_str


def init_dk(result,file_path_box_dir,file_dir_img_root,file_name,is_src=False):
    try:
        file_src = file_dir_img_root + file_name
        line_path =file_src
        if not is_src:
            img = cv2.imread(file_src+".jpg")
            img = cv2.GaussianBlur(img, (3, 3), 0)
            edges = cv2.Canny(img, 30, 100, apertureSize=3)
            heidht = img.shape[0]
            # 经验参数
            minLineLength = heidht/10
            maxLineGap = heidht/50
            line_img = img.copy()
            lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 50, minLineLength, maxLineGap)
            max_line =None
            max_angle=0
            max_a=0
            max_b=0
            if not (lines is None):
                for line in lines:

                    for x1, y1, x2, y2 in line:
                        a =x2-x1
                        b = y2-y1
                        c = math.sqrt(pow(a, 2) + pow(b, 2))
                        angle = math.degrees(math.asin(b / c))
                        if angle>max_angle:
                            max_angle=angle
                            max_line=line
                            max_a=a
                            max_b=b

                """"""
                if not (max_line is None):
                    print(max_line)
                    for x1, y1, x2, y2 in max_line:
                        print(x1,y1,x2,y2)
                        cv2.line(line_img, (x1, y1), (x2, y2), (0, 255, 0), 2)


                line_path = os.path.join(file_src, "005_1_line_" + file_name)
                cv2.imwrite(line_path + ".jpg", line_img)
                #if max_a>max_b:
                #    max_angle+=270
                line_img = box.rotate_about_center(line_img,max_angle)
                #print("===angle=",angle)
            line_path = os.path.join(file_src, "005_line_"+file_name)
            cv2.imwrite(line_path+".jpg",line_img,[int(cv2.IMWRITE_JPEG_QUALITY), 100])
        url = "http://127.0.0.1:8088/dk?" + line_path;
        # url = "http://dk.autohome.com.cn/dk?" + file_dir_img_root + file_name;
        http_client = tornado.httpclient.HTTPClient()
        http_response = http_client.fetch(url)
        body = json.loads(http_response.body.decode())
        if body:
            body_result = body.get("result")
            if body_result:
                result["debug"]["dk"] = body_result
                dk = body_result
                make_dk_img(dk, file_path_box_dir, file_name, file_dir_img_root,is_src)
                return dk
    #except Exception as e:
    #    print(e)
    finally:
        pass




def get_text_by_tesseract(service,im0,im1,im2,im3,page_top,file_path_resize,file_path_change_tb,file_name,file_path_box_dir,result,level,file_dir_img_root):
    file_src = os.path.join(file_dir_img_root, file_name + ".jpg")
    if page_top == None:
        if not im0 and os.path.exists(file_path_resize):
            im0 = Image.open(file_path_resize)
            result["debug"]["im0"]=im0
        if im0:
            text_str = service.get_text_by_tesseract(im0, file_name, file_path_box_dir, 0, result,level)
        if not text_str:
            # 反向识别
            if not im1 and os.path.exists(file_path_change_tb):
                im1 = Image.open(file_path_change_tb)
                result["debug"]["im1"] = im1
            if im1:
                text_str = service.get_text_by_tesseract(im1, file_name, file_path_box_dir, 1, result,level)

            if text_str != None:
                page_top = 1
            else:
                if im2==None:
                    init_dk(result, file_path_box_dir, file_dir_img_root, file_name,is_src=True)
                    im2 = Image.open(file_src)
                    result["debug"]["im2"] = im2
                text_str = service.get_text_by_tesseract(im2, file_name, file_path_box_dir, 2, result,level)
                if text_str != None:
                    page_top = 2
                else:
                    if im3 == None:
                        init_dk(result, file_path_box_dir, file_dir_img_root, file_name,is_src=False)
                        im3 = Image.open(file_src)
                        result["debug"]["im3"] = im3
                    text_str = service.get_text_by_tesseract(im3, file_name, file_path_box_dir, 3, result, level)
                    if text_str:
                        page_top = 3

        else:
            page_top = 0
    elif page_top == 0:
        text_str = service.get_text_by_tesseract(im0, file_name, file_path_box_dir, page_top, result,level)
    elif page_top == 1:
        text_str = service.get_text_by_tesseract(im1, file_name, file_path_box_dir, page_top, result,level)
    elif page_top == 2:
        text_str = service.get_text_by_tesseract(im2, file_name, file_path_box_dir, page_top, result, level)
    elif page_top == 3:
        text_str = service.get_text_by_tesseract(im3, file_name, file_path_box_dir, page_top, result, level)

    if not result["debug"].get("page_top"):
        result["debug"]["page_top"] = page_top

    return text_str


def make_dk_img(rects,file_path_box_dir,file_name,file_dir_img_root,is_src):

    file_src = os.path.join(file_dir_img_root,file_name,"005_line_"+file_name+".jpg")
    dir_num="3"
    if is_src:
        file_src = os.path.join(file_dir_img_root, file_name+".jpg")
        dir_num = "2"
    im = Image.open(file_src)
    if rects:
        dk_dir = os.path.join(file_path_box_dir,dir_num)
        if not os.path.exists(dk_dir):
            os.makedirs(dk_dir)
            cv2_img = cv2.imread(file_src)
            for rect in rects:
                #print("===", rect)
                #rect = json.load(rect)
                #print("==json=",rect)
                class_name = rect.get("class_name")
                class_array = class_name.split("_")
                xmin = rect.get("xmin")
                xmax = rect.get("xmax")
                ymin = rect.get("ymin")
                ymax = rect.get("ymax")
                box_width = xmax - xmin
                box_height = ymax - ymin
                forward = class_array[2]
                if box_height > box_width and forward!='1' and forward!="3":
                    forward="1"
                if box_width>box_height and forward!="0" and forward!="2":
                    forward="0"
                angle = 0
                if forward == '1':
                    angle = 90
                if forward == '2':
                    angle = 180
                if forward == '3':
                    angle = 270








                field = class_array[1]
                if field == "idcard":
                    field = "cardno"
                if field == "engine":
                    field = "engineno"
                if field == "vin":
                    field = "vinno"

                if forward == '0':
                    xmax +=int((xmax-xmin)*0.04)
                if forward == '1':
                    ymax +=int((ymax-ymin)*0.04)
                if forward == '2':
                    xmin -= int((xmax-xmin)*0.04)
                if forward == '3':
                    ymin -= int((ymax - ymin) * 0.04)

                color = (0, 255, 0)

                cv2_img = cv2.rectangle(cv2_img, (xmin, ymin), (xmax, ymax), color, 2)
                cv2_img = cv2.putText(cv2_img, class_name, (xmax, ymin - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

                target_path = box.box(xmin,ymin,xmax,ymax,im,dk_dir,field)

                if angle != 0:
                    img = cv2.imread(target_path)
                    #cv2.imwrite(target_path+".src.jpg",img)
                    img = box.rotate_about_center(img,angle)
                    cv2.imwrite(target_path,img)
                    #cv2.imwrite(target_path + ".rotate.jpg", img)
                    #box.handleBorderImage(target_path)
                img = Image.open(target_path)
                region_width = img.size[0]
                region_height = img.size[1]
                new_region_width = region_width
                if field == "cardno":
                    new_region_width = 460
                if field == "engineno":
                    new_region_width = 300
                if field == "vinno":
                    new_region_width = 460
                if field == "price":
                    new_region_width = 400
                region_height = region_height * new_region_width // region_width
                region_width = new_region_width
                img = img.resize((region_width, region_height), Image.ANTIALIAS)
                if img.mode=="P":
                    target_path_png= target_path+".png"
                    img.save(target_path_png)
                    shutil.copy(target_path_png,target_path)
                else:
                    img.save(target_path)
            cv2.imwrite(file_src + ".rect.jpg", cv2_img)
    pass