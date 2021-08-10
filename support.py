import re
import requests
import random


def getweather(location):
    path = "https://free-api.heweather.net/s6/weather?location=%s&key=a3269a0918a44a62ae97c314dd24f02a"
    url = path % location
    print(url)
    res = requests.get(url)

    result = res.json()
    weather = ""
    # print(result)

    if result['HeWeather6'][0]['status'] == 'ok':
        r1 = result['HeWeather6'][0]
        # print(r1)
        s0 = r1["basic"]["parent_city"]
        if s0 != location:
            s0 = location + " 坐标城市:%s\n" % s0
        today = r1['now']
        s1 = '天气：%s\n' % today['cond_txt']

        s2 = "当前：%s℃  本日:%s~%s℃\n" % (
            today['tmp'], r1['daily_forecast'][0]['tmp_min'], r1['daily_forecast'][0]['tmp_max'])
        s3 = "风向：%s\n" % today['wind_dir']
        pm25 = int(today['hum'])
        pollution = ''
        if 0 <= pm25 < 35:
            pollution = '优'
        elif 35 <= pm25 < 75:
            pollution = '良'
        elif 75 <= pm25 < 115:
            pollution = '轻度污染'
        elif 115 <= pm25 < 150:
            pollution = '中度污染'
        elif 150 <= pm25 < 250:
            pollution = '重度污染'
        elif pm25 >= 250:
            pollution = '严重污染'
        s4 = "pm25:%s 空气质量:%s\n" % (pm25, pollution)
        lifetip = r1["lifestyle"]
        s5 = "紫外线:"
        s6 = "生活小贴士：\n"
        count = 1
        for i in lifetip:
            if i['type'] not in ['sport', 'uv', 'comf', 'flu']:
                s6 += str(count) + ':' + i['txt'] + '\n'
                count += 1
            elif i['type'] == 'uv':
                s5 += i['txt'] + '\n'
        weather = s0 + s1 + s2 + s3 + s4 + s5 + s6
        print(weather)
    else:
        print("没查到这个地区的天气信息，请检查地区名是否输入规范")
        weather = "没查到这个地区的天气信息，请检查地区名是否输入规范"
    return weather


HEADERS = {
    'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
    'Accept - Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.5',
    'Connection': 'Keep-Alive',
    'Host': 'image.baidu.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'
}


def download_image(key_word, headers=HEADERS):
    download_index = 0
    str_gsm = '00'


    str_pn = str(download_index)

    # 定义百度图片的搜索URL
    url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=%s&pn=%s&gsm=%s&ct=&ic=0&lm=-1&width=0&height=0' % (
        key_word, str_pn, str_gsm
        )

    # 获取当前页面的源码
    result = requests.get(url, timeout=10, headers=headers).text  # timeout请求超时时间单位为秒
    # 获取当前页面的图片URL
    img_urls = re.findall('"objURL":"(.*?)",', result, re.S)  # 匹配字符串，以列表的形式返回匹配到的字符 re.S参数将这个字符串作为一个整体
    i = len(img_urls)
    flag = random.randint(0, i)

    return (img_urls[flag])


