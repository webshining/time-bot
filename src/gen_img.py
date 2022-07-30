from PIL import ImageDraw, Image, ImageFont
from datetime import datetime, timedelta
import pytz, pathlib

W, H = 1000, 1000


def img_generate():
    # Set timezone and generate time-text
    global name
    timezone = pytz.timezone('Europe/Kiev')
    time_now = datetime.now(timezone)
    start_minute = time_now.minute
    time_now = time_now.replace(minute=start_minute, second=0, microsecond=0)
    text = f'{time_now.hour:02}:{time_now.minute:02}'
    time_to_wait = (time_now + timedelta(minutes=1) - datetime.now(timezone)).total_seconds()

    # Open image
    if 4 < time_now.hour <= 9:
        name = 'evening'
    elif 9 < time_now.hour <= 17:
        name = 'day'
    elif 17 < time_now.hour <= 20:
        name = 'evening'
    elif time_now.hour >= 21 or time_now.hour <= 4:
        name = 'night'
    img = Image.open(f'{pathlib.Path(__file__).absolute().parent.parent}/images/{name}.jpg')
    img = img.convert('RGB')
    w, h = img.size

    # Crop img coords
    left = (w - W) / 2
    top = (h - H) / 2 + 200
    right = left + W
    buttom = top + H

    # Add text with custom font to the# image
    img = img.crop((left, top, right, buttom))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("fonts/Courgette-Regular.ttf", 250)
    w, h = draw.textsize(text, font=font)
    draw.text(((W - w) / 2, 20), text, font=font, fill="#fff")

    # Save image to images folder
    img.save(f'{pathlib.Path(__file__).absolute().parent.parent}/images/time.jpg', quality=90, optimize=True)

    # Return waiting time until next generation
    return time_to_wait
