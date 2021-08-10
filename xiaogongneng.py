# 2021.8.10更新
from urllib import request
import requests
import os
import json
import random
def getweather(location):
    path = "https://api.seniverse.com/v3/weather/now.json?key=Skb40T46PiBDM35V2&location=%s&language=zh-Hans&unit=c"
    path2 = "https://free-api.heweather.net/s6/weather?location=%s&key=a3269a0918a44a62ae97c314dd24f02a"
    url = path2 % location
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


stars = []


def creatsetulist():
    setulist = os.listdir(r'C:\Users\nian\Downloads\Illustration')
    for list in setulist:
        star = {}
        print(list)
        star['local'] = (r'C:\Users\nian\Downloads\Illustration\\' + list)
        stars.append(star)
    #print(stars)
    json_data = json.dumps(stars, ensure_ascii=False)
    #print(json_data)
    f = open('image.json', 'w', encoding='utf-8')
    f.write(json_data)
    f.close()

def catch_value(file_name, value, position):
    """提取所需元素的方法"""
    f = open(file_name, encoding='utf-8')
    setting = json.load(f)  # 把json文件转化为python用的类型
    f.close()
    my_value = setting[position][value]  # 提取元素中所需要的的值
    return my_value

def setu():
    i = random.randint(0,1000)
    img = catch_value('image.json', 'local', i)
    return img

if __name__ == '__main__':
    creatsetulist()
