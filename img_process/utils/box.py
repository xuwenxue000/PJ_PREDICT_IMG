#!/usr/bin/env python3
#-*-encoding:utf-8-*-
#planA 通过长宽比例切出对应内容的图片
import os,sys
from PIL import Image
import subprocess
import cv2
import numpy as np
import shutil
py_dir = os.path.dirname(os.path.realpath(__file__))
project_dir = os.path.dirname(os.path.dirname(py_dir))
import cv2
import PIL.Image as Image
import numpy as np
import matplotlib
import math

def box(xmin,ymin,xmax,ymax,im,target_dir,filename):
    target_path=target_dir + '/' + filename + '.jpg'
    if os.path.exists(target_path):
        return target_path
        #os.remove(target_path)
    box = (xmin,ymin,xmax,ymax)
    #box = (0, 0, 100, 100)

    region = im.crop(box)
    #region.show()
    if region.mode =="P":
        target_path_png = target_dir + '/' + filename + '.png'
        region.save(target_path_png)
        shutil.copy(target_path_png,target_path)
    else:
        region.save(target_path)
    #print("boxpath:",target_path)
    return target_path

def get_region_row(img,h,img_src,method,file_path,step_row=1,space_row=20,key_region=True):
    #img = img.convert('L')
    img_cv2 = cv2.imread(file_path)
    width = img.size[0]
    height = img.size[1]
    y = 0
    rows = []
    rows_gray_sum = 0

    while y + step_row < height:
        row_num = {}
        row_num["y"] = y
        box = (0, y, width, y + step_row)
        region = img.crop(box)
        target_dev = cv2.meanStdDev(np.array(region))
        target_gray_avg = target_dev[0][0][0]
        row_num["num"] = target_gray_avg
        rows_gray_sum += pow(target_gray_avg,1)
        rows.append(row_num)
        y += step_row
    #print(rows)
    rows2 = []
    min_dev = 255
    result = None
    result_list=[]
    if method=='find_valley':
        #使用波谷计算
        rows = find_valley(rows,space_row)
        row_index = 0
        while row_index < len(rows) - 1:
            row = rows[row_index]
            row_num = row["num"]
            row_y = row["y"]
            # print(col, cols_gray_avg)
            row2 = {}
            row2["begin"] = row_y
            row2["end"] = rows[row_index + 1]["y"]
            space = row2["end"] - row2["begin"]
            # print(space)
            if space > h:
                rows2.append(row2)
            """
            if space < h and row_index < len(rows) - 2:

                row_index_next = row_index + 1
                row__next = rows[row_index_next]
                row_next_x = row__next["y"]
                row_next_next_x = rows[row_index_next + 1]["y"]
                # print(space, ":", w, col_index,col_next_next_x,x)
                if row_next_next_x - row_next_x < h:
                    # print(space,":",w,col_index)
                    row2["end"] = rows[row_index + 2]["y"]
                    row_index += 1
            """

            row_index += 1
        #print(rows)
        #print(rows2)
    if method == 'find_peaks':
        # 使用波峰计算
        rows = find_peaks(rows, space_row)
        #print("find_peaks====:"+str(rows))
        row_index = 0
        while row_index < len(rows) - 1:

            row = rows[row_index]
            row_num = row["num"]
            row_y = row["y"]
            # print(col, cols_gray_avg)
            row2 = {}
            row2["begin"] = row_y
            if row_index >=len(rows)-1:
                row2["end"] = height
            else:

                row2["end"] = rows[row_index + 1]["y"]
            space = row2["end"] - row2["begin"]
            # print(space)
            if space > h:
                rows2.append(row2)
            """  
            row = rows[row_index]
            row_y = row["y"]
            row2 = {}
            row2["begin"]=0
            left = row_y-h
            right = row_y+h
            img_height = img.size[1]
            #print("left,right,h,h*1.2:",left,right,h,h*1.2)
            if img_height > h*2:
                if left > 0 and right < img_height:
                    row2["begin"] = left
                    row2["end"] = right
                if left > 0 and right > img_height:
                    #row2["begin"] = img_height-h*1.2
                    row2["begin"] = left
                    row2["end"] = img_height
                if left < 0 and right <img_height:
                    row2["begin"] = 0
                    #row2["end"] = h*1.2
                    row2["end"] = right

            else:
                row2["begin"] = 0
                row2["end"] = img_height
            #space = row2["end"] - row2["begin"]
            # print(space)
            rows2.append(row2)
            """
            row_index += 1
    if method == 'find_gray_avg':
        #使用平均灰度计算
        rows_gray_avg = rows_gray_sum*1.005 / len(rows)
        for row in rows:
            row_num = pow(row["num"],1)
            row_y = row["y"]
            if row_num < rows_gray_avg:
                row2_len = len(rows2)
                if row2_len == 0:
                    row2 = {}
                    row2["begin"] = row_y
                    row2["end"] = row_y + step_row
                    rows2.append(row2)
                else:
                    last_row = rows2[row2_len - 1]
                    last_row_end = last_row["end"]
                    if row_y == last_row_end:
                        last_row["end"] = row_y + step_row
                    else:
                        row2 = {}
                        row2["begin"] = row_y
                        row2["end"] = row_y + step_row
                        rows2.append(row2)

    #print(rows)
    #print(rows2)
    max_box_height=0
    for row in rows2:
        row_begin = row["begin"]
        row_end = row["end"]
        if row_end - row_begin < h:
            continue
            #pass
        if row_begin-h*13//20 > 0:
            row_begin = row_begin-h*13/20
        else :
            row_begin = 0
        #print(img.size)
        if row_end+h*13//20<img.size[1]:
            row_end= row_end+h*13//20
        else :
            row_end = img.size[1]
        box = (0, row_begin, width, row_end)
        region = img.crop(box)
        region_cvimg = np.array(region)
        now_row_height = row_end - row_begin
        if now_row_height >max_box_height:
            max_box_height = now_row_height
            result = region
            cv2.rectangle(img_cv2, (0, row["begin"]), (width, row["end"]), (255, 0, 0))

        """
        dev =cv2.meanStdDev(region_cvimg)
        avg_gray =dev[0][0][0]
        result_list.append(region)
        #print(min_dev,avg_gray)
        if avg_gray < min_dev:
            min_dev = avg_gray
            result = region
            #cv2.rectangle(cv2_img, (0, row["begin"]), (width, row["end"]), (255, 0, 0))
        """
    if not key_region:
        result = result_list
    if result==None:
        result=img
    #result.show()
    cv2.imwrite(file_path+"rect.jpg",img_cv2)
    return result


