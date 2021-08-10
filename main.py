# -*- coding: utf-8 -*-
import os
import subprocess
import asyncio
from wechaty import (
    Contact,
    FileBox,
    Message,
    Wechaty,
    ScanStatus,
)
os.environ['WECHATY_PUPPET']="wechaty-puppet-service"
os.environ['WECHATY_PUPPET_SERVICE_TOKEN']="puppet_padlocal_a48ae36edb074414a1db144d401ee05" # 这里填Wechaty token
os.environ['CUDA_VISIBLE_DEVICES']="0"


async def on_message(msg: Message):
    global mix_flag
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

    if msg.text() == '融合':
        mix_flag = 1
        if os.path.exists('image/first_image.png'):
            os.remove('image/first_image.png')
        if os.path.exists('image/second_image.png'):
            os.remove('image/second_image.png')
        await msg.say('please send the first image')

    if mix_flag == 1 and msg.type() == Message.Type.MESSAGE_TYPE_IMAGE:
        mix_flag = 2
        # 将Message转换为FileBox
        file_box_user_image = await msg.to_file_box()
        # 获取图片名
        # img_name = file_box_user_image.name
        # 图片保存的路径
        img_path = './image/' + 'first_image.png'
        # 将图片保存为本地文件
        await file_box_user_image.to_file(file_path=img_path)
        cmd = "python -u D:/Path/PaddleGAN/applications/tools/styleganv2fitting.py \
           --input_image image/first_image.png\
           --need_align \
           --start_lr 0.1 \
           --final_lr 0.025 \
           --latent_level 0 1 2 3 4 5 6 7 8 9 10 11 \
           --step 100 \
           --mse_weight 1 \
           --output_path output/1 \
           --model_type ffhq-config-f \
           --size 1024 \
           --style_dim 512 \
           --n_mlp 8 \
           --channel_multiplier 2"
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        out, err = p.communicate()
        result = out.split('\n'.encode())
        for lin in result:
            if not lin.startswith('#'.encode()):
                print(lin)
        await msg.say('please send the second image')

    if mix_flag == 2 and msg.type() == Message.Type.MESSAGE_TYPE_IMAGE:
        mix_flag = 3
        # 将Message转换为FileBox
        file_box_user_image = await msg.to_file_box()
        # 获取图片名
        # img_name = file_box_user_image.name
        # 图片保存的路径
        img_path = './image/' + 'second_image.png'
        # 将图片保存为本地文件
        await file_box_user_image.to_file(file_path=img_path)

        cmd = "python -u D:/Path/PaddleGAN/applications/tools/styleganv2fitting.py \
           --input_image image/second_image.png\
           --need_align \
           --start_lr 0.1 \
           --final_lr 0.025 \
           --latent_level 0 1 2 3 4 5 6 7 8 9 10 11 \
           --step 100 \
           --mse_weight 1 \
           --output_path output/2 \
           --model_type ffhq-config-f \
           --size 1024 \
           --style_dim 512 \
           --n_mlp 8 \
           --channel_multiplier 2"

        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        out, err = p.communicate()
        result = out.split('\n'.encode())
        for lin in result:
            if not lin.startswith('#'.encode()):
                print(lin)
        await msg.say("Nice!Let's wait a minite for a mixed image")

    if mix_flag == 3 and os.path.exists('output'):
        mix_flag = 4
        cmd = "python -u D:/Path/PaddleGAN/applications/tools/styleganv2mixing.py \
           --latent1 output/1/dst.fitting.npy \
           --latent2 output/2/dst.fitting.npy \
           --weights \
                     0.5 0.5 0.5 0.5 0.5 0.5 \
                     0.5 0.5 0.5 0.5 0.5 0.5 \
                     0.5 0.5 0.5 0.5 0.5 0.5 \
           --output_path mixoutput/ \
           --model_type ffhq-config-f \
           --size 1024 \
           --style_dim 512 \
           --n_mlp 8 \
           --channel_multiplier 2 "

        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        out, err = p.communicate()
        result = out.split('\n'.encode())
        for lin in result:
            if not lin.startswith('#'.encode()):
                print(lin)
        await msg.say('it will come soon!')

    if mix_flag == 4:
        mix_flag = 0
        file_box = FileBox.from_file('mixoutput/dst.mixing.png')
        await msg.say(file_box)

    '''if msg.type() == Message.Type.MESSAGE_TYPE_IMAGE:
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
        await msg.say('验证完毕')'''

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