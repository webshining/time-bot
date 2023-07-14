import io
from datetime import datetime, timedelta

import moviepy.editor as mp
import pytz
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageSequence

from data.config import DIR


class Generate:
    def __init__(self, img: str, font: str, imgsize: str or list[str] = None, fontsize: int = None, fill: str = '#ffffff', brightness: float = None, text: str = None, timezone: str = None):
        self.isgif = img.split('.')[-1] == 'gif'
        self.img = Image.open(f"{DIR}/images/{img}")
        self.W, self.H = (imgsize[0], imgsize[1]) if isinstance(imgsize, tuple) else (imgsize, imgsize) if imgsize else (min(self.img.size), min(self.img.size))
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
    
    def crop_img(self, img: Image.Image = None):
        w, h = img.size
        left = (w - self.W)//2
        top = (h - self.H)//2
        return img.convert('RGBA').crop((left, top, left+self.W, top+self.H))

    def darken_img(self, img: Image.Image = None, brightness: float = None):
        return ImageEnhance.Brightness(img).enhance(brightness) if brightness else img
    
    def generate_jpg(self):
        img = self.darken_img(self.crop_img(self.img), self.brightness)
        draw = ImageDraw.Draw(img)
        _, _, w, h = draw.textbbox((0, 0), self.text, font=self.font)
        draw.text(((self.W-w)/2, (self.H-h)/2), self.text, self.fill, self.font)
        b = io.BytesIO()
        img.save(b, format='PNG')
        return b
    
    def generate_gif(self):
        frames = []
        for frame in ImageSequence.Iterator(self.img):
            frame = self.darken_img(self.crop_img(frame), self.brightness)
            draw = ImageDraw.Draw(frame)
            _, _, w, h = draw.textbbox((0, 0), self.text, font=self.font)
            draw.text(((self.W-w)/2, (self.H-h)/2), self.text, self.fill, self.font)
            del draw
            
            frames.append(frame.resize((720,720)) if frame.size[1] > 720 else frame)
        frames[0].save(f'{self.path}.gif', format='GIF', save_all=True, append_images=frames[1:], loops=0)
        
        clip = mp.VideoFileClip(f"{self.path}.gif")
        clip.write_videofile(f"{self.path}.mp4", logger=None)
        return f'{self.path}.mp4'
        