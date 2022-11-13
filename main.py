import asyncio
from src.generate_img import generate_img
from pyrogram import Client


app = Client('timebot', 5041292, 'e145bc85c7335c989a7b3b35aed5ae83')

async def main():
    while True:
        path, time_to_sleep = generate_img()
        async with app:
            photos = [p async for p in app.get_chat_photos((await app.get_me()).id)]
            if photos:
                await app.delete_profile_photos(photos[0].file_id)
            await app.set_profile_photo(photo=path)
        await asyncio.sleep(time_to_sleep)
    

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    t1 = loop.create_task(main())
    loop.run_until_complete(t1)