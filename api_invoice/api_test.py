import pycurl

from io import StringIO
from io import BytesIO
import  base64
import urllib.parse
import urllib.request
"""
b = BytesIO()
def write(bytes):
    print(bytes)

c = pycurl.Curl()
c.setopt(c.HEADERFUNCTION, b.write)
c.setopt(c.POST, 1)
c.setopt(c.URL, "http://127.0.0.1:8888/invoice/file")
c.setopt(c.HTTPPOST, [("file", (c.FORM_FILE, "/Users/william/Desktop/1.jpg"))])
c.perform()
#print(b.getvalue().decode('utf-8'))
b.close()
c.close()
print( "\n=========================")

"""

"""
file_path = "/Users/william/Desktop/1.jpg"
data=None
out= BytesIO();
with open(file_path, 'rb') as f:
    data=base64.b64encode(f.read()) #读取文件内容，转换为base64编码
print(data)

b = BytesIO()
c = pycurl.Curl()
c.setopt(c.HEADERFUNCTION, b.write)
c.setopt(c.POST, 1)
c.setopt(c.URL, "http://127.0.0.1:8888/invoice/data")

post_data_dic={}
post_data_dic["data"]=data
c.setopt(c.POSTFIELDS,urllib.parse.urlencode(post_data_dic))
c.perform()


b.close()
c.close()

"""


b = BytesIO()
c = pycurl.Curl()
c.setopt(c.HEADERFUNCTION, b.write)
c.setopt(c.POST, 1)
c.setopt(c.URL, "http://127.0.0.1:8888/invoice/url")

post_data_dic={}
post_data_dic["url"]="http://www1.autoimg.cn/album/ds/2015/10/23/10/09171200-7098-kf8h-5f53-n204a35c9l6e.jpg"
c.setopt(c.POSTFIELDS,urllib.parse.urlencode(post_data_dic))
c.perform()


b.close()
c.close()