#复制目录下文件
scp -r original/upper_src/K_* numberAndUpper/upper_train/
scp -r wangjianmei@10.169.46.80:~/ssl_cp.conf ~/

#随机移动目录1下1000个文件到目录2
python ~/project/PJ_DATA_IMG/creatTrainDataSet/main.py moveimgs  numberAndUpper/upper_train/ numberAndUpper/upper_test/ 9000
python ~/project/PJ_DATA_IMG/creatTrainDataSet/main.py moveimgs  numberAndX/number_train/ numberAndX/number_test/ 10000
#清除坏图片
python ~/project/PJ_DATA_IMG/creatTrainDataSet/main.py clearimgs  numberAndX/number_train/

#生成图片--移动像素
python ~/project/PJ_DATA_IMG/creatTrainDataSet/main.py makeimgs movepix ~/mydataset/original/tmp/ 1 \(0,-1\)

#生成图片--椒盐加噪，每个图片生成2个新图
python main.py makeimgs salt ~/mydataset/numberAndUpper/upper_train/

#生成图片--高斯加噪，每个图片生成3个新图
python main.py makeimgs gussia ~/mydataset/numberAndUpper/upper_train/

#验证图片识别率:
python ~/project/PJ_DATA_IMG/train/keras_predict.py architecture_upper_number_0.json weights_upper_number_0.h5 /home/autoai/mydataset/original/upper_src_good/
# 启动 查看图片验证结果
python ~/project/PJ_DATA_IMG/data_check/predict_result.py
# 启动data_check/main.py
python ~/project/PJ_DATA_IMG/data_check/main.py



