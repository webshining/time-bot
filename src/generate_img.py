import io
import os
from datetime import datetime, timedelta

import pytz
from PIL import Image, ImageDraw, ImageFont, ImageSequence

from .helper import DIR


class Generate():
    def __init__(self, img: str, font: str, fontsize: int = 100, imgsize: int or tuple[int, int] = None, fill: str = '#ffffff'):
        self.img = Image.open(f"{DIR}/images/{img}")
        self.imgtype = img.split('.')[-1]
        self.font = ImageFont.truetype(f'{DIR}/fonts/{font}', size=fontsize)
        self.fill = fill
        self.path = f'{DIR}/images/out'
        self.W, self.H = (imgsize[0], imgsize[1]) if isinstance(imgsize, tuple) else (imgsize, imgsize) if imgsize else (min(self.img.size), min(self.img.size))
    
    def get_current_time(self):
        return datetime.now(pytz.timezone('Europe/Kyiv'))
    
    @property
    def time_to_wait(self):
        return (self.get_current_time().replace(second=0, microsecond=0)+timedelta(minutes=1)-self.get_current_time()).total_seconds()
    
    def generate_jpg(self):
        img = self.crop_img(self.img)
        text = self.get_current_time().strftime('%H:%M')
        draw = ImageDraw.Draw(img)
        w, h = self.font.getsize(text)
        draw.text(((self.W-w)/2, (self.H-h)/2), text, self.fill, self.font)
        b = io.BytesIO()
        img.save(b, format='JPEG')
        return b
    
    def generate_gif(self):
        frames = []
        text = self.get_current_time().strftime('%H:%M')
        for frame in ImageSequence.Iterator(self.img):
            frame = self.crop_img(frame)
            d = ImageDraw.Draw(frame)
            w, h = self.font.getsize(text)
            d.text(((self.W-w)/2, (self.H-h)/2), text, self.fill, self.font)
            del d
            
            frames.append(frame)
        frames[0].save(f'{self.path}.gif', format='GIF', save_all=True, append_images=frames[1:], loops=0)
        os.system(f'ffmpeg -i {self.path}.gif {self.path}.mp4 -loglevel error -y')
        return f'{self.path}.mp4'

    def crop_img(self, img: Image.Image):
        w, h = img.size
        left = (w - self.W)/2
        top = (h - self.H)/2
        return img.convert('RGB').crop((left, top, left+self.W, top+self.H))
        