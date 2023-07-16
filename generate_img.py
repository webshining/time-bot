import io
from datetime import datetime, timedelta

import imageio.v3 as iio
import pytz
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageSequence

from data.config import DIR


class Generate:
    def __init__(self, img: str, font: str, imgsize: int or list[int] = None, resize: int or list[int] = None, fontsize: int = None, fill: str = '#ffffff', brightness: float = None, text: str = None, timezone: str = None):
        self.isgif = img.split('.')[-1] == 'gif'
        self.img = Image.open(f"{DIR}/images/{img}")
        self.W, self.H = (imgsize[0], imgsize[1]) if isinstance(imgsize, tuple) else (imgsize, imgsize) if imgsize else (min(self.img.size), min(self.img.size))
        self.resize = resize if isinstance(resize, list) else (resize, resize) if resize else None
        self.fontsize = fontsize if fontsize else int(self.W/3-12)
        self.font = ImageFont.truetype(f'{DIR}/fonts/{font}', size=self.fontsize)
        self.fill = fill
        self.brightness = brightness
        self.path = f'{DIR}/images/out'
        self.timezone = pytz.timezone(timezone if timezone else 'Europe/Kyiv')
        self.text = text if text else self.current_time().strftime(f'%H:%M')
        
    def current_time(self) -> datetime:
        return datetime.now(self.timezone)
    
    def time_to_wait(self) -> timedelta.total_seconds:
        return (self.current_time().replace(second=0, microsecond=0)+timedelta(minutes=1)-self.current_time()).total_seconds()
    
    def crop_img(self, img: Image.Image):
        w, h = img.size
        left = (w - self.W)//2
        top = (h - self.H)//2
        return img.convert('RGB').crop((left, top, left+self.W, top+self.H))

    def darken_img(self, img: Image.Image, brightness: float = None):
        return ImageEnhance.Brightness(img).enhance(brightness) if brightness else img
    
    def get_avg_fps(self, img: Image.Image):
        img.seek(0)
        frames = duration = 0
        while True:
            try:
                frames += 1
                duration += img.info['duration']
                img.seek(img.tell() + 1)
            except EOFError:
                return frames / duration * 1000
        return None
    
    def generate_photo(self):
        img = self.darken_img(self.crop_img(self.img), self.brightness)
        draw = ImageDraw.Draw(img)
        _, _, w, h = draw.textbbox((0, 0), self.text, font=self.font)
        draw.text(((self.W-w)/2, (self.H-h)/2), self.text, self.fill, self.font)
        b = io.BytesIO()
        img.save(b, format='JPEG')
        return b
    
    def generate_video(self):
        frames = []
        for frame in ImageSequence.Iterator(self.img):
            frame = self.darken_img(self.crop_img(frame), self.brightness)
            draw = ImageDraw.Draw(frame)
            _, _, w, h = draw.textbbox((0, 0), self.text, font=self.font)
            draw.text(((self.W-w)/2, (self.H-h)/2), self.text, self.fill, self.font)
            del draw
            
            frames.append(frame.resize(self.resize) if self.resize else frame)
            
        iio.imwrite(f'{self.path}.mp4', frames, fps=self.get_avg_fps(self.img) or 25)
        return f'{self.path}.mp4'
        