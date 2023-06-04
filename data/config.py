from pathlib import Path

import pytz
from decouple import config

DIR = Path(__file__).absolute().parents[1]

TIMEZONE = pytz.timezone(config('TIMEZONE', cast=str, default='Europe/Kyiv'))

API_ID = config('API_ID', cast=int)
API_HASH = config('API_HASH', cast=str)
