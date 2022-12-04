from PIL import ImageDraw, ImageFont, Image
from decouple import config, Csv

from .helper import DIR


W, H = config('SIZE', cast=Csv(int), default=[1000, 1000])
FONT_SIZE = config('FONT_SIZE', cast=int, default=250)

def generate_img(text: str):
    # open image, convert to RGB and crop to W, H size
    img = Image.open(f'{DIR}/images/img.jpg').convert('RGB')
    w, h = img.size
    left, top = ((w - W) / 2, (h - H) / 2)
    img = img.crop((left, top, left+W, top+H))
    
    # add font to text and get it size
    font_rubik = ImageFont.truetype(f'{DIR}/fonts/RubikBurned-Regular.ttf', FONT_SIZE)
    w1, h1 = font_rubik.getsize(text)
    font_covered = ImageFont.truetype(f'{DIR}/fonts/CoveredByYourGrace-Regular.ttf', 50)
    w2, h2 = font_covered.getsize("How good when not negative good")
    
    
    # draw text
    draw = ImageDraw.Draw(img)
    draw.text(((W-w1)/2, (H-h1)/2), text, font=font_rubik, fill="#ffffff")
    draw.text(((W-w2-20), (H-h2-10)), text="How good when not negative good", font=font_covered, fill="#ffffff")
    
    # save image
    path = f'{DIR}/images/profile.jpg'
    img.save(path)
    
    # return path to img and sleep time
    return path
    