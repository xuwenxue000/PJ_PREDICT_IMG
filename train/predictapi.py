#!/usr/bin/python
#-*- encoding:utf-8 -*-

from __future__ import print_function
from keras.models import  model_from_json

import tensorflow as tf
from keras import backend as K
from keras.backend.tensorflow_backend import set_session
config = tf.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.3
set_session(tf.Session(config=config))

import os,cv2,sys

import numpy as np
py_dir = os.path.dirname(os.path.realpath(__file__))
project_dir = os.path.dirname(py_dir)
sys.path.append(project_dir)
import matplotlib.pyplot as plt
import train.dataload as data
#port api_common.utils.log as logger

# model 类型
"""
数字识别网络：modelArgs = ['number_architecture.json','number_weights.h5']
大写字母识别网络：modelArgs = ['upper_architecture.json','upper_weights.h5']
小写字母识别网络：modelArgs = ['lower_architecture.json','lower_weights.h5']
所有字母表识别网络：modelArgs = ['alphabet_architecture.json','alphabet_weights.h5']
数字+字母表识别网络：modelArgs = ['numandalphabet_architecture.json','numandalphabet_weights.h5']
"""
# input image dimensions
img_rows, img_cols = 28, 28
py_dir = os.path.dirname(os.path.realpath(__file__))
global modules
modules={}
#加载模型结构和参数
def modelLoad(modelArgs):
    key = modelArgs[0]+modelArgs[1]
    model = modules.get(key);
    if not model:
        model = model_from_json(open(modelArgs[0]).read())
        model.load_weights(modelArgs[1])
        modules[key]=model
    return model

# 识别单个图片
def checkSingelImage(imgpath,model):
    x = data.load_img_data(imgpath)
    if K.image_data_format() == 'channels_first':
        x = x.reshape(x.shape[0], 1, img_rows, img_cols)
    else:
        x = x.reshape(x.shape[0], img_rows, img_cols, 1)
    x = x.astype('float32')
    x /= 255
    #print('x shape:', x.shape)

    # 预测图片
    predicted_classes = model.predict_classes(x)
    print("predicted_classes ： "+str(predicted_classes))
    plt.figure()
    plt.subplot(3, 3, 1)
    plt.imshow(x[0].reshape(28, 28), cmap='gray', interpolation='none')
    plt.title("Predicted {}".format(predicted_classes[0]))
    plt.show()

# 字母识别单个图片
def lower_checkSingelImage(imgpath, model):
    x = data.load_img_data(imgpath)
    if K.image_data_format() == 'channels_first':
        x = x.reshape(x.shape[0], 1, img_rows, img_cols)
    else:
        x = x.reshape(x.shape[0], img_rows, img_cols, 1)
    x = x.astype('float32')
    x /= 255
    # print('x shape:', x.shape)

    # 预测图片
    predicted_classes = model.predict_classes(x)
    print("predicted_classes ： " + str(predicted_classes))
    plt.figure()
    plt.subplot(3, 3, 1)
    plt.imshow(x[0].reshape(28, 28), cmap='gray', interpolation='none')
    plt.title("Predicted {}".format(chr(predicted_classes[0]+97)))
    plt.show()

# 识别目录下的图片
def lower_checkImages(imgdir, model):
    path = imgdir
    X = data.load_X_data(path)
    if K.image_data_format() == 'channels_first':
        X = X.reshape(X.shape[0], 1, img_rows, img_cols)
    else:
        X = X.reshape(X.shape[0], img_rows, img_cols, 1)

    X = X.astype('float32')
    X /= 255
    # 开始预测
    predicted_classes = model.predict_classes(X)
    print(predicted_classes)

    # 图像展示出来9张看看
    plt.figure()
    for i, correct in enumerate(predicted_classes[:9]):
        print("i=" + str(i) + " correct=" + str(correct))
        plt.subplot(3, 3, i + 1)
        plt.imshow(X[i].reshape(28, 28), cmap='gray', interpolation='none')
        plt.title("Predicted {}".format(chr(predicted_classes[i]+97)))
    plt.show()

