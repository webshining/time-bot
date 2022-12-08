import io
import os
from PIL import ImageDraw, ImageFont, Image, ImageSequence

from .helper import DIR


def generate_img(text: str, image: str, save_name: str, font: str, font_size: int = 100, img_size: tuple[int] = (500, 500), fill: str = '#ffffff'):
    W, H = img_size
    img_format = image.split('.')[-1]
    img = Image.open(f'{DIR}/images/{image}')
    ft = ImageFont.truetype(f'{DIR}/fonts/{font}', font_size)
    w, h = ft.getsize(text)
    path = f'{DIR}/images/{save_name}'
    if img_format in ('jpg' or 'png'):
        img.convert('RGB')
        left = (img.size[0]-W)/2
        top = (img.size[1]-H)/2
        img.crop((left, top, left+W, top+H))
        d.text(((W-w)/2, (H-h)/2), text, font=ft, fill=fill)
        img.save(f'{path}.jpg')
        return f'{path}.jpg'
    elif img_format == 'gif':
        frames = []
        for frame in ImageSequence.Iterator(img):
            left = (img.size[0]-W)/2
            top = (img.size[1]-H)/2
            frame = frame.convert('RGB').crop((left, top, left+W, top+H))
            d = ImageDraw.Draw(frame)
            d.text(((W-w)/2, (H-h)/2), text, font=ft, fill=fill)
            del d
            
            b = io.BytesIO()
            frame.save(b, format='GIF')
            frame = Image.open(b)
            frames.append(frame)
        frames[0].save(f'{path}.gif', format='GIF', save_all=True, append_images=frames[1:], loop=0, duration=50, optimize=True, quality=95)
        os.system(f'ffmpeg -i {path}.gif {path}.mp4 -y')
        return f'{path}.mp4'
