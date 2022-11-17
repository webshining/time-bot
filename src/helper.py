import pytz
from pathlib import Path
from datetime import datetime, timedelta


DIR = Path(__file__).absolute().parent


def get_current_time(timezone: str = 'Europe/Kyiv'):
    tz = pytz.timezone(timezone)
    return datetime.now(tz)


def time_to_next(current_time: datetime):
    return current_time.replace(second=0, microsecond=0) + timedelta(minutes=1) - current_time
