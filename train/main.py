#-*-encoding:utf-8-*-
"""
    这里是整个图片训练的入口

"""
import dataload
#公共参数
import sys,os,cv2
py_dir = os.path.dirname(os.path.realpath(__file__))
project_dir = os.path.dirname(py_dir)
sys.path.append(project_dir)
import creatTrainDataSet.mydataset as mydataset

'''
# 加载数据
trainpath = '/Volumes/Transcend/ijob/filesoutput/upper_train/'
#(x_train, y_train), (x_test, y_test) = dataload.loadAlphabet_data(trainpath, 60, trainpath, 10)
#print (x_train, y_train)

trainpaths = [['/Volumes/Transcend/ijob/filesoutput/temp1/',4],['/Volumes/Transcend/ijob/filesoutput/temp2/',2]]
testpaths = [['/Volumes/Transcend/ijob/filesoutput/temp1/',1],['/Volumes/Transcend/ijob/filesoutput/temp2/',1]]
(x_train, y_train), (x_test, y_test) = dataload.loadNumberAndAlphabet_data(trainpaths, testpaths)
print (x_train, y_train)
'''


# 清楚无效图片
def clear(imgsdirs):
    for path in imgsdirs:
        imgs = os.listdir(path)
        num = len(imgs)
        for i in range(num):
            img = cv2.imread(path + imgs[i], 0)  # 直接读为灰度图像
            if (img is None):
                print(imgs[i])
                os.remove(path + imgs[i])

(img_from_dir,img_to_dir) = mydataset.getmydatasetdir(0)
imgsdirs = [img_to_dir+'tmp/']
clear(imgsdirs)
for imgsdir in imgsdirs:
    print (imgsdir)
    filenames = os.listdir(imgsdir)
    num = len(filenames)
    for i in range(0,num):
    #for i,filename in filenames:
        img = cv2.imread(imgsdir+filenames[i],0)
        res = cv2.resize(img, (28, 28))
        ret, thresh1 = cv2.threshold(res, 0, 255, cv2.THRESH_BINARY_INV)
        cv2.imwrite(imgsdir+str(i)+"_"+filenames[i],ret)
        #print filenames[i],img,res



