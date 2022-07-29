import time
from pyrogram import Client
from decouple import config
from src.gen_img import img_generate

app = Client('time_bot', api_id=int(config('API_ID')), api_hash=config('API_HASH'))

with app:
    while True:
        # Get time to wait
        wait = img_generate()
        # Get profile photos
        photos = list(app.get_chat_photos('me'))
        photos_list = [p for p in photos]
        # Delete last and set profile photo
        app.set_profile_photo(photo='images/time.jpg')
        app.delete_profile_photos(photos_list[0].file_id)
        # Falling asleep until the next time change
        time.sleep(wait)
