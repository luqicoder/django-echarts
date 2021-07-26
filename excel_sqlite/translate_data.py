# /usr/bin/env python
# coding=utf8

import json
import http.client  # 修改引用的模块
import hashlib  # 修改引用的模块
from urllib import parse
import random
import time
"""
from :zh
to: en
"""


def translate(word, from_lang, to_lang):
    appid = '20201224000654698'  # 你的appid
    secretKey = '8C0OoRSKe4UR5KMol933'  # 你的密钥

    httpClient = None
    myurl = '/api/trans/vip/translate'
    q = word
    salt = random.randint(32768, 65536)

    sign = appid + q + str(salt) + secretKey
    m1 = hashlib.md5()
    m1.update(sign.encode("utf-8"))
    sign = m1.hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + parse.quote(
        q) + '&from=' + from_lang + '&to=' + to_lang + '&salt=' + str(
        salt) + '&sign=' + sign

    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
        response = httpClient.getresponse()

        # 转码
        html = response.read().decode('utf-8')
        html = json.loads(html)
        dst = html["trans_result"][0]["dst"]
        return dst
    except Exception as e:
        print(e)
    finally:
        if httpClient:
            httpClient.close()
    time.sleep(30)
import pandas as pd
fd = pd.read_excel("C:\\Users\\wu411299174\\Desktop\\B学科人才(1).xlsx", sheet_name=5)
for i in range(0, fd.shape[0]):
    if isinstance(fd.values[i][0], str):
        print(translate(fd.values[i][1], "en", "zh"))
        time.sleep(1)
