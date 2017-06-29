import tornado.web
import shutil
import sys,os


#公共参数
py_dir = os.path.dirname(os.path.realpath(__file__))
project_dir = os.path.dirname(py_dir)
sys.path.append(project_dir)
file_path='/home/autoai/mydataset/original/'
file_del_path='/home/autoai/mydataset/original/'
Errors={}
Errors["403"]={"returncode":403,"message":"access forbid"}



class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.post()

    def post(self):
        prefix = self.get_argument("prefix",default='')
        start = int(self.get_argument("start", default=0))
        limit = int(self.get_argument("limit", default=100))
        check_dir = self.get_argument("check_dir", default='upper2_src')
        check_path = file_path + check_dir
        moveto_dir = self.get_argument("moveto_dir", default='upper_del')
        moveto_path = file_path + moveto_dir

        imgs=[]
        files = os.listdir(check_path)
        if prefix and prefix != '':

            if files:
                for f_name in files:
                    if f_name.startswith(prefix):
                        imgs.append(f_name)
        else:
            if files:
                for f_name in files:
                    imgs.append(f_name)
        end = start+limit
        if end >= len(imgs):
            end = len(imgs)-1
        self.render("demo.html", imgs=imgs[start:end], start=start, limit=limit, total=len(imgs),prefix=prefix,check_dir=check_dir,moveto_dir=moveto_dir)

class FileHandler(tornado.web.RequestHandler):
    def get(self):
        uri = self.request.uri
        file_name = self.get_argument("img", default='')
        check_dir = self.get_argument("check_dir", default='upper2_src')
        check_path = file_path + check_dir
        data = None
        if os.path.exists(check_path+"/"+file_name):
            #application/octet-stream
            self.set_header('Content-Type', 'image/jpeg')
            with open(check_path+"/"+file_name, 'rb') as f:
                data = f.read()
        if not data:
            data = 'not find this file'
        self.write(data)

class DelHandler(tornado.web.RequestHandler):
    def get(self):
        uri = self.request.uri
        #file_name = uri[16:]
        file_name = self.get_argument("img", default='')
        if file_name is None or file_name=='':
            return
        check_dir = self.get_argument("check_dir", default='upper2_src')
        check_path = file_path + check_dir
        moveto_dir = self.get_argument("moveto_dir", default='upper_del')
        moveto_path = file_path + moveto_dir
        if os.path.exists(check_path + "/" + file_name):
            shutil.move(check_path+"/"+file_name,moveto_path+"/"+file_name)
            pass
        self.write("ok")

class RenameHandler(tornado.web.RequestHandler):
    def get(self):
        file_name = self.get_argument("img", default='')
        if file_name is None or file_name=='':
            return
        check_dir = self.get_argument("check_dir", default='upper2_src')
        check_path = file_path + check_dir

        newname = self.get_argument("newname")
        file_newname = newname + file_name[1:]

        if os.path.exists(check_path + "/" + file_name):
            shutil.move(check_path+"/"+file_name,check_path+"/"+file_newname)
            pass
        self.write("ok")

application=tornado.web.Application([
    (r'/data_check/index',IndexHandler),
    (r'/data_check/del',DelHandler),
    (r'/data_check/file',FileHandler),
    (r'/data_check/rename',RenameHandler),
])

if __name__=="__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()