def box_step(img_src, w, h, step_row=1, step_col=1,letter_pace=14,row_space=25, is_process_link=True,is_get_main_region=True,try_num=''):
    """

    :param img_src: 原图地址
    :param w: 切割结果的宽
    :param h: 切割结果的高
    :param step: 递进的大小
    :return: 
    """

    # 按照递进值进行灰度分析
    x = 0
    y = 0
    #print(rows)
    #print(rows2)


    #去除横向线条
    cv2_img = cv2.imread(img_src)
    """
    lut = np.zeros(256, dtype=cv2_img.dtype)  # 创建空的查找表
    hist, bins = np.histogram(cv2_img.flatten(), 256, [0, 256])
    cdf = hist.cumsum()  # 计算累积直方图
    cdf_m = np.ma.masked_equal(cdf, 0)  # 除去直方图中的0值
    cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf_m.max() - cdf_m.min())  # 等同于前面介绍的lut[i] = int(255.0 *p[i])公式
    cdf = np.ma.filled(cdf_m, 0).astype('uint8')  # 将掩模处理掉的元素补为0
    
    # 计算
    #cv2_img = cdf[cv2_img]
    cv2_img = cv2.LUT(cv2_img, cdf)

    #cv2.cvtColor(cv2_img,cv2.COLOR_BGR2GRAY)
    cv2.imwrite(img_src,cv2_img)
    cv2_img = cv2.imread(img_src)
    #cv2_img = cv2.Laplacian(cv2_img,cv2.CV_8UC4)
    cv2.cvtColor(cv2_img, cv2.COLOR_BGR2GRAY)
    """



    target_dev = cv2.meanStdDev(cv2_img)
    target_gray_avg = target_dev[0][0][0]+1
    #target_gray_avg = 255

    cv2_img = cv2.GaussianBlur(cv2_img, (3, 3), 0)
    edges = cv2.Canny(cv2_img, 40, 80, apertureSize=3)
    #lines = cv2.HoughLines(edges, 1, np.pi / 180, 118)
    minLineLength = 100
    maxLineGap = 40
    line_img = cv2_img.copy()
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 80, minLineLength, maxLineGap)
    if (lines is not None) and (len(lines) > 0):
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_img, (x1, y1), (x2, y2), (target_gray_avg,target_gray_avg,target_gray_avg), 8)
    cv2.imwrite(img_src,line_img)
    cv2.imwrite(img_src+".line.jpg",line_img)

        #img.show()
    img = Image.open(img_src)
    region = img
    #region = get_region_row(region, h,img_src,"find_peaks", step_row, row_space)
    #region.save(img_src + "_row1.jpg")
    #region = get_region_row(region, h,img_src,"find_valley", step_row, row_space)
    #region.save(img_src + "_row2.jpg")
    if is_get_main_region:
        region = get_region_row(region, h,img_src,"find_gray_avg", img_src,step_row, row_space)
    #region = get_region_row(region, h,img_src,"find_gray_avg", step_row, row_space)
    region.save(img_src + "_row3.jpg")
    #region = get_region_row(region,h,img_src,step_row,row_space)
    #region.show()
    #region = get_region_row(region, h, step_row, row_space)


    img.save(img_src+"_src.jpg")
    img_src = img_src + "_result"+str(try_num)+".jpg"

    if not os.path.exists(img_src + "_dir"):
        os.mkdir(img_src + "_dir")
    else:
        shutil.rmtree(img_src + "_dir")
        os.mkdir(img_src + "_dir")
    if not os.path.exists(img_src + "_dir_src"):
        os.mkdir(img_src + "_dir_src")
    else:
        shutil.rmtree(img_src + "_dir_src")
        os.mkdir(img_src + "_dir_src")

    region_height = region.size[1]
    region_width = region.size[0]
    x = 0
    if is_get_main_region:
        cols = get_cols(region,step_col,w,mehtod_avg=True)
        #print(cols)
        if len(cols)>0:
            col_all_begin = cols[0]["x"]
            col_all_end = cols[len(cols)-1]["x"]
            if col_all_begin-10<0:
                col_all_begin=0
            else :
                col_all_begin = col_all_begin-10
            if col_all_end+13>region_width:
                col_all_end=region_width
            else :
                col_all_end= col_all_end+13
            box = (col_all_begin, 0, col_all_end, region_height)
            region = region.crop(box)
        #region_copy = region.copy()
        #region_copy = region_copy.resize((region_copy.size[0] * 2, region_copy.size[1] * 2), Image.ANTIALIAS)

    region.save(img_src)

    big_size = 2
    w = w * big_size
    h = h * big_size
    letter_pace = letter_pace * big_size
    row_space = row_space * big_size
    region_width = region.size[0]*big_size
    region_height = region.size[1] * big_size
    #new_width = to_width
    #new_height = region_height*to_width//region_width

    region = region.resize((region_width , region_height), Image.ANTIALIAS)


    """
    #斜度
    region.save(img_src)
    r_img = cv2.imread(img_src)
    r_img = rotate_about_center(r_img,1.1,dsize=(region_width,region_height))
    cv2.imwrite(img_src,r_img)
    region = Image.open(img_src)
    """

    cols = get_cols(region, step_col,w)

    #find_peaks(cols,9)
    #print("box_step,cols:", len(cols), cols)
    cols = find_valley(cols,letter_pace,big_size)




    #print("box_step,cols:",len(cols),cols)
    cv2_regin_img = np.array(region)
    #cols = get_cols(region, step_col)
    #print(co cols = get_cols(region,step_col)ls_gray_avg)
    #print(cols_gray_avg*1.2)
    cols2=[]
    col_index=0

    while col_index< len(cols)-1:
        col = cols[col_index]
        col_num = col["num"]
        col_x = col["x"]
        # print(col, cols_gray_avg)
        col2 = {}
        col2["begin"] = col_x
        col2["end"] = cols[col_index+1]["x"]
        space=col2["end"]-col2["begin"]
        #print(space)
        if space <w and col_index <len(cols)-2 and col_index>0:
            col_index_next=col_index+1
            col_next = cols[col_index_next]
            col_next_x = col_next["x"]
            col_next_next_x = cols[col_index_next+1]["x"]
            next_space=col_next_next_x-col_next_x
            col_index_pre = col_index - 1
            col_pre = cols[col_index_pre]
            col_pre_x = col_pre["x"]
            pre_space = col_x-col_pre_x
            if pre_space<next_space:
                cols2[len(cols2)-1]["end"]=col_next_x
                col2 = None
            else:
                col2["end"] = cols[col_index + 2]["x"]
                col_index += 1
        if space < w and col_index == 0 and len(cols)>2:
            col_index_next = col_index + 1
            col_next = cols[col_index_next]
            col_next_x = col_next["x"]
            col_next_next_x = cols[col_index_next + 1]["x"]
            next_space = col_next_next_x - col_next_x
            col2["end"] = cols[col_index + 2]["x"]
            col_index += 1
        if col2:
            cols2.append(col2)
        col_index+=1
    #print(cols2)

    """
    sum_width =0
    max_width =0
    for col2 in cols2:
        col_width = col2["end"]-col2["begin"]
        if col_width>max_width:
            max_width = col_width
        sum_width+=col_width
    sum_width -=max_width
    avg_width = sum_width//(len(cols2)-1)
    """
    if is_process_link:
        col_index=0
        cols3 = []
        for col2 in cols2:
            col_width = col2["end"] - col2["begin"]
            if col_width > w*2:
                if col_index==0:
                    col = {}
                    col["end"] = col2["end"]
                    col2["end"]-=int(w*1.2)
                    col["begin"] = col2["end"]
                    if col2["end"]-col2["begin"]>=w:
                        cols3.append(col2)
                    if col["end"]-col["begin"]>=w:
                        cols3.append(col)
                elif col_index == len(cols2)-1:
                    col = {}
                    col["end"] = col2["end"]
                    col2["end"] = col2["begin"]+int(w*1.2)
                    col["begin"] = col2["end"]
                    if col2["end"] - col2["begin"] >= w:
                        cols3.append(col2)
                    if col["end"] - col["begin"] >= w:
                        cols3.append(col)
                else:
                    col = {}
                    col["end"] = col2["end"]
                    col2["end"] = col2["begin"] + (col2["end"]-col2["begin"])//2
                    col["begin"] = col2["end"]
                    cols3.append(col2)
                    cols3.append(col)
            else:
                if col2["end"] - col2["begin"] >= w:
                    cols3.append(col2)
            col_index+=1
        cols2= cols3

    col2_index = 0
    col_width_sum = 0
    col_width_avg=0
    for col2 in cols2:
        col2_begin = col2["begin"]
        col2_end = col2["end"]
        box = (col2["begin"], 0, col2["end"], region_height)
        one_region = region.crop(box)
        one_region_width = one_region.size[0]
        one_region_height = one_region.size[1]
        img =None
        top=1
        bottom=1
        left=1
        right=1

        if(one_region_width>one_region_height) :
            border = (one_region_width-one_region_height)//2
            top=border+1
            bottom=one_region_width-one_region_height-top+2

        if (one_region_height > one_region_width):
            border = (one_region_height - one_region_width) // 2
            left = border+1
            right = (one_region_height - one_region_width)-left+2
        img = np.array(one_region)
        cv2.imwrite(img_src + "_dir_src/" + str(col2_index).zfill(3) + ".jpg", img)
        #dev = cv2.meanStdDev(img)
        #kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        #kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        #gray_avg = dev[1][0][0]
        #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 17, 3)
        #img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel2)
        #ret, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
        #img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT,value=(255,255,255))
        #img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_REPLICATE)
        #print(img[0][0][0],img[0][0][1],img[0][0][2])
        img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(int(img[0][0][0]),int(img[0][0][1]),int(img[0][0][2])))
        #img= ~img
        img = cv2.resize(img,(28,28),Image.ANTIALIAS)
        #img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 13, 0)

        #img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel1)
        #

        #ret, img = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
        #img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
        #cvMorphologyEx

        #ret, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)


        cv2.imwrite(img_src + "_dir/" + str(col2_index).zfill(3) + ".jpg",img)
        col2_index += 1
        cv2.rectangle(cv2_regin_img, (col2["begin"], 0), (col2["end"], region_height),(255, 0, 0))
    cv2.imwrite(img_src + "build.jpg", cv2_regin_img)
    pass

