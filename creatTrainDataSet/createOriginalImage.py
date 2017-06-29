#!/usr/bin/python
#-*- encoding:utf-8 -*-

import numpy as np
import cv2
import os
from matplotlib import pyplot as plt
#import freetype
from PIL import Image, ImageDraw, ImageFont

# public define
py_dir = os.path.dirname(os.path.realpath(__file__))
project_dir = os.path.dirname(py_dir)
img_dir = project_dir+'/files/'
img_dir ='/Volumes/Transcend/ijob/original/'

numbers = ['0','1','2','3','4','5','6','7','8','9']
letters_up = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
letters_low =['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

"""
letters_up = ['A']
letters_low =['身','份']
number = ['0','1','2','3','4','5','6','7','8','9']
"""
# create numbers Image
def createNumberImg(targetpath):
    #targetpath = img_dir + '/number/'
    if os.path.isdir(targetpath):
        pass
    else:
        os.mkdir(targetpath)

    for x in numbers:
        img = np.zeros((28, 28), np.uint8)
        font = cv2.FONT_ITALIC
        img = cv2.putText(img, x, (2, 24), font, 1, (255, 255, 255), 2)
        cv2.imwrite(targetpath + x + '.jpg', img)
        #img = cv2.imread(targetpath + x + '.png', 0)
        # img= cv2.resize(img, (28,28), interpolation=cv2.INTER_CUBIC)
        #cv2.imwrite(targetpath + x + '.png', img)

    '''
    for y in numbers:
        img = np.full((28, 28), 255, np.uint8)
        font = cv2.FONT_ITALIC
        img = cv2.putText(img, y, (2, 24), font, 1, (0, 0, 0), 2)
        cv2.imwrite(targetpath + y + '.jpg', img)
    '''

# create upperLetter Image
def createUpperLetterImg(targetpath):
    #targetpath = img_dir + '/upper/'

    if os.path.isdir(targetpath):
        pass
    else:
        os.mkdir(targetpath)

    for x in letters_up:
        img = np.zeros((28, 28), np.uint8)
        font = cv2.FONT_ITALIC
        img = cv2.putText(img, x, (2, 24), font, 1, (255, 255, 255), 2)
        cv2.imwrite(targetpath + x + '.jpg', img)
        #img = cv2.imread(targetpath + x + '.png', 0)
        # img= cv2.resize(img, (28,28), interpolation=cv2.INTER_CUBIC)
        #cv2.imwrite(targetpath + x + '.png', img)
    '''
    for x in letters_up:
        img = np.full((28, 28), 255, np.uint8)
        font = cv2.FONT_ITALIC
        img = cv2.putText(img, x, (2, 24), font, 1, (0, 0, 0), 2)
        cv2.imwrite(targetpath + x + '.jpg', img)
    '''

# create lowerLetter Image
def createLowerLetterImg(targetpath):
    #targetpath = img_dir + '/lower_2/'

    if os.path.isdir(targetpath):  #目录不存在创建
        pass
    else:
        os.mkdir(targetpath)

    for x in letters_low:
        img = np.zeros((28, 28), np.uint8)
        font = cv2.FONT_ITALIC
        img = cv2.putText(img, x, (2,20),font,0.78, (255, 255, 255),2)
        cv2.imwrite(targetpath + x + '.jpg', img)
        #img = cv2.imread(targetpath + x + '.png', 1)
        # img= cv2.resize(img, (28,28), interpolation=cv2.INTER_CUBIC)
        #cv2.imwrite(targetpath + x + '.png', img)
    '''
    for x in letters_low:
        img = np.full((28, 28), 255, np.uint8)
        font = cv2.FONT_ITALIC
        img = cv2.putText(img, x, (2,20),font,0.78, (0, 0, 0),2)
        cv2.imwrite(targetpath + x + '.jpg', img)
    '''
# create Chinese Image
def createChineseImg():

    """
    font = ImageFont.truetype('simsun.ttc', 24)
    im = Image.open(sourcepath + letter+'.png')
    draw = ImageDraw.Draw(im)
    text = unicode('你好', 'utf-8')
    draw.text((20, 20), text, font=font, fill=(0, 0, 0, 0))
    im.save(targetpath + letter + '.png')
    """

