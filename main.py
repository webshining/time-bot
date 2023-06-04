import asyncio

from pyrogram import Client

from data.config import API_HASH, API_ID
from generate_img import Generate

app = Client('data/timebot', api_id=API_ID, api_hash=API_HASH)

async def main():
    async with app:
        while True:
            generate = Generate(img='img.png', font='font.ttf')
            photos = [i.file_id for i in await app.get_profile_photos("me") if hasattr(i, 'file_id')]
            if generate.imgtype == 'gif':
                await app.set_profile_photo(video=generate.generate_gif())
            else:
                await app.set_profile_photo(photo=generate.generate_jpg())
            if photos:
                await app.delete_profile_photos(photos[0])
            await asyncio.sleep(generate.time_to_wait)

if __name__ == '__main__':
    app.run(main())