def inverse_color(image):
    height,width,size = image.shape
    img2 = image.copy()

    for i in range(height):
        for j in range(width):
            img2[i,j] = (255-image[i,j])
    return img2

def get_cols(row_region,step_col,w,mehtod_avg=False,method_peak=False):
    region_width = row_region.size[0]
    region_height = row_region.size[1]
    x = 0
    cols = []
    cols_gray_sum = 0.0
    while x + step_col < region_width:
        # print(cols)
        box = (x, 0, x + step_col, region_height)
        region_col = row_region.crop(box)
        region_col_dev = cv2.meanStdDev(np.array(region_col))
        region_col_gray_avg = region_col_dev[1][0][0]
        col_num = {}
        cols.append(col_num)
        col_num["num"] = region_col_gray_avg
        col_num["x"] = x
        cols_gray_sum += region_col_gray_avg
        x += step_col
    cols_gray_avg = cols_gray_sum / len(cols)
    cols3 = cols
    if mehtod_avg:
        cols3 = []
        for col in cols:
            col_num = col["num"]
            if col_num > cols_gray_avg:
                cols3.append(col)
    if method_peak:
        cols3 = find_peaks(cols,6)
    #print("cols3",cols3)
    cols4 = []
    col_index=0
    cols5 =[]
    while col_index < len(cols3)-1:
        col = cols3[col_index]
        col_x = col["x"]
        col4 = {}
        col4["begin"] = col_x
        space = cols3[col_index + 1]["x"] - col_x
        cols6=[]
        cols6.append(col)

        while space == step_col and col_index < len(cols3)-2:
            col4["end"] = cols3[col_index+1]["x"]
            col_index += 1
            col = cols3[col_index]
            col_x = col["x"]
            cols6.append(col)
            space = cols3[col_index + 1]["x"] - col_x
        if not col4.get("end") :
            col4["end"] = col_x
        #print("col4", col4)
        cols4.append(col4)
        space = col4["end"]-col4["begin"]
        if space > w//4:
            for col in cols6:
                cols5.append(col)
        col_index += 1
    #print("cols4",cols4)
    #print("cols5",cols5)
    return cols5

