import asyncio

from decouple import config
from pyrogram import Client

from src.generate_img import Generate

app = Client('timebot', config('API_ID', cast=int), config('API_HASH', cast=str))


async def main():
    async with app:
        while True:
            generate = Generate('img.jpg', 'CabinSketch-Bold.ttf', 145)
            photos = [i.file_id async for i in app.get_chat_photos((await app.get_me()).id)]
            if generate.imgtype == 'gif':
                await app.set_profile_photo(video=generate.generate_gif())
            else:
                await app.set_profile_photo(photo=generate.generate_jpg())
            if photos:
                await app.delete_profile_photos(photos[0])
            await asyncio.sleep(generate.time_to_wait)

if __name__ == '__main__':
    app.run(main())