import re
#Errors=['验证通过!','身份证号码位数不对!','身份证号码出生日期超出范围或含有非法字符!','身份证号码校验错误!','身份证地区非法!']
import api_common.utils.log as logger


chars = "0123456789.¥"
def process(code):
    result=''
    if not code ==None:
        for char in code:

            if char == 'o' or char == 'O':
                char = '0'
            #print(char)
            if char in chars:
                result += char
        index = result.find("¥")
        if index>0:
            result = result[index:]

    return result


def check(code):
    try:
        ERROR = None
        if not "¥" in code :
             ERROR ='无人民币符号'
        else:
            pass
        if not "." in code:
            ERROR = '无小数点'
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
