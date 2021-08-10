# 2021.8.10更新
import json
import urllib.request
# 彩虹屁
def caihongpi():
    APIKEY = '44cbe797722bc0a82e0148ed06c06c23'
    url = 'http://api.tianapi.com/txapi/caihongpi/index?key=' + APIKEY

    req = urllib.request.Request(url)

    resp = urllib.request.urlopen(req)
    content = json.loads(resp.read())
    print(content)
    if (content):
        return content['newslist'][0]['content']
    else:
        return '你的机器人离岗了'


# 舔狗日记
def tiangouriji():
    APIKEY = '44cbe797722bc0a82e0148ed06c06c23'
    url = 'http://api.tianapi.com/txapi/tiangou/index?key=' + APIKEY

    req = urllib.request.Request(url)

    resp = urllib.request.urlopen(req)
    content = json.loads(resp.read())
    print(content)
    if (content):
        return content['newslist'][0]['content']
    else:
        return '你的机器人离岗了'


# 毒鸡汤
def dujitang():
    APIKEY = '44cbe797722bc0a82e0148ed06c06c23'
    url = 'http://api.tianapi.com/txapi/dujitang/index?key=' + APIKEY

    req = urllib.request.Request(url)

    resp = urllib.request.urlopen(req)
    content = json.loads(resp.read())
    print(content)
    if (content):
        return content['newslist'][0]['content']
    else:
        return '你的机器人离岗了'
# 互删句子
def hushanjuzi():
    APIKEY = '44cbe797722bc0a82e0148ed06c06c23'
    url = 'http://api.tianapi.com/txapi/hsjz/index?key=' + APIKEY

    req = urllib.request.Request(url)

    resp = urllib.request.urlopen(req)
    content = json.loads(resp.read())
    print(content)
    if (content):
        return content['newslist'][0]['content']
    else:
        return '你的机器人离岗了'
# 网易云
def wangyiyun():
    APIKEY = '44cbe797722bc0a82e0148ed06c06c23'
    url = 'http://api.tianapi.com/txapi/hotreview/index?key=' + APIKEY

    req = urllib.request.Request(url)

    resp = urllib.request.urlopen(req)
    content = json.loads(resp.read())
    print(content)
    if (content):
        return content['newslist'][0]['content']
    else:
        return '你的机器人离岗了'
# 朋友圈
def pyq():
    APIKEY = '44cbe797722bc0a82e0148ed06c06c23'
    url = 'http://api.tianapi.com/txapi/pyqwenan/index?key=' + APIKEY

    req = urllib.request.Request(url)

    resp = urllib.request.urlopen(req)
    content = json.loads(resp.read())
    print(content)
    if (content):
        return content['newslist'][0]['content']
    else:
        return '你的机器人离岗了'
