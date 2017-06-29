# -*- coding: utf-8 -*-

no_chars = "0123456789ABCDEFGHIGKLMNOPQRSTUVWXYZ"
def process(no):
    result=''
    if not no ==None:
        for char in no:
            if char == 'o' or char == 'O':
                char = "0"
            if char == 'i' or char == 'I':
                char = "1"
            if char in no_chars:
                result += char

    return result

def check(code):
    try:
        ERROR = None
        if len(code) != 17 :
             ERROR ='长度不符合要求'
        else:
            pass

        if ERROR== None:
            return True
        else:
            #print("code;",code,";",ERROR)
            return False
    except Exception  :
        print("未知错误")
        return False
