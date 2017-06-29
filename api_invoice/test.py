#-*-encoding:utf-8-*-
import os,sys
from PIL import Image
import subprocess
import cv2
import numpy as np
import threading

py_dir = os.path.dirname(os.path.realpath(__file__))
project_dir = os.path.dirname(py_dir)
sys.path.append(project_dir)
import img_process.utils.resize as resize
import api_invoice.utils.data as data
import img_process.utils.change as change
import img_process.utils.check as check
import api_invoice.service.text as text
import api_common.utils.log as logger
import datetime
import threadpool
import time
import shutil
import uuid
import api_invoice.service.cardno as cardno_service
import api_invoice.service.vinno as vinno_service
import api_invoice.service.organno as organno_service
import api_invoice.service.engineno as engineno_service
import api_invoice.service.price as price_service
import api_invoice.service.img as img_service
import api_invoice.config.profile as profile_config
import api_invoice.dao.invoice_dao as invoice_dao
import api_invoice.dao.log_dao as log_dao
##入口初始化
## 设置profile
profile_config.profile.set_profile(sys.argv[0])

import tensorflow as tf
from keras.backend.tensorflow_backend import set_session
config = tf.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.3
set_session(tf.Session(config=config))

#公共参数
py_dir = os.path.dirname(os.path.realpath(__file__))
project_dir = os.path.dirname(py_dir)

img_file= project_dir+"/data/invoice/img.txt"
result_file= project_dir+"/data/invoice/result.txt"

file_dir_img_root = project_dir+"/data/invoice/img/"
file_dir_img_error_root = project_dir+"/data/invoice/img_error/"
file_dir_img_tesseract_root = project_dir+"/data/invoice/img_tesseract/"

if not os.path.exists(file_dir_img_root):
    os.mkdir(file_dir_img_root)

if not os.path.exists(file_dir_img_error_root):
    os.mkdir(file_dir_img_error_root)
else :
    shutil.rmtree(file_dir_img_error_root)
    os.mkdir(file_dir_img_error_root)

if not os.path.exists(file_dir_img_tesseract_root):
    os.mkdir(file_dir_img_tesseract_root)
else :
    shutil.rmtree(file_dir_img_tesseract_root)
    os.mkdir(file_dir_img_tesseract_root)
test_name=[]

#test_name.append("111")
#test_name.append("autohomecar__wKjBwlgmeSaAJrTHAAG-BeYqJoM741")


#test_name.append("41586520-7668-chbe-1gce-n204abm4cf7d")
#test_name.append("04005040-7417-41d5-be2d-n203a829dmge")
#test_name.append("autohomecar__wKjBw1b7NFaAWJkvAAKAyzSQbeo282")
#test_name.append("autohomecar__wKjBw1g9EPOAEIgFAAHQVHt-NE8287")
#test_name.append("autohomecar__wKjBzFghLxiAN0CnADRxl7NnxJE096")
#test_name.append("01362710-8011-h74m-622d-n204afcc45mt")






muilti_thread = False





width =2048
exclude=[]
target_path = project_dir + "/tmp_predict/test3"
if os.path.exists(target_path):
    shutil.rmtree(target_path)
    os.mkdir(target_path)


target_path_error_char = project_dir + "/tmp_predict/error_char"
if os.path.exists(target_path_error_char):
    shutil.rmtree(target_path_error_char)
    os.mkdir(target_path_error_char)

target_path4 = project_dir + "/tmp_predict/test4"
if os.path.exists(target_path4):
    shutil.rmtree(target_path4)
    os.mkdir(target_path4)
else :
    #os.mkdir(target_path4)
    pass

mydateset_base_dir = "/home/autoai/mydataset/original/"

mydateset_base_dir2 = os.path.join(project_dir,"data/invoice/temp")
print("====mydateset_base_dir====",mydateset_base_dir)

