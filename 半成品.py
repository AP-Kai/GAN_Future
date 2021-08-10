# 2021.8.10更新
# -*- coding: utf-8 -*-
import os
os.environ['WECHATY_PUPPET']="wechaty-puppet-service"
os.environ['WECHATY_PUPPET_SERVICE_TOKEN']="puppet_padlocal_a48ae36edb074414a1db144d401ee05" # 这里填Wechaty token
os.environ['CUDA_VISIBLE_DEVICES']="0"
# os.environ['WECHATY_PUPPET_SERVICE_ENDPOINT']="127.0.0.1:8080" #这里填Wechaty服务端的IP和端口
# os.system("pip install wechaty==0.7dev17")
# os.system("hub install deeplabv3p_xception65_humanseg") #安装已保存的模型
import asyncio
import paddlehub as hub
import cv2
import json
from pachong import download_image
import tianxingapi
import xiaogongneng
from wechaty import (
    Contact,
    FileBox,
    Message,
    Wechaty,
    ScanStatus,
)


async def on_message(msg: Message):

    talker = msg.talker()
    room = msg.room()
    print(room)
    try:
        if msg.text() == 'ding':
            await msg.say('这是自动回复: dong dong dong')

        if msg.text() == 'hi' or msg.text() == '你好':
            await msg.say('这是自动回复: 机器人目前的功能是\n- 收到"ding", 自动回复"dong dong dong"\n- 收到"图片", 自动回复一张图片\n- 收到“搜图 XX”,搜索相关图片\n- 收到“查天气 xx”,查询xx地天气情况\n- 收到“来一份涩图”，可获得一张涩图\n'
                          '- 收到"彩虹屁"，自动回复花式彩虹屁\n- 收到"舔狗"，自动回复花式舔狗日记\n- 收到"毒鸡汤"，自动回复花式毒鸡汤\n- 收到“互删句子”，自动回复互删句子\n- 收到“网易云”，自动回复热评\n- 收到“朋友圈文案”，自动回复最佳文案\n')

        if msg.text() == '图片':
            url = 'https://images.unsplash.com/photo-1470770903676-69b98201ea1c?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1500&q=80'

            # 构建一个FileBox
            file_box_1 = FileBox.from_url(url=url, name='xx.jpg')
            await msg.say(file_box_1)
        if msg.text() == '来一份涩图':
            img = str(xiaogongneng.setu())
            file_box_3 = FileBox.from_file(img, name=img.split('/')[-1])
            await msg.say(file_box_3)
        if msg.text() == '彩虹屁':
            await msg.say(tianxingapi.caihongpi())
        if msg.text() == '舔狗':
            await msg.say(tianxingapi.tiangouriji())
        if msg.text() == '毒鸡汤':
            await msg.say(tianxingapi.dujitang())
        if msg.text() == '互删句子':
            await msg.say(tianxingapi.hushanjuzi())
        if msg.text() == '网易云':
            await msg.say(tianxingapi.wangyiyun())
        if msg.text() == '朋友圈文案':
            await msg.say(tianxingapi.pyq())

        if msg.text().split(' ', 1)[0] == '查天气':
            key = str(msg.text().split(' ')[1])
            weather = xiaogongneng.getweather(key)
            await msg.say(weather)
        if msg.text().split()[1] == '拍了拍我':
            await msg.say('别拍了,再拍要坏掉了')

        if msg.text().split(' ', 1)[0] == '搜图':
            key = str(msg.text().split(' ')[1])
            #await msg.say('正在查找'+ key)

            url1 = download_image(key)
            #await msg.say(url1[0])
            #print(url1)
            # 构建一个FileBox
            file_box_2 = FileBox.from_url(url=url1, name='xx.jpg')
            await msg.say(file_box_2)

        '''
        if msg.type() == Message.Type.MESSAGE_TYPE_IMAGE:
            await talker.say('已收到图像，开始验证')
            # 将Message转换为FileBox
            file_box_user_image = await msg.to_file_box()
            # 获取图片名
            img_name = file_box_user_image.name
            # 图片保存的路径
            img_path = './image/' + img_name
            # 将图片保存为本地文件
            await file_box_user_image.to_file(file_path=img_path)
    
            human_seg = hub.Module(name="deeplabv3p_xception65_humanseg")
            result = human_seg.segmentation(images=[cv2.imread('./image/'+img_name)],
                                            use_gpu=True,
                                            visualization=True,
                                            output_dir='./image/output')
            file_box_final_result = FileBox.from_file(result)
            await msg.say(file_box_final_result)
            await msg.say('验证完毕')
        '''

    except Exception as e:
        print('出现了错误,错误情况%s' % e)
        #await msg.say("千冬出现了未知错误！请联系管理员进行处理")


async def on_scan(
        qrcode: str,
        status: ScanStatus,
        _data,
):
    print('Status: ' + str(status))
    print('View QR Code Online: https://wechaty.js.org/qrcode/' + qrcode)


async def on_login(user: Contact):
    print(user)


async def main():
    # 确保我们在环境变量中设置了WECHATY_PUPPET_SERVICE_TOKEN
    if 'WECHATY_PUPPET_SERVICE_TOKEN' not in os.environ:
        print('''
            Error: WECHATY_PUPPET_SERVICE_TOKEN is not found in the environment variables
            You need a TOKEN to run the Python Wechaty. Please goto our README for details
            https://github.com/wechaty/python-wechaty-getting-started/#wechaty_puppet_service_token
        ''')

    bot = Wechaty()

    bot.on('scan', on_scan)
    bot.on('login', on_login)
    bot.on('message', on_message)

    await bot.start()

    print('[Python Wechaty] Ding Dong Bot started.')


asyncio.run(main())
