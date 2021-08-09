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


from wechaty import (
    Contact,
    FileBox,
    Message,
    Wechaty,
    ScanStatus,
)

async def on_message(msg: Message):
    talker = msg.talker()
    if msg.text() == 'ding':
        await msg.say('这是自动回复: dong dong dong')

    if msg.text() == 'hi' or msg.text() == '你好':
        await msg.say('这是自动回复: 机器人目前的功能是\n- 收到"ding", 自动回复"dong dong dong"\n- 收到"图片", 自动回复一张图片')

    if msg.text() == '图片':
        url = 'https://images.unsplash.com/photo-1470770903676-69b98201ea1c?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1500&q=80'

        # 构建一个FileBox
        file_box_1 = FileBox.from_url(url=url, name='xx.jpg')

        await msg.say(file_box_1)

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

    bot.on('scan',      on_scan)
    bot.on('login',     on_login)
    bot.on('message',   on_message)

    await bot.start()

    print('[Python Wechaty] Ding Dong Bot started.')


asyncio.run(main())