def find_peaks(data,step,bigsize=1):
    #print(data)
    data_size = len(data)
    result=[]
    for i in range(0,data_size):
        d = data[i]
        peak=True
        d_step = (step - 1) * 2
        ltnum = d_step
        for s in range(1,step):
            left =0
            if i-s>0:
                left = i-s
            right=data_size-1
            if i+s<data_size-1:
                right = i+s
            l_data = data[left]
            r_data = data[right]
            if l_data["num"]> d["num"]:
                ltnum -= 1
            if r_data["num"]> d["num"]:
                ltnum -= 1
        if ltnum/d_step<0.9:
            peak=False
            #print(d,l_data,r_data)
        if peak :
            if len(result)>0:
                last = result[len(result) - 1]
                if d.get("x"):
                    if d["x"] - last["x"] <bigsize*4:
                        result[len(result) - 1]=d
                    else:
                        result.append(d)
                elif d.get("y"):
                    if d["y"] - last["y"] < bigsize * 4:
                        result[len(result) - 1] = d
                    else:
                        result.append(d)
            else:
                result.append(d)
    #print("peak:",result)
    #print("peak len:",len(result))
    return  result
def find_valley(data,step,bigsize=1):
    #print(data)
    data_size = len(data)
    result=[]
    for i in range(0,data_size):
        d = data[i]
        valley=True
        d_step = (step - 1) * 2
        #if i<step:
        #    d_step = (step - 1) * 2-(step-i)
        ltnum = d_step
        for s in range(1,step):
            left =0
            if i-s>0:
                left = i-s
            right=data_size-1
            if i+s<data_size-1:
                right = i+s
            l_data = data[left]
            r_data = data[right]
            if l_data["num"]< d["num"]:
                ltnum -=1
            if r_data["num"]< d["num"]:
                ltnum -= 1

        if ltnum/d_step<0.9:
            valley=False
            #print(d,l_data,r_data)


        if valley:
            if len(result)>0:
                last = result[len(result) - 1]
                if d.get("x"):
                    if d["x"] - last["x"] <bigsize*4:
                        result[len(result) - 1]=d
                    else:
                        result.append(d)
                elif d.get("y"):
                    if d["y"] - last["y"] < bigsize * 4:
                        result[len(result) - 1] = d
                    else:
                        result.append(d)
            else:
                result.append(d)

    #print("valley:",result)
    #print("valley len:",len(result))
    return  result