# 识别目录下的图片
def upper_checkImages(imgdir, model):
    path = imgdir
    X = data.load_X_data(path)
    if K.image_data_format() == 'channels_first':
        X = X.reshape(X.shape[0], 1, img_rows, img_cols)
    else:
        X = X.reshape(X.shape[0], img_rows, img_cols, 1)

    X = X.astype('float32')
    X /= 255
    # 开始预测
    predicted_classes = model.predict_classes(X)
    print(predicted_classes)

    # 图像展示出来9张看看
    plt.figure()
    for i, correct in enumerate(predicted_classes[:9]):
        print("i=" + str(i) + " correct=" + str(correct))
        plt.subplot(3, 3, i + 1)
        plt.imshow(X[i].reshape(28, 28), cmap='gray', interpolation='none')
        plt.title("Predicted {}".format(chr(predicted_classes[i]+65)))
    plt.show()

# 字母识别单个图片
def upper_checkSingelImage(imgpath, model):
    x = data.load_img_data(imgpath)
    if K.image_data_format() == 'channels_first':
        x = x.reshape(x.shape[0], 1, img_rows, img_cols)
    else:
        x = x.reshape(x.shape[0], img_rows, img_cols, 1)
    x = x.astype('float32')
    x /= 255
    # print('x shape:', x.shape)

    # 预测图片
    predicted_classes = model.predict_classes(x)
    print("predicted_classes ： " + str(predicted_classes))
    plt.figure()
    plt.subplot(3, 3, 1)
    plt.imshow(x[0].reshape(28, 28), cmap='gray', interpolation='none')
    plt.title("Predicted {}".format(chr(predicted_classes[0]+65)))
    plt.show()

dict_numbers_and_letters={'0':'0','1':'1','2':'2','3':'3','4':'4','5':'5','6':'6','7':'7','8':'8','9':'9'
    ,'10':'A','11':'B','12':'C','13':'D','14':'E','15':'F','16':'G','17':'H','18':'I','19':'J','20':'K','21':'L','22':'M'
    ,'23':'N','24':'O','25':'P','26':'Q','27':'R','28':'S','29':'T','30':'U','31':'V','32':'W','33':'X','34':'Y','35':'Z'
    ,'36':'a','37':'b','38':'c','39':'d','40':'e','41':'f','42':'g','43':'h','44':'i','45':'j','46':'k','47':'l','48':'m'
    ,'49':'n','50':'o','51':'p','52':'q','53':'r','54':'s','55':'t','56':'u','57':'v','58':'w','59':'x','60':'y','61':'z'}
dict_numbers_and_X={'0':'0','1':'1','2':'2','3':'3','4':'4','5':'5','6':'6','7':'7','8':'8','9':'9','10':'X'}