def img_process(img):
    begin = datetime.datetime.now()
    id = img["id"]
    path = img["path"]
    file_name = img["name"]
    file_suffix = img["suffix"]
    #file_suffix='jpg'
    if (test_name == None or file_name in test_name or len(test_name) == 0):
        file_path_resize=None

        # 原图
        try:
            file_path_src = file_dir_img_root + file_name + '.' + file_suffix

            pil_img = Image.open(file_path_src)
            if pil_img.size[0]*pil_img.size[1]<480000:
                invoice_dao.update_error_status_by_id("图片分辨率太低,至少大于800*600",id)
                return
            file_path_src_copy = file_dir_img_root + file_name + '/000_src_copy' + file_name + '.' + file_suffix
            # 横竖调整图
            file_path_change_wh = file_dir_img_root + file_name + '/001_change_wh' + file_name + '.' + file_suffix
            # 检测发票表格图
            file_path_rect = file_dir_img_root + file_name + '/002_rect' + file_name + '.' + file_suffix
            # 大小调整
            file_path_resize = file_dir_img_root + file_name + '/003_resize' + file_name + '.' + file_suffix
            # 灰度二值图
            #file_path_gray = file_dir_img_root + file_name + '/gray' + file_name + '.' + file_suffix
            # 上下调整图
            file_path_change_tb = file_dir_img_root + file_name + '/004_change_tb' + file_name + '.' + file_suffix



            file_path_box_dir = file_dir_img_root + file_name + '/box'

            cv2.imwrite(file_path_src_copy, cv2.imread(file_path_src))
            # 横竖处理
            #change.change_wh(file_path_src, file_path_change_wh)

            # 上下重置
            # change.change_tb(file_path_resize,file_path_change_tb)
            # 矫正并抽出中心内容

            check_result = check.check_rect(file_path_src, file_path_rect)
            """
            if check_result:
                area = check_result["all_area"]
                check_result_new =check.check_rect(file_path_rect, file_path_rect+"_new.jpg",level='simple')
                if check_result_new:
                    area_new = check_result_new["area"]
                    if area_new > area*0.55:
                        file_path_rect = file_path_rect+"_new.jpg"
                        print("========= check_reck twice")
                    print("===========area",area,area_new)
            """
            # 大小重置
            resize.resize(file_path_rect, file_path_resize, width)

            change.change_tb(file_path_resize, file_path_change_tb)
        except Exception as e:
            print(e)
        finally:
            pass

        result = {}
        result["info"] = {}
        result["log"] = {}
        result["debug"] = {}
        info = result.get("info")

        try:
            if (file_path_resize):
                img_service.get_text(cardno_service,file_path_resize,file_path_change_tb,file_name,file_path_box_dir,result,file_dir_img_root)
        #except Exception as e:
        #    print(e)
        finally:
            pass

        cardno = info.get("cardno")
        #if cardno:
        #    invoice_dao.update_idcardno_by_id(cardno,id)
        #机构代码识别
        if not cardno:
            try:
                if (file_path_resize):
                    img_service.get_text(organno_service, file_path_resize, file_path_change_tb, file_name, file_path_box_dir,
                                 result,file_dir_img_root)
            except Exception as e:
                print(e)
            #if organno:
                #invoice_dao.update_roganno_by_id(organno, id)
        organno = info.get("organno");
        try:
            if (file_path_resize):
                img_service.get_text(vinno_service, file_path_resize, file_path_change_tb, file_name, file_path_box_dir,result,file_dir_img_root)
        except Exception as e:
            print(e)
        finally:
            pass
        vinno = info.get("vinno");
        #if vinno:
            #invoice_dao.update_vin_by_id(vinno, id)

        try:
            if (file_path_resize):
                img_service.get_text(engineno_service, file_path_resize, file_path_change_tb, file_name, file_path_box_dir, result,
                     file_dir_img_root)
        except Exception as e:
            print(e)
        engineno = info.get("engineno");
        if engineno:
            #invoice_dao.update_engineno_by_id(engineno, id)
            build_check_char_img("engineno", info, result)



        try:
            if (file_path_resize):
                img_service.get_text(price_service, file_path_resize, file_path_change_tb, file_name, file_path_box_dir, result,
                     file_dir_img_root)
        except Exception as e:
            print(e)

        price = info.get("price");
        if price:
            #invoice_dao.update_price_by_id(price, id)
            build_check_char_img("price", info, result)
        if not cardno:
            invoice_dao.update_unknow_status_by_id(id)
        end = datetime.datetime.now()
        #predict_time =(end - begin).microseconds//1000
        predict_time =(end - begin).seconds
        predict_type_idcard = result["debug"].get("predict_type_cardno")
        invoice_dao.update_invoice_by_id(id,idcard=cardno,vin=vinno,organ=organno,engine=engineno,price=price,predict_time=predict_time,predict_type_idcard=predict_type_idcard)

        out_result = {}
        out_result["time"] = predict_time
        invoice_dao.update_predict_time_by_id(out_result["time"], id)
        out_result["file_name"] = file_name
        out_result["info"] = result["info"]
        #out_result["cardno_machine_default"] = cardno_machine_default
        out_result["log"] = result["log"]

        out_result["page_top"] = result["debug"].get("page_top")
        log_dao.info(str(out_result),"invoice",img["id"])
        with open(result_file, 'a') as f:
            f.write(str(out_result)+"\n")
        thread = threading.current_thread()
        t=thread_list.get(thread.name)
        if t!=None:
            thread_list.pop(thread.name)


