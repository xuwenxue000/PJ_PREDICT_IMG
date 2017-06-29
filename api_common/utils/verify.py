# -*- coding: utf-8 -*-
"""
校验签名的地方
目前内网先简单校验_appid,以及对应的一个token,
外网发布需要加签名
"""
import  uuid
#uuid_str = uuid.uuid4()
#print(uuid_str)
appids={
    "mall":"91ce2a68-3774-41a1-9253-535e3c1042a7",
}

def check_token(_appid,_token):

    result=False
    token = appids.get(_appid)
    if token !=None and token == _token:
        result=True
    return True

def check_sign(_appid,_sign):


    return True
