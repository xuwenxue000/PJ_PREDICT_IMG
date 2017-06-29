# -*-encoding:utf-8-*-
import api_invoice.config.db as db_config
table_name = "pe_log"


class PeLog:
    def __init__(self, dict_row=None):
        if dict_row:
            self.id = dict_row.get("id")
            self.created = dict_row.get("created")
            self.modified = dict_row.get("modified")
            self.content = dict_row.get("content")
            self.type = dict_row.get("type")
            self.level = dict_row.get("level")
            self.data_id = dict_row.get("fk_data_id")
        else:
            self.id = None
            self.created = None
            self.modified = None


def insert(log):
    sql = "INSERT INTO  "+table_name+" (content,type,level,fk_data_id) VALUES (%s,%s,%s,%s)"
    #print(sql)
    db = db_config.get_db()
    result =db.execute(sql, log.content, log.type, log.level,log.data_id)
    return result

#机器识别处理来的数据
def info(content,type,data_id):
    log(content,type,data_id,"INFO")

#未识别出来的数据
def error(content,type,data_id,):
    log(content,type,data_id,"ERROR")

#不是用机器识别出来的数据
def warn(content,type,data_id):
    log(content,type,data_id,"ERROR")


def log(content,type,data_id,level):
    log = PeLog()
    log.level=level
    log.content=content
    log.type=type
    log.data_id=data_id
    insert(log)






