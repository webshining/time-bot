import io
from moviepy.editor import VideoFileClip
from PIL import ImageDraw, ImageFont, Image, ImageSequence

from .helper import DIR


def generate_img(text: str, image: str, save_name: str, font: str, font_size: int = 100, img_size: tuple[int] = (500, 500), fill: str = '#ffffff'):
    W, H = img_size
    img_format = image.split('.')[-1]
    img = Image.open(f'{DIR}/images/{image}')
    ft = ImageFont.truetype(f'{DIR}/fonts/{font}', font_size)
    w, h = ft.getsize(text)
    if img_format in ('jpg' or 'png'):
        img.convert('RGB')
        left = (img.size[0]-W)/2
        top = (img.size[1]-H)/2
        img.crop((left, top, left+W, top+H))
        d.text(((W-w)/2, (H-h)/2), text, font=ft, fill=fill)
        img.save(f'{DIR}/images/{save_name}.jpg')
        return f'{DIR}/images/{save_name}.jpg'
    elif img_format == 'gif':
        frames = []
        for frame in ImageSequence.Iterator(img):
            frame = frame.copy().convert('RGB')
            left = (img.size[0]-W)/2
            top = (img.size[1]-H)/2
            frame = frame.crop((left, top, left+W, top+H))
            d = ImageDraw.Draw(frame)
            d.text(((W-w)/2, (H-h)/2), text, font=ft, fill=fill)
            del d
            frames.append(frame)
        frames[0].save(f'{DIR}/images/{save_name}.mp4', format="GIF", save_all=True, append_images=frames[1:])
        VideoFileClip(f'{DIR}/images/{save_name}.mp4').write_videofile(f'{DIR}/images/{save_name}.mp4')
        return f'{DIR}/images/{save_name}.mp4'
