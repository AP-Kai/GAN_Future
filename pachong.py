# 2021.8.10
import re
import requests
import random

# 从edge浏览器获得的访问image.baidu.com时的header，可以让网站认为是用户通过浏览器在访问
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

def main():
    # 最大图片下载数量

    max_failure = 10
    # 输入想搜索的图片的名字
    key_word = str(input('输入想搜索的图片名称: '))
    # 输入想搜索的最大图片个数
    max_download = int(input('输入想搜索的图片个数: '))
    # 使用明星的名字开始下载图片
    download_image(key_word, max_download, max_failure)
    print('全部图片已下载完成')


if __name__ == '__main__':
    url = download_image('苹果')
    print(str(url[0]))
