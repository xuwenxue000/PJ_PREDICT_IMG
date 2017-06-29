#!/usr/bin/python
#-*- encoding:utf-8 -*-

import numpy as np
import cv2
import os
import PIL.Image as Image

# 只复制原图
def img_copy(sourcepath,targetpath):
    for filename in os.listdir(sourcepath):
        name = filename.split('.', 1)[0]
        suffix = filename.split('.',1)[1]
        img = cv2.imread(sourcepath+filename,0)
        if (img is None):
            print(filename)
        # 复制原图
        cv2.imwrite(targetpath + filename, img)

# 几何变换：平移
def img_move(sourcepath, targetpath,numpixs,directionnumber=8):

    for filename in os.listdir(sourcepath):
        if '_move_' not in filename:
            name = filename.split('.', 1)[0]
            suffix = filename.split('.', 1)[1]
            img = cv2.imread(sourcepath + filename)
            #print(img.shape)

            directions = 0
            numpixs = numpixs;

            dst = img_movepix(img,numpixs,0)
            cv2.imwrite(targetpath + name + '_move_x_'+str(numpixs)+'.' + suffix, dst)
            directions = directions + 1
            if directions >= directionnumber:
                continue

            dst = img_movepix(img,0,numpixs)
            cv2.imwrite(targetpath + name + '_move_y_' + str(numpixs) + '.' + suffix, dst)
            directions = directions + 1
            if directions >= directionnumber:
                continue

            dst = img_movepix(img,-numpixs,0)
            cv2.imwrite(targetpath + name + '_move_-x_' + str(numpixs) + '.' + suffix, dst)
            directions = directions + 1
            if directions >= directionnumber:
                continue

            dst = img_movepix(img,0,-numpixs)
            cv2.imwrite(targetpath + name + '_move_-y_' + str(numpixs) + '.' + suffix, dst)
            directions = directions + 1
            if directions >= directionnumber:
                continue

            dst = img_movepix(img,numpixs,numpixs)
            cv2.imwrite(targetpath + name + '_move_1_' + str(numpixs) + '.' + suffix, dst)
            directions = directions + 1
            if directions >= directionnumber:
                continue

            dst = img_movepix(img, -numpixs, numpixs)
            cv2.imwrite(targetpath + name + '_move_2_' + str(numpixs) + '.' + suffix, dst)
            directions = directions + 1
            if directions >= directionnumber:
                continue

            dst = img_movepix(img, numpixs, -numpixs)
            cv2.imwrite(targetpath + name + '_move_3_' + str(numpixs) + '.' + suffix, dst)
            directions = directions + 1
            if directions >= directionnumber:
                continue

            dst = img_movepix(img, -numpixs, -numpixs)
            cv2.imwrite(targetpath + name + '_move_4_' + str(numpixs) + '.' + suffix, dst)


# 对图片移动,x轴x_pix个像素，y轴y_pix个像素
def img_movepix(img,x_pix,y_pix):
    rows, cols,type = img.shape
    M = np.float32([[1, 0, x_pix], [0, 1, y_pix]])  # move a pix
    dst = cv2.warpAffine(img, M, (cols, rows),borderMode=cv2.BORDER_CONSTANT, borderValue=(int(img[0][0][0]),int(img[0][0][1]),int(img[0][0][2])))
    return dst

# 几何变换：按指定direction方向按指定step步长平移numpixs个像素
def img_move(sourcepath,targetpath,numpixs=1,direction=(1,0)):
    for filename in os.listdir(sourcepath):
        if '_move_' not in filename:
            name = filename.split('.', 1)[0]
            suffix = filename.split('.', 1)[1]
            img = cv2.imread(sourcepath + filename)
            dst = img_movepix(img, direction[0] * numpixs, direction[1] * numpixs)
            cv2.imwrite(targetpath + name + '_move_' + str(direction[0])+str(direction[1])+str(numpixs) + '.' + suffix, dst)

# 几何变换：倾斜
def img_turn(sourcepath,targetpath):
    for filename in os.listdir(sourcepath):
        name = filename.split('.', 1)[0]
        suffix = filename.split('.',1)[1]
        img = cv2.imread(sourcepath+filename,0)
        if (img is None):
            print(filename)
        # 复制原图
        #cv2.imwrite(targetpath + filename, img)

        # 按角度倾斜,
        rows, cols = img.shape
        for v in (1,2,3,-1,-2,-3):
            M = cv2.getRotationMatrix2D((cols / 2, rows / 2), v*2,1)
            #dst = cv2.warpAffine(img, M, (cols, rows),borderValue=255)
            dst = cv2.warpAffine(img, M, (cols, rows))
            cv2.imwrite(targetpath +name +'_turn_'+str(v*5)+'.'+suffix, dst)

        # 垂直翻转
        #flipped = cv2.flip(img, 1)
        #cv2.imwrite(targetpath +name + '_turn_flip1.'+suffix, flipped)

        #水平翻转
        #flipped = cv2.flip(img, 0)
        #cv2.imwrite(targetpath +name + '_turn_flip0.'+suffix, flipped)

        # 图像水平垂直翻转
        #flipped = cv2.flip(img, -1)
        #cv2.imwrite(targetpath +name + '_turn_flip2.'+suffix, flipped)

