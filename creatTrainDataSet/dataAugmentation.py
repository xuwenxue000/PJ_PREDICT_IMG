# -*- coding: utf-8 -*-
__author__ = 'wangjianmei'

# import packages
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img

datagen = ImageDataGenerator(
        rotation_range=0.2,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest')

img = load_img('C:\Users\Administrator\Desktop\dataA\lena.jpg')  # this is a PIL image, please replace to your own file path
x = img_to_array(img)  # this is a Numpy array with shape (3, 150, 150)
x = x.reshape((1,) + x.shape)  # this is a Numpy array with shape (1, 3, 150, 150)

# the .flow() command below generates batches of randomly transformed images
# and saves the results to the `preview/` directory

i = 0
for batch in datagen.flow(x,
                          batch_size=1,
                          save_to_dir='C:\Users\Administrator\Desktop\dataA\pre',#生成后的图像保存路径
                          save_prefix='lena',
                          save_format='jpg'):
    i += 1
    if i > 20:
        break  # otherwise the generator would loop indefinitely