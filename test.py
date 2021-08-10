import subprocess


def gan1():
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
    result = out.split('/n'.encode())
    for lin in result:
        if not lin.startswith('#'.encode()):
            print(lin)


gan1()