def build_check_char_img(field_name,info,result,server_char_dir="upper_201706",server_number_dir="number_201706",server_signal_dir="signal_201706",char_set="ABCDEFGHIJKLMNOPQRSTUVWXYZ",num_set="0123456789",signal_set=".¥-"):
    target_mydateset_base_dir=mydateset_base_dir
    if not os.path.exists(target_mydateset_base_dir):
        target_mydateset_base_dir =mydateset_base_dir2
    server_char_path = os.path.join(target_mydateset_base_dir,server_char_dir)
    if not os.path.exists(server_char_path):
        os.makedirs(server_char_path)
    server_number_path = os.path.join(target_mydateset_base_dir,server_number_dir)
    if not os.path.exists(server_number_path):
        os.makedirs(server_number_path)
    server_signal_path = os.path.join(target_mydateset_base_dir,server_signal_dir)
    if not os.path.exists(server_signal_path):
        os.makedirs(server_signal_path)
    field = info.get(field_name);
    field_file = result.get(field_name+"_file")
    logger.info("=============="+field_name+","+field_name+"_file", field, field_file)
    if field_file and field:
        text_type = result["log"][field_name+"_type"]
        if text_type.startswith("tesseract"):
            target_dir = file_dir_img_tesseract_root + file_name + "_"+field_name
            if os.path.exists(target_dir):
                shutil.rmtree(target_dir)
                # os.mkdir(target_dir)
            else:
                pass
                # os.mkdir(target_dir)
            shutil.copytree(file_dir_img_root + file_name, target_dir)
        img_src_name = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(field_file))))
        box_dir = field_file + "_dir"
        box_src_dir = field_file + "_dir_src"
        logger.debug("=============="+field+",box_dir", field, box_dir)
        if os.path.exists(box_dir):
            files = os.listdir(box_dir)
            files_len = len(files)
            logger.info("=============", files_len, len(field), field, files)
            if files_len == len(field):
                logger.info("============= build box img :" + field)
                value = field
                for i in range(0, len(field)):
                    char_text = field[i]
                    try:
                        if char_text in num_set:
                            if os.path.exists(server_number_path):
                                shutil.copyfile(box_src_dir + "/" + str(i).zfill(3) + ".jpg",
                                                server_number_path + "/" + char_text + "_" + str(i).zfill(
                                                    3) + "_" + value + "_" + img_src_name + ".jpg")
                            pass
                        if char_text in char_set:
                            if os.path.exists(server_char_path):
                                shutil.copyfile(box_dir + "/" + str(i).zfill(3) + ".jpg",
                                                server_char_path + "/" + char_text + "_" + str(i).zfill(
                                                    3) + "_" + value + "_" + img_src_name + ".jpg")
                        if char_text in signal_set:
                            if os.path.exists(server_signal_path):
                                shutil.copyfile(box_dir + "/" + str(i).zfill(3) + ".jpg",
                                                server_signal_path + "/" + char_text + "_" + str(i).zfill(
                                                    3) + "_" + value + "_" + img_src_name + ".jpg")
                                pass
                    # except Exception as e:
                    #    logger.error("======:Exception:",e)
                    #    pass
                    finally:
                        pass
            else:
                logger.warn("================file and dada is diff================")
    else:
        target_dir = file_dir_img_error_root + file_name + "_"+field
        if os.path.exists(target_dir):
            shutil.rmtree(target_dir)
            # os.mkdir(target_dir)
        else:
            pass
            # os.mkdir(target_dir)
        shutil.copytree(file_dir_img_root + file_name, target_dir)
        pass
        # engineno




if os.path.exists(result_file):
    os.remove(result_file)
global thread_list
thread_list ={}


index = 0


def get_target_imgs():
    if len(test_name) == 0:
        # 读取图片列表
        imgs = data.getimgs(img_file, file_dir_img_root)
    else:
        muilti_thread = False
        if os.path.exists(file_dir_img_root):
            shutil.rmtree(file_dir_img_root)
            os.mkdir(file_dir_img_root)
        imgs = data.get_by_filenames(test_name, file_dir_img_root)
    target_imgs = []
    if imgs:
        for img in imgs:
            file_name = img["name"]
            # print(file_name)
            if file_name in exclude:
                # break
                pass
            else:
                file_path_src_dir = file_dir_img_root + file_name
                # print(file_path_src_dir)
                if os.path.exists(file_path_src_dir):
                    shutil.rmtree(file_path_src_dir)

                file_suffix = img["suffix"]
                if not test_name or len(test_name) == 0:
                    target_imgs.append(img)
                elif file_name in test_name:
                    target_imgs.append(img)
    return target_imgs

target_imgs = get_target_imgs()

if muilti_thread:
    pool = threadpool.ThreadPool(40)
    requests = threadpool.makeRequests(img_process, target_imgs)
    [pool.putRequest(req) for req in requests]
    pool.wait()
else :
    while target_imgs and len(target_imgs)>0:
        imgs_len = len(target_imgs)
        for img in target_imgs:
            index += 1
            path = img["path"]
            file_name = img["name"]
            print("=======begin=====================", index, "/", imgs_len,"[",img["id"],"]", file_name)
            img_process(img)
            print("=======end=====================", index, "/", imgs_len,"[",img["id"],"]")
        if len(test_name) == 0:
            target_imgs = get_target_imgs()
        else :
            break
text.write_param_config()


