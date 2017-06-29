#!/usr/bin/env python3
#-*-encoding:utf-8-*-

import os,sys
import re
from urllib import request
import hashlib
import api_invoice.dao.invoice_dao as invoice_dao
import api_common.utils.log as logger
import cv2
#处理横竖问题
def getimgs(img_file,targetpath):
    logger.debug(img_file,targetpath)
    result=[]
    if os.path.exists(img_file) :
        with open(img_file, 'r') as f:
            for line in f.readlines():
                imgurl=line.strip()

                invoice = invoice_dao.get_invoice_by_src(imgurl)
                re_str = '.*/(.*)\.(.*)'
                re_pat = re.compile(re_str)
                search_ret = re_pat.search(imgurl)
                if search_ret:
                    #logger.debug(search_ret.groups())
                    file_name =search_ret.groups()[0]
                    #file_suffix=search_ret.groups()[1]
                    file_suffix = "jpg"
                    out_path=targetpath+'%s.%s' % (file_name,file_suffix)
                    img={}
                    img['name']=file_name
                    img['suffix']=file_suffix
                    img['path']=out_path
                    if not os.path.exists(out_path):
                        try:
                            logger.info(out_path)
                            request.urlretrieve(imgurl, out_path)
                            img = cv2.imread(out_path)
                            cv2.imwrite(out_path,img)
                            result.append(img)
                        except Exception as err:
                            pass
                            #logger.error(err)
                        finally:
                            pass
                    else :
                        result.append(img)

                    if invoice:
                        img["id"] = invoice.id
                    else:
                        if os.path.exists(out_path):
                            invoice = invoice_dao.PeInvoice()
                            invoice.file_src = imgurl
                            invoice.request_type = "file"
                            invoice.file_target=out_path
                            invoice.file_name=file_name
                            with open(out_path, 'rb') as of:
                                md5 = hashlib.md5()
                                md5.update(of.read())
                                md5_code = md5.hexdigest()
                            if not md5_code:
                                md5_code = ''
                            invoice.md5_code = md5_code
                            id = invoice_dao.insert(invoice)
                            #img["id"]=id
            return
    #从数据库中读取数据
    #invoices = invoice_dao.query_unprocess_data_random(100)
    invoices = invoice_dao.query_unprocess_data(20)
    if invoices and len(invoices)>0:
        for inv in invoices:
            img = build_file(targetpath, inv)
            result.append(img)
    return result


def build_file(targetpath,invoice):
    imgurl = invoice.file_src.strip()
    invoice = invoice_dao.get_invoice_by_src(imgurl)
    re_str = '.*/(.*)\.(.*)'
    re_pat = re.compile(re_str)
    search_ret = re_pat.search(imgurl)
    if search_ret:
        # logger.debug(search_ret.groups())
        file_name = search_ret.groups()[0]
        #file_suffix = search_ret.groups()[1]
        file_suffix = "jpg"
        out_path = targetpath + '%s.%s' % (file_name, file_suffix)
        img = {}
        img['name'] = file_name
        img['suffix'] = file_suffix
        img['path'] = out_path
        if not os.path.exists(out_path):
            try:
                logger.info(out_path)
                request.urlretrieve(imgurl, out_path)
                cv2_img = cv2.imread(out_path)
                cv2.imwrite(out_path, cv2_img)
            except Exception as err:
                pass
                # logger.error(err)
            finally:
                pass

        if invoice:
            img["id"] = invoice.id
    return img


def get_by_filenames(filenames,targetpath):
    result=[]
    for filename in filenames:
        invoices = invoice_dao.query_by_filename(filename)
        if invoices and len(invoices) > 0:
            for inv in invoices:
                img = build_file(targetpath, inv)
                result.append(img)
    return result