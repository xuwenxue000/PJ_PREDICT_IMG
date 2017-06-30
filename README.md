PJ_PREDICT_IMG - A IMG PREDICT Tool,Only suppport Invoice now(图片识别工具,目前仅支持发票识别)
====================================================================================================
  此项目用于对中国购车发票进行内容识别,目前完成的是身份证,vin,发动机号,价格的识别
  提供了展示的demo页,以及提供了传入文件,路径,base64码的多种方式调用的api,返回识别出来的json数据

How To Get
-------------
    git clone https://github.com/xuwenxue000/PJ_PREDICT_IMG.git


Installation
------------
    brew install python3
    brew install mysql
    brew install --with-training-tools tesseract
    brew install opencv3 --with-ffmpeg --with-python3 --c++11 --with-contrib --force
    
    pip3 install tornado
    pip3 install mysqlclient
    pip3 install PILLOW
    pip3 install tensorflow
    pip3 install keras


Quick Start
-------------
- 首先找一张发票的图片:

    - 百度搜索出来的图片:
        https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1498711297986&di=5684845f9c4904b92523a608ff2ed370&imgtype=0&src=http%3A%2F%2Fclub2.autoimg.cn%2Falbum%2Fg13%2FM0F%2FA4%2FA3%2Fuserphotos%2F2015%2F10%2F10%2F21%2F500_wKgH1FYZE2mALP-JAAJQY1pp49o236.jpg
    - 找到原图地址:
        http://club2.autoimg.cn/album/g13/M0F/A4/A3/userphotos/2015/10/10/21/500_wKgH1FYZE2mALP-JAAJQY1pp49o236.jpg

- 启动识别服务(web接口服务)
    ```
        ./api_invoice/main.py
    ```
    开启的是8888端口,暂时未做配置化,可以直接在main.py中修改

- 访问demo页
    - 访问http://128.0.0.1:8888/invoice/index
    - 选择上传图片,会识别出来图片并将结果显示在页面上
    - 并显示识别的方法和识别定位的图片
- 访问接口:
    - http://127.0.0.1:8888/invoice/url?url=http%3A%2F%2Fclub2.autoimg.cn%2Falbum%2Fg13%2FM0F%2FA4%2FA3%2Fuserphotos%2F2015%2F10%2F10%2F21%2F500_wKgH1FYZE2mALP-JAAJQY1pp49o236.jpg
    - 传入图片连接,返回json数据,例如:
    {
    "cardno": "130102198707041249",
    "vinno": "LSGHD5289FD298030",
    "engineno": "152306132",
    "price": "¥61500.00"
    }
    - 还支持上传文件,图片base64字符串传参等多种方式




OtherInfo
-------------
# 代码执行过程说明
- 使用tornado启动web服务,json格式化数据
- 首先对图片做处理,opencv,PIL,找到需要识别的局部图片并截取出来
    - 图像处理方式
        - 使用二值化加上轮廓等方法找到图片中最大方格,然后找到四个点
        - 对四个点对应的四边形进行矫正,变成正方形,使得字体不会是歪的
        - 检查长宽,处理横竖图片问题,这里还可以改进优化
        - 缩放到固定大小
        - 生成一张翻转的图片,因为暂时无法确定是否倒过来的,暂时做识别两次的处理,可以优化
        - 然后按照比例切出对应识别区域
        - 最后把这个局部的图片切割出来
        - 缺点是部分图片的方格不完整,图片打印的比较歪,明暗度差异的问题会导致识别准确率下降
    - 深度学习图片定位方式
        - 使用darknet的yolo定位的方法,标识一批样本中关键数据的局部图片的位置
        - 然后进行训练
        - 训练完成后会得出一个权重文件
        - 改造darknet的代码
            - 为了能够更快的处理,在darknet里面启动了一个web服务
            - 可以传入图片地址(服务器绝对地址,无后缀)
            - 识别后返回图片中关键局部位置的坐标点
            - 再使用坐标点将图片的关键部位切割出来
            - 效果还好,主要是识别速度稍慢,作为第二方案,还有优化余地,甚至可以替代第一方案
- 图片定位切割完成之后,做正向反向识别
        - 首先使用机器识别
            - 先将图片再次切割,根据灰度值和波峰波谷算法将每个字符切割开
            - 使用训练好的但字符模型镜像识别,有三个不同的模型,依次进行识别
        - 其次使用tesseract识别
            - 原图识别
            - 灰度图识别
            - 默认阈值二值化识别
            - 批量默认阈值二值化识别
            - 遍历阈值二值化识别
- 识别结果校验
     - 如果不通过校验,则继续往下走

# 识别率校验
- 将图片网络地址放到img.txt中,文件放到data/invoice目录下
- 执行ipi_invoice/test.py,将文件导入到数据库
- 然后删除img.txt文件
- 继续执行执行ipi_invoice/test.py,将会逐个识别并将结果记录到数据库,
- 通过sql可以判断出来识别率


# 单图识别训练:
- 模型训练
    - 训练出的模型包括：识别10个数字类别模型；用于身份证识别的 识别"数字+X" 11个类别的模型；识别"大写字母+数字" 26个类别的模型。
    - 训练样本处理的目录为/creatTrainDataSet, 模型训练的目录为 /train/
        -准备图片：本项目将发票系统中的数字，字母图片切割出来，转换成统一的28*28图片
        - 为尽可能提高训练模型识别率，将图片做相应处理，剔除噪声较多的图片，尤其是每一类别有相同噪声的图片。
        - 已经处理好的训练样本图片见压缩包：/dataset/numberAndX.tar.gz,/dataset/numberAndUpper.tar.gz，解压缩到自定义目录
        - 修改/train目录下相应的模型训练文件，生成对应训练模型，已有模型在目录/trainmodel/下
        - 修改/train/keras_predict.py中需要识别的的图片路径或目录，使用已有模型识别图片类型。
    
# darknet图片定位
    详情见另一项目darknet
    https://github.com/xuwenxue000/PJ_DARKNET

         
         
     

其他说明:
    代码的识别暂时对身份证号码的时候做了比较多的优化,3w张发票识别率达到95以上,其他的暂未优化
