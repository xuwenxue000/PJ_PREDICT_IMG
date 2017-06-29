#-*-encoding:utf-8-*-
import tornado.web
import shutil
import sys,os

import uuid
import base64

from urllib import request
import json
#public params
py_dir = os.path.dirname(os.path.realpath(__file__))
project_dir = os.path.dirname(py_dir)
sys.path.append(project_dir)

import api_invoice.service.img as img
import api_common.utils.verify as verify
import api_common.utils.log as logger
upload_path="/data/invoice/upload/"
file_dir_img_root = project_dir+upload_path

env = sys.argv[0]

if env=='production':
    file_dir_img_root = "/data/invoice/upload/"
#logger.debug(file_dir_img_root)
if not os.path.exists(file_dir_img_root):
    os.makedirs(file_dir_img_root)
config={}
config["data_dir"]=file_dir_img_root

Errors={}
Errors["403"]={"returncode":403,"message":"access forbid"}

def clean_file(filename):
    return
    #logger.debug(filename)
    #logger.debug(os.path.join(file_dir_img_root, filename + '.jpg'))
    #logger.debug(os.path.join(file_dir_img_root, filename))
    if os.path.exists(os.path.join(file_dir_img_root,filename+'.jpg')):
        os.remove(os.path.join(file_dir_img_root,filename+'.jpg'))
    if os.path.exists(os.path.join(file_dir_img_root,filename)):
        shutil.rmtree(os.path.join(file_dir_img_root,filename))

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('''
<html>
  <head><title>Upload File</title></head>
  <body>
    <form action='/invoice/index' enctype="multipart/form-data" method='post'>
    <input type='file' name='file'/><br/>
    <input type='submit' value='submit'/>
    </form>
  </body>
</html>
''')
    def get_base64(self,file):
        data = None
        with open(file, 'rb') as f:
            data = base64.b64encode(f.read())  # 读取文件内容，转换为base64编码
        return data


    def post(self):

        #upload_path=os.path.join(os.path.dirname(__file__),'files')  #文件的暂存路径
        upload_path=file_dir_img_root
        logger.debug(upload_path);
        #os.mkdir(upload_path)
        file_metas=self.request.files['file']    #提取表单中‘name’为‘file’的文件元数据
        for meta in file_metas:
            filename=str(uuid.uuid1())
            filepath=os.path.join(upload_path,filename+'.jpg')
            #rint(str(meta))
            #filename = meta['filename']
            with open(filepath,'wb') as up:      #有些文件需要已二进制的形式存储，实际中可以更改
                up.write(meta['body'])
            result = img.img_process(filepath,config)
            file_path_src = result.get("file_path_src")
            cardno_file = result.get("cardno_file")
            cardno_buildfile = result.get("cardno_buildfile")
            engineno_file = result.get("engineno_file")
            engineno_buildfile = result.get("engineno_buildfile")
            vinno_file = result.get("vinno_file")
            vinno_buildfile = result.get("vinno_buildfile")
            price_file = result.get("price_file")
            price_buildfile = result.get("price_buildfile")

            img_data={}
            img_data["src"]=self.get_base64(file_path_src)
            if cardno_file!=None and  os.path.exists(cardno_file):
                img_data["cardno"]=self.get_base64(cardno_file)
            if engineno_file!=None and os.path.exists(engineno_file):
                img_data["engineno"]=self.get_base64(engineno_file)
            if vinno_file!=None and os.path.exists(vinno_file) :
                img_data["vinno"]=self.get_base64(vinno_file)
            if cardno_buildfile != None and os.path.exists(cardno_buildfile):
                img_data["cardno_buildfile"] = self.get_base64(cardno_buildfile)
            if engineno_buildfile != None and os.path.exists(engineno_buildfile):
                img_data["engineno_buildfile"] = self.get_base64(engineno_buildfile)
            if vinno_buildfile != None and os.path.exists(vinno_buildfile):
                img_data["vinno_buildfile"] = self.get_base64(vinno_buildfile)
            if price_file != None and os.path.exists(price_file):
                img_data["price"] = self.get_base64(price_file)
            if price_buildfile != None and os.path.exists(price_buildfile):
                img_data["price_buildfile"] = self.get_base64(price_buildfile)
            print(result)
            info = result.get("info")
            log = result.get("log")
            debug = result.get("debug")
            log["cardno_machine_default"]=debug.get("cardno_machine_default")
            log["engineno_machine_default"] = debug.get("engineno_machine_default")
            log["vinno_machine_default"] = debug.get("vinno_machine_default")
            log["cardno_tesseract_default"] = debug.get("cardno_tesseract_default")
            log["engineno_tesseract_default"] = debug.get("engineno_tesseract_default")
            log["vinno_tesseract_default"] = debug.get("vinno_tesseract_default")
            log["price_machine_default"] = debug.get("price_machine_default")
            log["price_tesseract_default"] = debug.get("price_tesseract_default")
            clean_file(filename)
            self.render("demo.html", img_data=img_data,info=info,log=log)
            #self.write('result:'+str(result.get("info")))

class ApiFileHandler(tornado.web.RequestHandler):
    def post(self):
        _appid = self.get_argument("_appid")
        _token = self.get_argument("_token")
        if not verify.check_token(_appid,_token):
            self.write(Errors.get("403"))
        upload_path = file_dir_img_root
        logger.debug(upload_path);

        file_metas = self.request.files['file']  # 提取表单中‘name’为‘file’的文件元数据
        for meta in file_metas:
            filename = str(uuid.uuid1())
            filepath = os.path.join(upload_path, filename + '.jpg')
            logger.debug(str(meta))
            with open(filepath, 'wb') as up:  # 有些文件需要已二进制的形式存储，实际中可以更改
                up.write(meta['body'])
            result = img.img_process(filepath, config)
            self.write(str(result))


class ApiDataHandler(tornado.web.RequestHandler):
    def post(self):
        _appid = self.get_argument("_appid")
        _token = self.get_argument("_token")

        if not verify.check_token(_appid, _token):
            self.write(Errors.get("403"))
        upload_path = file_dir_img_root
        logger.debug(upload_path);
        data = self.get_argument("data")
        data = base64.b64decode(data)
        #data = base64.
        filename = str(uuid.uuid1())
        filepath = os.path.join(upload_path, filename + '.jpg')
        with open(filepath, 'wb') as up:  # 有些文件需要已二进制的形式存储，实际中可以更改
            up.write(data)
        result = img.img_process(filepath, config)
        self.write(str(result))
class UrlHandler(tornado.web.RequestHandler):
    def post(self):
        #_appid = self.get_argument("_appid")
        #_token = self.get_argument("_token")

        #if not verify.check_token(_appid, _token):
        #    self.write(Errors.get("403"))

        upload_path = file_dir_img_root
        logger.debug(upload_path);
        url = self.get_argument("url")

        #data = base64.
        filename = str(uuid.uuid1())
        filepath = os.path.join(upload_path, filename + '.jpg')
        request.urlretrieve(url, filepath)
        result = img.img_process(filepath, config)
        if result:
            self.write(json.dumps(result.get("info")))
        else :
            self.write("predict error")

    def get(self):
        self.post()


application=tornado.web.Application([
    (r'/invoice/index',IndexHandler),
    (r'/invoice/file',ApiFileHandler),
    (r'/invoice/data',ApiDataHandler),
    (r'/invoice/url',UrlHandler),
],debug=True)

if __name__=="__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()