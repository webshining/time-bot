import asyncio
from decouple import config
from pyrogram import Client

from src.generate_img import generate_img
from src.helper import get_current_time, time_to_next


app = Client('timebot', config('API_ID', cast=int), config('API_HASH', cast=str))


async def main():
    async with app:
        while True:
            text = get_current_time().strftime("%H:%M")
            path = generate_img(text=text, image='img.gif', font='RubikBurned-Regular.ttf', font_size=185, img_size=(750, 750), save_name='profile')
            photos = [p async for p in app.get_chat_photos((await app.get_me()).id)]
            if path.split('.')[-1] not in ('gif', 'mp4'):
                await app.set_profile_photo(photo=path)
            else: 
                await app.set_profile_photo(video=path)
            if photos:
                await app.delete_profile_photos(photos[0].file_id)
            await asyncio.sleep(time_to_next(get_current_time()).total_seconds())


if __name__ == '__main__':
    app.run(main())