#-*-encoding:utf-8-*-
import os,cv2,random
import shutil

# 定义数据集存储目录,flag=1 代表服务器路径  flag=0代表本地路径
def getmydatasetdir(flag):
    if flag == 1:
        img_from_dir = '/home/autoai/mydataset/original/'
        img_to_dir = '/home/autoai/mydataset/'
    elif flag == -1:
        img_from_dir = '/Volumes/Transcend/ijob/mydataset/original/'
        img_to_dir = '/Volumes/Transcend/ijob/mydataset/'
    else:
        if os.path.exists('/home/autoai/mydataset/'):
            img_from_dir = '/home/autoai/mydataset/original/'
            img_to_dir = '/home/autoai/mydataset/'
        else:
            img_from_dir = '/Volumes/Transcend/ijob/mydataset/original/'
            img_to_dir = '/Volumes/Transcend/ijob/mydataset/'

    return (img_from_dir,img_to_dir)

# 清楚无效图片
def clear(path):
    if os.path.exists(path):
        imgs = os.listdir(path)
        num = len(imgs)
        for i in range(num):
            img = cv2.imread(path + imgs[i], 0)  # 直接读为灰度图像
            if (img is None):
                print(imgs[i])
                os.remove(path + imgs[i])

#从sourcepath中随机选取num个数据,移动到targetpath中,iscleartargetpath为是否清除原有数据
def chooseRandomImgs(sourcepath,targetpath,num,iscleartargetpath=1):
    if iscleartargetpath:
        if os.path.isdir(targetpath):
            shutil.rmtree(targetpath)
            os.mkdir(targetpath)
        else:
            os.mkdir(targetpath)

    files = os.listdir(sourcepath)
    if(len(files)<num):
        num = len(files)

    slice = random.sample(files,num)  # 从list中随机取num个数据，每次取的不一致
    for file in slice:
        shutil.move(sourcepath+file, targetpath + file)

#从sourcepath中随机选取num个数据,复制到targetpath中,iscleartargetpath为是否清除原有数据
def copyRandomImgs(sourcepath,targetpath,num,iscleartargetpath=1):
    if iscleartargetpath:
        if os.path.isdir(targetpath):
            shutil.rmtree(targetpath)
            os.mkdir(targetpath)
        else:
            os.mkdir(targetpath)

    files = os.listdir(sourcepath)
    if(len(files)<num):
        num = len(files)

    slice = random.sample(files,num)  # 从list中随机取num个数据，每次取的不一致
    for file in slice:
        shutil.copy(sourcepath+file, targetpath + file)