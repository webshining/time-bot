import asyncio
from decouple import config
from pyrogram import Client

from src.generate_img import generate_img


app = Client('timebot', config('API_ID', cast=int), config('API_HASH', cast=str))


async def main():
    async with app:
        while True:
            path, time_to_sleep = generate_img()
            photos = [p async for p in app.get_chat_photos((await app.get_me()).id)]
            if photos:
                await app.delete_profile_photos(photos[0].file_id)
            await app.set_profile_photo(photo=path)
            await asyncio.sleep(time_to_sleep)


if __name__ == '__main__':
    app.run(main())