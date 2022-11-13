import pytz
from pathlib import Path
from datetime import datetime


DIR = Path(__file__).absolute().parent


def get_current_time(timezone: str = 'Europe/Kyiv'):
    tz = pytz.timezone(timezone)
    return datetime.now(tz)