#img_path = project_dir + "/data/invoice/test/cardno.jpg"
#img =cv2.imread(img_path,0)
#img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,3)
#kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
#img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
#new_img = Image.fromarray(img)
#new_img.show()
#img = Image.open(img_path)
#box_step(project_dir + "/data/invoice/test/cardno.jpg", 18, 20,letter_pace=10)
#box_step(project_dir + "/data/invoice/test/vinno.jpg", 6, 20,3,1)
#box_step(project_dir + "/data/invoice/test/vinno.jpg", 6, 20,)
#get_region_row(img,20).show()




def rotate_about_center(src, angle, scale=1.,dsize=None):
    w = src.shape[1]
    h = src.shape[0]
    rangle = np.deg2rad(angle)  # angle in radians
    # now calculate new image width and height
    nw = (abs(np.sin(rangle)*h) + abs(np.cos(rangle)*w))*scale
    nh = (abs(np.cos(rangle)*h) + abs(np.sin(rangle)*w))*scale
    # ask OpenCV for the rotation matrix
    rot_mat = cv2.getRotationMatrix2D((nw*0.5, nh*0.5), angle, scale)
    # calculate the move from the old center to the new center combined
    # with the rotation
    rot_move = np.dot(rot_mat, np.array([(nw-w)*0.5, (nh-h)*0.5,0]))
    # the move only affects the translation, so update the translation
    # part of the transform
    rot_mat[0,2] += rot_move[0]
    rot_mat[1,2] += rot_move[1]
    if not dsize:
        dsize = (int(math.ceil(nw)), int(math.ceil(nh)))
    return cv2.warpAffine(src, rot_mat, dsize, flags=cv2.INTER_LANCZOS4,borderMode=cv2.BORDER_REPLICATE)




