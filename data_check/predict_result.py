import tornado.web
import shutil
import sys,os,json


#public params
py_dir = os.path.dirname(os.path.realpath(__file__))
project_dir = os.path.dirname(py_dir)
sys.path.append(project_dir)
import train.predictapi as predictapi

file_path='/home/autoai/mydataset/original/'
predict_resutl_path = project_dir +'/tmp_predict/'
Errors={}
Errors["403"]={"returncode":403,"message":"access forbid"}



class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.post()

    def post(self):
        prefix = self.get_argument("prefix", default='')
        start = int(self.get_argument("start", default=0))
        limit = int(self.get_argument("limit", default=100))
        filename = self.get_argument("filename",default='result.txt')
        moveto_dir = self.get_argument("moveto_dir", default='upper_del')
        architecture = self.get_argument("architecture",default='')
        weights = self.get_argument("weights", default='')
        check_dir =self.get_argument("check_dir", default='')
        order = self.get_argument("order",default='')

        imgs = []
        success_rate=0

        success_num=0
        result_file = os.path.join(predict_resutl_path, filename)
        if os.path.isfile(result_file):
            f = open(result_file)
            for eachLine in f:
                line = eachLine.strip()
                line = line.strip(',')

                js = None
                try:
                    # print(line)
                    js = json.loads(line)
                    if ('path') in js.keys():
                        check_dir = js["path"]
                    elif ('success_rate') in js.keys():
                        success_rate = js["success_rate"]
                        #print(js["success_rate"])
                    elif ('file_name') in js.keys():
                        f_name = js["file_name"]
                        if prefix and prefix != '':
                            if f_name.startswith(prefix):
                                success = js["success"]
                                if success =='1':
                                    success_num = success_num+1

                                if order=='':
                                    imgs.append(js)
                                elif order==success:
                                    imgs.append(js)

                        else:
                            success = js["success"]
                            if order == '':
                                imgs.append(js)
                            elif order == success:
                                imgs.append(js)

                except Exception as e:
                    print(e)
                    continue
                finally:
                    pass
        end = start + limit
        if prefix and prefix != '' and success_num > 0 and len(imgs)>0:
            success_rate = success_num/len(imgs)
        if end >= len(imgs):
            end = len(imgs)
        self.render("predict_result.html", imgs=imgs[start:end],start=start, limit=limit, total=len(imgs),prefix=prefix,filename=filename,check_dir=check_dir,moveto_dir=moveto_dir,success_rate=success_rate,file_path=file_path,predict_resutl_path=predict_resutl_path,architecture=architecture,weights=weights)

class FileHandler(tornado.web.RequestHandler):
    def get(self):
        uri = self.request.uri
        file_name = self.get_argument("img", default='')
        check_path = self.get_argument("check_dir", default='')
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
        check_path = self.get_argument("check_dir", default='')
        #check_path = file_path + check_dir
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
        check_path = self.get_argument("check_dir", default='')
        #check_path = file_path + check_dir

        newname = self.get_argument("newname")
        file_newname = newname + file_name[1:]

        if os.path.exists(check_path + "/" + file_name):
            shutil.move(check_path+"/"+file_name,check_path+"/"+file_newname)
            pass
        self.write("ok")

class RepredictHandler(tornado.web.RequestHandler):
    def get(self):
        architecture = self.get_argument("architecture", default='')
        if architecture is None or architecture=='':
            return
        weights = self.get_argument("weights", default='')
        if weights is None or weights == '':
            return
        check_dir = self.get_argument("predict_dir", default='')
        if check_dir is None or check_dir == '':
            return

        if os.path.exists(check_dir):
            #print(architecture)
            #print(weights)
            result,result_class= predictapi.predictObjects(architecture, weights, check_dir, 0,isresulttxt=True)
            #print(result_class)
            #pass
        self.write("ok")

class TxtbakHandler(tornado.web.RequestHandler):
    def get(self):
        file_name = self.get_argument("filename", default='')
        if file_name is None or file_name=='':
            return
        filename_bak = self.get_argument("filename_bak", default='')
        if filename_bak is None or filename_bak=='':
            return
        result_file = os.path.join(predict_resutl_path, file_name)
        if os.path.isfile(result_file):
            shutil.copy(result_file,predict_resutl_path+filename_bak)
        self.write("copy success")

application=tornado.web.Application([
    (r'/predict_result/index',IndexHandler),
    (r'/predict_check/file',FileHandler),
    (r'/predict_check/del',DelHandler),
    (r'/predict_check/rename',RenameHandler),
    (r'/predict_check/repredict',RepredictHandler),
    (r'/predict_check/txt_bak',TxtbakHandler),


],debug=True)

if __name__=="__main__":
    application.listen(8889)
    tornado.ioloop.IOLoop.instance().start()