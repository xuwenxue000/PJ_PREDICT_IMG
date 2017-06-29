# -*- coding: utf-8 -*-

import api_common.utils.log as logger
no_chars = "0123456789-ABCDEFGHIGKLMNOPQRSTUVWXYZ"
def process(no):
    result=''
    if not no ==None:
        for char in no:
            if char == 'o' or char == 'O':
                char = "0"
            if char in no_chars:
                result += char

    return result

def check(code):
    try:
        ERROR = None
        if len(code) < 6 :
             ERROR ='长度不符合要求'
        else:
            pass

        if ERROR== None:
            return True
        else:
            logger.info("code;",code,";",ERROR)
            return False
    except Exception  :
        logger.info("未知错误")
        return False
