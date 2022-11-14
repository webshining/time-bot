from datetime import timedelta
from PIL import ImageDraw, ImageFont, Image

from .helper import DIR, get_current_time


W, H = (1000, 1000)
FONT_SIZE = 250

def generate_img():
    # get current time for text
    _time = get_current_time()
    text = f'{_time.strftime("%H")}:{_time.strftime("%M")}'
    
    # open image, convert to RGB and crop to W, H size
    img = Image.open(f'{DIR}/images/img.jpg').convert('RGB')
    w, h = img.size
    left, top = ((w - W) / 2, (h - H) / 2)
    img = img.crop((left, top, left+W, top+H))
    
    # add font to text and get it size
    font = ImageFont.truetype(f'{DIR}/fonts/RubikBurned-Regular.ttf', FONT_SIZE)
    w, h = font.getsize(text)
    
    # draw text
    draw = ImageDraw.Draw(img)
    draw.text(((W-w)/2, (H-h)/2), text, font=font, fill="#ffffff")
    
    # save image
    path = f'{DIR}/images/profile.jpg'
    img.save(path)
    
    # return path to img and sleep time
    return path, ((_time.replace(second=0, microsecond=0) + timedelta(minutes=1)) - _time).total_seconds()
    