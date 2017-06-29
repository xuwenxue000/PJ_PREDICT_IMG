#-*-encoding:utf-8-*-
"""
    这里是创建训练数据集的入口（生成图片）

"""
import os,sys,shutil
# public define
py_dir = os.path.dirname(os.path.realpath(__file__))
project_dir = os.path.dirname(py_dir)
sys.path.append(project_dir)

import creatTrainDataSet.mydataset as mydataset
import creatTrainDataSet.createTrainDateSet as createTrainDateSet

(img_from_dir,img_to_dir) = mydataset.getmydatasetdir(0)


#生成全部训练数据集合
def makeImgs(sourcepath,targetpath):
    print (sourcepath,targetpath)
    mydataset.clear(sourcepath)

    if os.path.isdir(targetpath):
        mydataset.clear(targetpath)
        shutil.rmtree(targetpath)
        os.mkdir(targetpath)
    else:
        os.mkdir(targetpath)

    createTrainDateSet.img_copy(sourcepath,targetpath)
    createTrainDateSet.img_move(sourcepath,targetpath)
    #img_turn(sourcepath,targetpath)             # step1 对原图几何变换
    #img_affineTransform(sourcepath,targetpath)  # step2 放射变换(对原图放射变换)
    #turnAndTransform_file(targetpath)           # step3 放射变换(对几何变换图+放射变换)
    createTrainDateSet.img_line(targetpath, targetpath)            # step2 对原图划线
    createTrainDateSet.addGussiaNoise(targetpath)                  # step4 所有图片加噪音（原图+几何图+放射图+几何放射图）
    createTrainDateSet.addSaltNoise(targetpath)                    # step5 所有图片加噪音（原图+几何图+放射图+几何放射图）

def chooseRandomImgs(sourcepath,targetpath,num):
    mydataset.chooseRandomImgs(img_to_dir + sourcepath,img_to_dir + targetpath, num)


params = sys.argv
print (params)
if len(sys.argv)>=2:
    param = str(sys.argv[1])
    if param =='makeimgs':
        action = sys.argv[2]
        if action =='movepix' and len(sys.argv)>= 5 and len(sys.argv)== 6:
            sourcepath = sys.argv[3]
            numpixs = int(sys.argv[4])
            direction = tuple(eval(sys.argv[5]))
            if len(direction) == 2:
                createTrainDateSet.img_move(sourcepath, sourcepath, numpixs=numpixs, direction=direction)
                print("OK")
            else:
                print("direction is error : ,please input direction=(x,y)")

        elif action=='salt' and len(sys.argv)== 4:
            targetpath = sys.argv[3]
            createTrainDateSet.addSaltNoise(targetpath)
        elif action == 'gussia' and len(sys.argv)== 4:
            targetpath = sys.argv[3]
            createTrainDateSet.addGussiaNoise(targetpath)
        elif action=='image_adjust' and len(sys.argv)==4:
            targetpath = sys.argv[3]
            createTrainDateSet.image_adjust(targetpath)

        #pass
    elif param == 'moveimgs' and len(sys.argv)== 5:
        sourcepath = sys.argv[2]
        targetpath = sys.argv[3]
        num = int(sys.argv[4])
        chooseRandomImgs(sourcepath, targetpath, num)
        print ("OK")
    elif param == 'clearimgs' and len(sys.argv) == 3:
        path = sys.argv[2]
        print("clear path : ",img_to_dir+path)
        if os.path.isdir(img_to_dir+path):
            mydataset.clear(img_to_dir+path)
        print("OK")
    else:
        print ("cmd error")


# 生成原图
#createOriginalImage.createNumberImg(img_from_dir+'number/')
#createOriginalImage.createUpperLetterImg(img_from_dir+'upper3/')
#createOriginalImage.createLowerLetterImg(img_from_dir+'lower/')
#createChineseImg()

#mydataset.clear(img_from_dir + 'numberAndUpper/upper/')
#createTrainDateSet.img_turn(img_from_dir + 'numberAndUpper/upper_tmp/',img_from_dir + 'numberAndUpper/upper_tmp/')
#createTrainDateSet.img_move(project_dir + '/tmp_predict/test1/',project_dir + '/tmp_predict/test1/',direction=(0,-1),numpixs=2)
#createTrainDateSet.image_adjust(project_dir + '/tmp_predict/tmp/')
#createTrainDateSet.addGussiaNoise(project_dir + '/tmp_predict/test1/')
#createTrainDateSet.addSaltNoise(project_dir + '/tmp_predict/test1/')

# 训练库
# 生成数字图片,大写字母图片,小写字母图
#createTrainDateSet.makeImgs(img_from_dir + 'numberAndUpper/number/',img_to_dir + 'numberAndUpper/number_train/')
#createTrainDateSet.makeImgs(img_from_dir + 'numberAndUpper/upper_X/',img_to_dir + 'numberAndUpper/upper_X_train/')
#createTrainDateSet.makeImgs(img_from_dir + 'numberAndUpper/upper/',img_to_dir + 'numberAndUpper/upper_train/')
#createTrainDateSet.img_move(img_from_dir + 'numberAndUpper/upper/',img_to_dir + 'numberAndUpper/upper_train/')
#createTrainDateSet.makeImgs(img_from_dir + 'upper3/',img_to_dir + 'upper_train/')
#createTrainDateSet.makeImgs(img_from_dir + 'lower/', img_to_dir + 'lower_train/')

# 从训练库中选num个到验证库
#createTrainDateSet.copyRandomImgs(img_to_dir + 'number_train/',img_to_dir + 'number_predict/',100)
#createTrainDateSet.copyRandomImgs(img_to_dir + 'upper_train/',img_to_dir + 'upper_predict/',500,1)
#createTrainDateSet.copyRandomImgs(img_to_dir + 'upper_train_3_0/',img_to_dir + 'upper_test_3_0/',100,1)
#createTrainDateSet.copyRandomImgs(img_to_dir + 'lower_train/',img_to_dir + 'lower_predict/',2000)

# 从训练库中选num个移动到测试库
#createTrainDateSet.chooseRandomImgs(img_to_dir + 'numberAndUpper/number_train/',img_to_dir + 'numberAndUpper/number_test/',11000)
#createTrainDateSet.chooseRandomImgs(img_to_dir + 'numberAndUpper/upperX_train/',img_to_dir + 'numberAndUpper/upperX_test/',300)
#createTrainDateSet.chooseRandomImgs(img_to_dir + '/numberAndUpper/upper_train/',img_to_dir + '/numberAndUpper/upper_test/',20000,1)
#createTrainDateSet.chooseRandomImgs(img_to_dir + 'lower_train/',img_to_dir + 'lower_test/',20000,1)