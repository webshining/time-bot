from pathlib import Path

from decouple import config

DIR = Path(__file__).absolute().parents[1]

API_ID = config('API_ID', cast=int)
API_HASH = config('API_HASH', cast=str)
