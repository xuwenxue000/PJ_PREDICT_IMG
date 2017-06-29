#!/usr/bin/python
#-*- encoding:utf-8 -*-

'''Trains a simple convnet on the MNIST dataset.
Gets to 99.25% test accuracy after 12 epochs
(there is still a lot of margin for parameter tuning).
16 seconds per epoch on a GRID K520 GPU.
'''

from __future__ import print_function

# 公共参数
import os
import sys
py_dir = os.path.dirname(os.path.realpath(__file__))
project_dir = os.path.dirname(py_dir)
sys.path.append(project_dir)

import creatTrainDataSet.mydataset as mydataset
import train.predictapi as predictapi

#if __name__=="__main__":
(img_from_dir, img_to_dir) = mydataset.getmydatasetdir(0)
params = sys.argv  #
print (params)
architecture ='architecture_upper_number_0.json'
weights = 'weights_upper_number_0.h5'
predictpath = project_dir + '/tmp_predict/tmp/'

if len(sys.argv) < 4:
    pass
else:
    architecture = sys.argv[1]
    weights = sys.argv[2]
    predictpath = sys.argv[3]

result,result_class = predictapi.predictObjects(architecture, weights, predictpath,0)
print (result_class)
print (result)




