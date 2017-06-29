# -*- coding: utf-8 -*-

import string
CODEMAP = string.digits + string.ascii_uppercase # 用数字与大写字母拼接成CODEMAP，每个字符的index就是代表该字符的值
WMap = [3, 7, 9, 10, 5, 8, 4, 2] # 加权因子列表

cardno_chars = "0123456789-ABCDEFGHIGKLMNOPQRSTUVWXYZ"
def process(idcard):
    result=''
    if not idcard ==None:
        for char in idcard:
            if char == 'o' or char == 'O':
                char = "0"
            if char in cardno_chars:
                result += char

    return result
def get_C9(bref):
    # C9=11-MOD（∑Ci(i=1→8)×Wi,11）
    # 通过本地计算出C9的值
    sum = 0
    for ind, i in enumerate(bref):
        Ci = CODEMAP.index(i)
        Wi = WMap[ind]
        sum += Ci * Wi

    C9 = 11 - (sum % 11)
    if C9 == 10:
        C9 = 'X'
    elif C9 == 11:
        C9 = '0'
    return str(C9)


def check(code):
    # 输入组织机构代码进行判断，如果正确，则输出'验证通过，组织机构代码证格式正确！'，错误则返回错误原因
    try:
        ERROR = None
        if '-' in code:
            bref, C9_check = code.split('-')
        else:
            bref = code[:-1]
            C9_check = code[-1:]

        if len(bref) != 8 or len(C9_check) != 1:
             ERROR ='本体或校验码长度不符合要求'
        else:
            try:
                C9_right = get_C9(bref)
            except ValueError:
                ERROR = '本体错误'
            if C9_check != C9_right:
                ERROR = '校验码错误'
            else:
                pass
        if ERROR== None:
            return True
        else:
            #print("code;",code,";",ERROR)
            return False
    except Exception  :
        #print("未知错误")
        return False