# 仿射变换
def img_affineTransform(sourcepath,targetpath):
    for filename in os.listdir(sourcepath):
        if '_' not in filename:
            name = filename.split('.', 1)[0]
            suffix = filename.split('.', 1)[1]
            img = cv2.imread(sourcepath+filename,0)
            for i in range(1,4):
                (newimg1,newimg2) = imgnew_affineTransform(img, i)
                cv2.imwrite(targetpath + name + '_transform_' + str(i) + '1.'+suffix, newimg1)
                #cv2.imwrite(targetpath + name + '_transform_' + str(i) + '2.'+suffix, newimg2)




# 为每张图放射变换
def imgnew_affineTransform(img,rand):
    """
    #cv2.imshow(img)
    rows, cols, ch = img.shape
    dst = np.zeros((rows*2,cols*2), np.uint8)
    #pts1 = np.float32([[rand*0.03, rand*0.03], [cols-1, 0], [0, rows-1]])
    #pts2 = np.float32([[cols, rows*0.3], [cols*0.85, rows*0.25], [cols*0.15, rows*0.7]])
    pts1 = np.float32([[0, 0], [cols - 14, 0], [0, rows - 1]])
    pts2 = np.float32([[1, 14], [cols*0.9 , 14], [cols*0.1, rows * 0.95]])    
    pts1 = np.float32([[rand, rand], [28, 2], [2, 28]])
    pts2 = np.float32([[2, 28], [28, 1], [28, 28]])
    
    M = cv2.getAffineTransform(pts1, pts2)
    dst = cv2.warpAffine(img,M, (cols, rows))
    """

    rows, cols = img.shape
    rate = 0.2+rand*0.15   # 原：rand*0.25
    pts1 = np.float32([[0,0], [cols-1,0], [0,rows-1], [cols-1,rows-1]])
    #pts2 = np.float32([[cols*0.05,rows*0.33], [cols*0.9,rows*0.25], [cols*0.2,rows*0.7], [cols*0.8,rows*0.9]])
    pts2 = np.float32([[0,0], [cols-1,0], [1, rows-1], [cols * rate, rows]])
    PerspectiveMatrix = cv2.getPerspectiveTransform(pts1, pts2)
    dst1 = cv2.warpPerspective(img, PerspectiveMatrix, (cols, rows))

    pts2 = np.float32([[0, 0], [cols - 1, 0], [1, rows - 1], [cols, rows*rate]])
    PerspectiveMatrix = cv2.getPerspectiveTransform(pts1, pts2)
    dst2 = cv2.warpPerspective(img, PerspectiveMatrix, (cols, rows))



    """
    rows, cols, ch = img.shape
    pts1 = np.float32([[rand, rand], [28, 2], [2, 28]])
    pts2 = np.float32([[10, 100], [200, 50], [100, 200]])
    M = cv2.getAffineTransform(pts1, pts2)
    dst = cv2.warpAffine(img, M, (cols, rows))
    """
    return dst1,dst2


# 为每张图放射变换
def imgnew_affineTransform_copy(img, rand):
    """
    #cv2.imshow(img)
    rows, cols, ch = img.shape
    dst = np.zeros((rows*2,cols*2), np.uint8)
    #pts1 = np.float32([[rand*0.03, rand*0.03], [cols-1, 0], [0, rows-1]])
    #pts2 = np.float32([[cols, rows*0.3], [cols*0.85, rows*0.25], [cols*0.15, rows*0.7]])
    pts1 = np.float32([[0, 0], [cols - 14, 0], [0, rows - 1]])
    pts2 = np.float32([[1, 14], [cols*0.9 , 14], [cols*0.1, rows * 0.95]])    
    pts1 = np.float32([[rand, rand], [28, 2], [2, 28]])
    pts2 = np.float32([[2, 28], [28, 1], [28, 28]])

    M = cv2.getAffineTransform(pts1, pts2)
    dst = cv2.warpAffine(img,M, (cols, rows))
    """

    rows, cols = img.shape
    rate = rand*0.25
    pts1 = np.float32([[0, 0], [cols - 1, 0], [0, rows - 1], [cols - 1, rows - 1]])
    pts2 = np.float32([[0, 0], [cols - 1, 0], [1, rows - 1], [cols * rate, rows]])
    PerspectiveMatrix = cv2.getPerspectiveTransform(pts1, pts2)
    dst1 = cv2.warpPerspective(img, PerspectiveMatrix, (cols, rows))

    pts2 = np.float32([[0, 0], [cols - 1, 0], [1, rows - 1], [cols, rows * rate]])
    PerspectiveMatrix = cv2.getPerspectiveTransform(pts1, pts2)
    dst2 = cv2.warpPerspective(img, PerspectiveMatrix, (cols, rows))

    """
    rows, cols, ch = img.shape
    pts1 = np.float32([[rand, rand], [28, 2], [2, 28]])
    pts2 = np.float32([[10, 100], [200, 50], [100, 200]])
    M = cv2.getAffineTransform(pts1, pts2)
    dst = cv2.warpAffine(img, M, (cols, rows))
    """
    return dst1, dst2

