import io
import os
from datetime import datetime, timedelta

from PIL import Image, ImageDraw, ImageFont, ImageSequence

from data.config import DIR, TIMEZONE


class Generate():
    def __init__(self, img: str, font: str, fontsize: int = None, imgsize: int or tuple[int, int] = None, fill: str = '#ffffff', text: str = None):
        self.imgtype = img.split('.')[-1]
        self.img = Image.open(f"{DIR}/images/{img}")
        self.W, self.H = (imgsize[0], imgsize[1]) if isinstance(imgsize, tuple) else (imgsize, imgsize) if imgsize else (min(self.img.size), min(self.img.size))
        if not fontsize:
            fontsize = int(self.W/3-12)
        self.font = ImageFont.truetype(f'{DIR}/fonts/{font}', size=fontsize)
        self.fill = fill
        self.text = text if text else self.current_time.strftime('%H:%M')
        self.path = f'{DIR}/images/out'
    
    @property
    def current_time(self) -> datetime:
        return datetime.now(TIMEZONE)
    
    @property
    def time_to_wait(self) -> timedelta.total_seconds:
        return (self.current_time.replace(second=0, microsecond=0)+timedelta(minutes=1)-self.current_time).total_seconds()
    
    def generate_jpg(self):
        img = self.crop_img(self.img)
        draw = ImageDraw.Draw(img)
        _, _, w, h = draw.textbbox((0, 0), self.text, font=self.font)
        draw.text(((self.W-w)/2, (self.H-h)/2), self.text, self.fill, self.font)
        b = io.BytesIO()
        img.save(b, format='JPEG')
        return b
    
    def generate_gif(self):
        frames = []
        for frame in ImageSequence.Iterator(self.img):
            frame = self.crop_img(frame)
            draw = ImageDraw.Draw(frame)
            _, _, w, h = draw.textbbox((0, 0), self.text, font=self.font)
            draw.text(((self.W-w)/2, (self.H-h)/2), self.text, self.fill, self.font)
            del draw
            
            frames.append(frame)
        frames[0].save(f'{self.path}.gif', format='GIF', save_all=True, append_images=frames[1:], loops=0)
        os.system(f'ffmpeg -i {self.path}.gif {self.path}.mp4 -loglevel error -y')
        return f'{self.path}.mp4'

    def crop_img(self, img: Image.Image):
        w, h = img.size
        left = (w - self.W)/2
        top = (h - self.H)/2
        return img.convert('RGB').crop((left, top, left+self.W, top+self.H))
        