def isCrust(pix):
    return sum(pix) < 25


def hCheck(img, y):
    count = 0
    width = img.size[0]
    for x in range(0, width):
        if isCrust(img.getpixel((x, y))):
            count += 1
        if count > width//2:
            return True
    return False

def vCheck(img, x, ):
    count = 0
    height = img.size[1]
    for y in range(0, height):
        if isCrust(img.getpixel((x, y))):
            count += 1
        if count > height//2:
            return True
    return False

def boundaryFinder(img,crust_side,core_side,checker):
    if not checker(img,crust_side):
        return crust_side
    if checker(img,core_side):
        return core_side
    mid = (crust_side + core_side) / 2
    while  mid != core_side and mid != crust_side:
        if checker(img,mid):
            crust_side = mid
        else:
            core_side = mid
        mid = (crust_side + core_side) / 2
    return core_side
    pass


def handleBorderImage(filename):
    img = Image.open(os.path.join(filename))
    if img.mode != "RGB":
        img = img.convert("RGB")
    width, height = img.size
    left = boundaryFinder(img, 0, width/2, vCheck)
    right = boundaryFinder(img, width-1, width/2, vCheck)
    top = boundaryFinder(img, 0, height/2, hCheck)
    bottom = boundaryFinder(img, height-1, width/2, hCheck)

    rect = (left,top,right,bottom)
    region = img.crop(rect)
    region.save(filename)
    pass