# 几何变换+放射变换
def turnAndTransform_file(targetpath):
    for filename in os.listdir(targetpath):
        if '_turn_' in filename and ('_transform_' not in filename) and ('noise_' not in filename):
            name = filename.split('.', 1)[0]
            suffix = filename.split('.', 1)[1]
            img = cv2.imread(targetpath + filename,0)
            for i in range(1,4):

                (newimg1, newimg2) = imgnew_affineTransform(img, i)
                cv2.imwrite(targetpath + name + '_transform_' + str(i) + '1.'+suffix, newimg1)
                cv2.imwrite(targetpath + name + '_transform_' + str(i) + '2.'+suffix, newimg2)

# 画干扰线
def img_line(sourcepath, targetpath):
    for filename in os.listdir(sourcepath):
        if '_line' not in filename:
            name = filename.split('.', 1)[0]
            suffix = filename.split('.', 1)[1]
            img = cv2.imread(sourcepath + filename, 0)
            if (img is None):
                print(filename)
                continue
            img1 = cv2.line(img, (0, 0), (28, 28), (0, 0, 0), thickness=1)
            cv2.imwrite(targetpath + name + '_line1.' + suffix, img1)
            img = cv2.imread(sourcepath + filename, 0)
            img2 = cv2.line(img, (0, 28), (28, 0), (0, 0, 0), thickness=1)
            cv2.imwrite(targetpath + name + '_line2.' + suffix, img2)
            img3 = cv2.line(img1, (0, 28), (28, 0), (0, 0, 0), thickness=1)
            cv2.imwrite(targetpath + name + '_line3.' + suffix, img3)
            # cv2.imwrite(targetpath + name + '_transform_' + str(i) + '2.'+suffix, newimg2)

# 高斯加噪
def addGussiaNoise(targetpath):
    for filename in os.listdir(targetpath):
        if 'noise_' not in filename:
            name = filename.split('.', 1)[0]
            suffix = filename.split('.', 1)[1]
            img = cv2.imread(targetpath + filename,0)
            if (img is None):
                print(img)
                continue

            # 如果是灰度图
            if img.ndim == 2:
                #img[j, i] = 255
                for i in range(1, 4):
                    param = 5 * i
                    # 灰阶范围
                    grayscale = 256
                    w = img.shape[1]
                    h = img.shape[0]
                    newimg = np.zeros((h, w), np.uint8)

                    for x in range(0, h):
                        for y in range(0, w, 2):
                            r1 = np.random.random_sample()
                            r2 = np.random.random_sample()
                            z1 = param * np.cos(2 * np.pi * r2) * np.sqrt((-2) * np.log(r1))
                            z2 = param * np.sin(2 * np.pi * r2) * np.sqrt((-2) * np.log(r1))

                            fxy = int(img[x, y] + z1)
                            fxy1 = int(img[x, y + 1] + z2)
                            # f(x,y)
                            if fxy < 0:
                                fxy_val = 0
                            elif fxy > grayscale - 1:
                                fxy_val = grayscale - 1
                            else:
                                fxy_val = fxy
                            # f(x,y+1)
                            if fxy1 < 0:
                                fxy1_val = 0
                            elif fxy1 > grayscale - 1:
                                fxy1_val = grayscale - 1
                            else:
                                fxy1_val = fxy1
                            newimg[x, y] = fxy_val
                            newimg[x, y + 1] = fxy1_val
                            cv2.imwrite(targetpath + name + '_gussianoise_' + str(param) + '.' + suffix, newimg)
            # 如果是RBG图片
            elif img.ndim == 3:
                for i in range(1, 4):
                    param = 5 * i
                    w = img.shape[1]
                    h = img.shape[0]
                    p = img.shape[2]
                    newimg = img
                    for x in range(0, h):
                        for y in range(0, w, 2):
                            r1 = np.random.random_sample()
                            r2 = np.random.random_sample()
                            z1 = param * np.cos(2 * np.pi * r2) * np.sqrt((-2) * np.log(r1))
                            #z2 = param * np.sin(2 * np.pi * r2) * np.sqrt((-2) * np.log(r1))

                            newimg[x, y, 0] = 255
                            newimg[x, y, 1] = 255
                            newimg[x, y, 2] = 255
                            cv2.imwrite(targetpath + name + '_gussianoise_' + str(param) + '.'+suffix, newimg)

