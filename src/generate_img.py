import io
from PIL import ImageDraw, ImageFont, Image, ImageSequence

from .helper import DIR


def generate_img(text: str, image: str, font: str, font_size: int, img_size: tuple[int], save: str):
    W, H = img_size
    gif = image.split('.')[-1] == 'gif'
    
    # open image
    img = Image.open(f'{DIR}/images/{image}')
    if not gif:
        img.convert('RGB')
        left, top = ((img.size[0] - W) / 2, (img.size[1] - H) / 2)
        img = img.crop((left, top, left+W, top+H))
    
    # add font to text and get it size
    font = ImageFont.truetype(f'{DIR}/fonts/{font}', font_size)
    w, h = font.getsize(text)
    
    # draw text
    if not gif:
        draw = ImageDraw.Draw(img)
        draw.text(((W-w)/2, (H-h)/2), text, font=font, fill="#ffffff")
    else:
        frames = []
        for frame in ImageSequence.Iterator(img):
            draw = ImageDraw.Draw(frame)
            draw.text(((W-w)/2, (H-h)/2), text, font=font, fill="#ffffff")
            del draw
            b = io.BytesIO()
            frame.save(b, format="GIF")
            frame = Image.open(b)
            frames.append(frame)
    
    # save image
    path = f'{DIR}/images/{save}'
    img.save(path) if not gif else frames[0].save(path, save_all=True, append_images=frames[1:])
    
    # return path to img
    return path
