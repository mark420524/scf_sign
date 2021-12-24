# -*- coding: utf8 -*-
import time
import json
import requests

from func.iqiyi import IQY_sign
from func.tx import TX_sign
from func.mgtv import MG_sign
from func.wyy import WYY_sign
from func.ecloud import ECloud_sign
from func.wapj import PJ_sign
from func.ley import LY_sign
from func.bbs import JY_sign
from push.dingtalk import push_msg

def sendMsg(push_info, content):
    push_type = push_info['type']
    print(push_type)
    key_info = push_info[push_type]
    print(key_info)
    if push_type == "dingding":
        push_msg(key_info['access_token'], key_info['sign_secret'], content)
    elif push_type == "coolplus" :
        url = f"https://push.xuthus.cc/send/{key}"
        params = {
            "c": content
        }
        requests.get(url, params=params)


def iqy(P00001):
    '''爱奇艺引用'''
    # 签到
    obj = IQY_sign(P00001)
    msg1 = obj.sign()
    # 抽奖
    msg2 = []
    for i in range(3, 0, -1):
        ret = obj.draw(i)
        if ret["status"]:
            msg2.append(ret["msg"])
        else:
            break
    # 日常任务
    obj.queryTask().joinTask()
    msg3 = obj.queryTask().getReward()

    msg = f"{msg1}\n抽奖：{msg2}\n任务：{msg3}"
    return msg


def tx(cookies, params):
    '''腾讯视频引用'''
    obj = TX_sign(cookies, params)
    obj.auth_refresh()
    msg = f"用户：{obj.nickName}\n签到(1)：{obj.sign_once()}\n签到(2)：{obj.sign_twice()}"
    return msg


def mg(params):
    '''芒果tv引用'''
    obj = MG_sign(params)
    msg = obj.sign()
    return msg


def wyy(uin, pwd):
    '''网易云音乐引用'''
    obj = WYY_sign(uin, pwd)
    if obj.isLogin:
        msg = f'用户：{obj.nickname}\n签到：{obj.sign()}\n打卡：{obj.daka()}'
    else:
        msg = "登录失败，密码错误"
    return msg


def ecloud(user, pwd):
    '''天翼云盘引用'''
    obj = ECloud_sign(user, pwd)
    msg = obj.main()
    return msg

def pj(cookies):
    '''吾爱破解论坛引用'''
    obj = PJ_sign(cookies)
    msg = obj.sign()
    return msg

def ly(cookies):
    '''乐易论坛引用'''
    obj = LY_sign(cookies)
    msg = obj.sign()
    return msg


def jy(cookies):
    '''精易论坛引用'''
    obj = JY_sign(cookies)
    msg = obj.sign()
    return msg




def main_handler(event, context):
    with open("config.json", "r", encoding="utf-8") as f:
        data = json.loads(f.read())

    push_info = data["push"]
    # 爱奇艺
    msg_iqy = ""
    data_iqy = data["IQIYI"]
    if data_iqy["enable"]:
        for d in data_iqy["users"]:
            msg_iqy += iqy(d["P00001"])
    else:
        msg_iqy = "未开启"

    # 腾讯视频
    msg_tx = ""
    tx = data["TX"]
    if tx["enable"]:
        for d in tx["users"]:
            params = dict([p.split("=") for p in d["params"].split("&")])
            cookies = dict([c.split("=") for c in d["cookies"].split("; ")])
            msg_tx += tx(cookies, params)
    else:
        msg_tx = "未开启"

    # 芒果tv
    msg_mg = ""
    mg = data["MGO"]
    if mg["enable"]:
        for d in mg["users"]:
            params = dict([p.split("=") for p in d["params"].split("&")])
            msg_mg += mg(params)
    else:
        msg_mg = "未开启"

    # 天翼云盘
    msg_ec = ""
    ec = data["ECLOUD"]
    if ec["enable"]:
        for d in ec["users"]:
            msg_ec += ecloud(d["user"], d["pwd"])
    else:
        msg_ec = "未开启"

    # 吾爱论坛
    msg_52 = ""
    data_52 = data["52PJ"]
    if data_52["enable"]:
        for d in data_52["users"]:
            cookies = dict([c.split("=") for c in d["cookies"].split("; ")])
            msg_52 += pj(cookies)
    else:
        msg_52 = "未开启"

    # 乐易论坛
    msg_ly = ""
    ley = data["LEY"]
    if ley["enable"]:
        for d in ley["users"]:
            cookies = dict([c.split("=") for c in d["cookies"].split("; ")])
            msg_ly += ly(cookies)
    else:
        msg_ly = "未开启"

    # 精易论坛
    msg_jy = ""
    bbs = data["BBS"]
    if bbs["enable"]:
        for d in bbs["users"]:
            cookies = dict([c.split("=") for c in d["cookies"].split("; ")])
            msg_jy += jy(cookies)
    else:
        msg_jy = "未开启"

    # 网易云音乐
    msg_wyy = ""
    wyy = data["WYY"]
    if wyy["enable"]:
        for d in wyy["users"]:
            msg_wyy += wyy(d["uin"], d["pwd"])
    else:
        msg_wyy = "未开启"

    # 发送信息
    msg = f"【爱奇艺】\n{msg_iqy}\n\
【腾讯视频】\n{msg_tx}\n\
【芒果tv】\n{msg_mg}\n\
【天翼云盘】\n{msg_ec}\n\
【吾爱破解论坛】\n{msg_52}\n\
【乐易论坛】\n{msg_ly}\n\
【精易论坛】\n{msg_jy}\n\
【网易云】\n{msg_wyy}"
    sendMsg(push_info, msg)
    return msg

if __name__=="__main__":
    main_handler('','') 
    