# 椒盐加噪
def addSaltNoise(targetpath):
    for filename in os.listdir(targetpath):
        if 'noise_' not in filename:
            name = filename.split('.', 1)[0]
            suffix = filename.split('.', 1)[1]
            img = cv2.imread(targetpath + filename)
            if (img is None):
                print(img)
                continue
            # coutn = 10000
            for number in range(1, 3):
                coutn = 8 * number
                # 循环添加n个椒盐
                for k in range(coutn):
                    # 随机选择椒盐的坐标
                    i = int(np.random.random() * img.shape[1])
                    j = int(np.random.random() * img.shape[0])
                    # 如果是灰度图
                    if img.ndim == 2:
                        img[j, i] = 255
                    # 如果是RBG图片
                    elif img.ndim == 3:
                        img[j, i, 0] = 200
                        img[j, i, 1] = 200
                        img[j, i, 2] = 200
                cv2.imwrite(targetpath + name + '_saltnoise_' + str(coutn) + '.'+suffix, img)

# 切割完的原图  - 多种昂方式生成 样本库
def image_adjust(targetpath):
    col2_index = 0
    targetpath_1 = targetpath[:len(targetpath)-1]+'_1/'
    for filename in os.listdir(targetpath):
        img = cv2.imread(targetpath + filename)
        if img is None:
            print('img is None',filename)
        one_region_width = img.shape[1]
        one_region_height = img.shape[0]

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

        print(top,bottom,left,right)
        img = np.array(img)

        img1 = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(int(img[0][0][0]),int(img[0][0][1]),int(img[0][0][2])))
        print(img1.shape)
        #cv2.imwrite(targetpath + 'bj_img1' + str(col2_index).zfill(2) + ".jpg", img1)
        tmpimg = cv2.resize(img1, (28, 28), Image.ANTIALIAS)
        cv2.imwrite(targetpath_1 + filename+'img1' + str(col2_index).zfill(2) + ".jpg", tmpimg)

        img2 = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT,
                                 value=(int(img[one_region_height-1][0][0]), int(img[one_region_height-1][0][1]), int(img[one_region_height-1][0][2])))
        #cv2.imwrite(targetpath + 'bj_img2' + str(col2_index).zfill(2) + ".jpg", img2)
        tmpimg = cv2.resize(img2, (28, 28), Image.ANTIALIAS)
        cv2.imwrite(targetpath_1 +filename+ 'img2' + str(col2_index).zfill(2) + ".jpg", tmpimg)

        img3 = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT,
                                 value=(int(img[0][one_region_width-1][0]), int(img[0][one_region_width-1][1]), int(img[0][one_region_width-1][2])))
        tmpimg = cv2.resize(img3, (28, 28), Image.ANTIALIAS)
        cv2.imwrite(targetpath_1 + filename + 'img3' + str(col2_index).zfill(2) + ".jpg", tmpimg)

        img4 = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT,
                                 value=(int(img[one_region_height-1][one_region_width-1][0]), int(img[one_region_height-1][one_region_width-1][1]), int(img[one_region_height-1][one_region_width-1][2])))
        tmpimg = cv2.resize(img4, (28, 28), Image.ANTIALIAS)
        cv2.imwrite(targetpath_1 + filename + 'img4' + str(col2_index).zfill(2) + ".jpg", tmpimg)

        #cv2.imwrite(targetpath+filename + str(col2_index).zfill(3) + ".jpg", img)
        #for i in range(1,5):
            #name = 'img'+str(i)
            #print(name)
            #print((img+i).shape)
            #cv2.imwrite(targetpath +'bj_' +str(i) + str(col2_index).zfill(2) + ".jpg", img+i)
            #tmpimg = cv2.resize(img+i,(28,28),Image.ANTIALIAS)
            #cv2.imwrite(targetpath + str(i)+str(col2_index).zfill(2) + ".jpg", tmpimg)
        col2_index += 1