# predict whit type
# 0:number 1:number and upper 2:number and upper and lower 3:number and upperX
def checkImages(imgdir, model,type,isresulttxt=False):
    result = []
    result_class = []
    predictedX=None
    if os.path.isfile(imgdir):
        predictedX = data.load_img_data(imgdir)
    elif os.path.isdir(imgdir):
        if len(os.listdir(imgdir)) > 0:
            predictedX,filenames = data.load_X_data(imgdir)
    else:
        print ("{imgdir is not a file or dir,return}")

    if predictedX is None:
        return result,result_class
    if K.image_data_format() == 'channels_first':
        predictedX = predictedX.reshape(predictedX.shape[0], 1, img_rows, img_cols)
    else:
        predictedX = predictedX.reshape(predictedX.shape[0], img_rows, img_cols, 1)
    if predictedX is None:
        return result,result_class
    predictedX = predictedX.astype('float32')
    predictedX /= 255

    # 开始预测
    predict_proba = model.predict_proba(predictedX)

    # 返回类别
    result_class = []
    if predict_proba.shape[-1] > 1:
        predicted_classes = predict_proba.argmax(axis=-1)
        for i in range(0, len(predicted_classes)):
            if type ==3:
                result_class.append(dict_numbers_and_X[str(predicted_classes[i])])
            else:
                result_class.append(dict_numbers_and_letters[str(predicted_classes[i])])
    else:
        result_class = (predict_proba > 0.5).astype('int32')

    # 返回概率
    result = []
    if predict_proba.shape[-1] > 1:
        proba = predict_proba.astype('float16')
        num = len(proba)
        result = []
        for i in range(0, num):
            m = np.argsort(-proba[i], axis=0)  # 降序排
            Yclass = []
            for j in range(0,3):
                resultclass = m[j]
                if (proba[i][resultclass]>0.0):
                    if type == 3:
                        dict = {"value": dict_numbers_and_X[str(resultclass)],
                                "probability": proba[i][resultclass]}
                        Yclass.append(dict)
                    else:
                        dict = {"value":dict_numbers_and_letters[str(resultclass)],"probability":proba[i][resultclass]}
                        Yclass.append(dict)
            result.append(Yclass)
    else:
        #print (predict_proba > 0.5).astype('int32')
        result.append(predict_proba > 0.5).astype('int32')


    # 图像展示出来9张看看
    '''
    plt.figure()
    for i, correct in enumerate(predicted_classes[:9]):
        print("i=" + str(i) + " correct=" + str(correct))
        plt.subplot(3, 3, i + 1)
        plt.imshow(predictedX[i].reshape(28, 28), cmap='gray', interpolation='none')
        plt.title("Predicted {}".format(dict_numbers_and_letters[str(predicted_classes[i])]))
    plt.show()
    '''

    if isresulttxt == True:
        # 将结果保存在predict_result.txt中
        result_file = project_dir + "/tmp_predict/result.txt"
        if os.path.exists(result_file):
            os.remove(result_file)
        if os.path.isdir(imgdir):
            num = len(os.listdir(imgdir))
            successnum =0
            with open(result_file, 'a') as f:
                f.write(str('{"path":"'+imgdir+'"}') + '\n')
            for i in range(num):
                out_result = ''
                out_result=out_result+'"file_name":"'+filenames[i]+'","predict_result":"'+result_class[i]+'"'

                if filenames[i][0]==result_class[i]:
                    out_result=out_result+',"success":"1"'
                    successnum = successnum+1
                else:
                    out_result = out_result+',"success":"0"'
                with open(result_file, 'a') as f:
                    f.write(str('{'+out_result+'}') + '\n')
            with open(result_file, 'a') as f:
                f.write(str('{"success_rate":"'+str(successnum/num)+'"}') + '\n')

    return result,result_class

# 识别 字母+数字
def predictAll(modelArgs,imgsdirs):
    result=""
    model = modelLoad(modelArgs)
    for imgdir in imgsdirs:
        if os.path.exists(imgdir):
            check_text = checkImages(imgdir, model)
            if check_text!=None:
                result+= check_text


# 清楚无效图片
def clearInvalidImgs(imgsdirs):
    for path in imgsdirs:
        imgs = os.listdir(path)
        num = len(imgs)
        for i in range(num):
            img = cv2.imread(path + imgs[i], 0)  # 直接读为灰度图像
            if (img is None):
                print(imgs[i])
                os.remove(path + imgs[i])


# predict the model result
def predictObjects(architecture, weights, predictpath):
    modelArgs = [project_dir + '/trainmodel/' + architecture,project_dir+'/trainmodel/'+weights]
    model = modelLoad(modelArgs)
    return checkImages(predictpath, model)

# predict the model result
def predictObjects(architecture, weights, predictpath,type):
    modelArgs = [project_dir + '/trainmodel/' + architecture,project_dir+'/trainmodel/'+weights]
    model = modelLoad(modelArgs)
    return checkImages(predictpath, model,type)

# predict the model result
def predictObjects(architecture, weights, predictpath,type,isresulttxt=False):
    modelArgs = [project_dir + '/trainmodel/' + architecture,project_dir+'/trainmodel/'+weights]
    model = modelLoad(modelArgs)
    return checkImages(predictpath, model,type,isresulttxt)