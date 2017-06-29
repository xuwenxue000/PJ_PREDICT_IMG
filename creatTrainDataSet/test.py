import numpy as np
import cv2
import os,keras
import mydataset

(img_from_dir,img_to_dir) = mydataset.getmydatasetdir(0)
"""
#img = np.zeros((28, 28), np.uint8)
#img = np.matrix((28, 28), np.uint8)
img = np.full((28, 28), 255,np.uint8)
#print img
font = cv2.FONT_ITALIC
img = cv2.putText(img,'A', (2, 24), font, 1, (0, 0, 0), 2)
#cv2.cvthreshold(img)
#cv2.cvNot(img)
cv2.imwrite(img_to_dir +'tmp/A.png', img)
cv2.imwrite(img_to_dir +'tmp/A.jpg', img)

filename = 'A.jpg'
name = filename.split('.')[1]
#print name

img = cv2.imread('../tmp_predict/0.jpg',0)
print ~img




config = tf.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.Session(config=config, ...)


# (keras.backend._config)


rows, cols = img.shape
for v in (1,2,3,-1,-2,-3):
#for v in range(1,12):
    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), v*15,1)
    #dst = cv2.warpAffine(img, M, (cols, rows),borderValue=255)
    dst = cv2.warpAffine(img, M, (cols, rows))
    cv2.imwrite('turn_'+str(v*15)+'.jpg', dst)
"""
num_test=3
testpath= img_to_dir+'/number_test_4/'
imgs_test = os.listdir(testpath)
x_test = np.empty((num_test, 1, 28, 28), dtype="float32")
y_test = np.empty((num_test,), dtype="uint8")

for i in range(num_test):
    img = cv2.imread(testpath + imgs_test[i], 0)  # 直接读为灰度图像
    if img is None:
        print(imgs[i])
        # os.remove(trainpath + imgs[i])
    else:
        im = Image.fromarray(img, None)
        # arr = np.asarray(im, dtype="float32")
        arr = np.array(im, dtype="float32")
        x_test[i, :, :, :] = arr
        y_test[i] = int(imgs[i].split('.')[0][0])