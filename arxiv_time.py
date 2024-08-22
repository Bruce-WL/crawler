from datetime import UTC, datetime, timedelta
from tzlocal import get_localzone
from functools import lru_cache

HOLIDAY_2024 = [
    "2024 15 January",
    "2024 22 May",
    "2024 19 June",
    "2024 4 July",
    "2024 2 September",
    "2024 28 November",
    "2024 25 December",
    "2024 26 December",
    "2024 31 December",
]
HOLIDAY_2024_date = [datetime.strptime(d, "%Y %d %B") for d in HOLIDAY_2024]


def native_local_to_utc(naive_time: datetime):
    return naive_time.replace(tzinfo=get_localzone()).astimezone(UTC)

@lru_cache()
def next_arxiv_update_day(time: datetime):
    # see https://info.arxiv.org/help/availability.html
    # arxiv update time is UTC+0 00:00:00

    time.astimezone(UTC)
    time_date = time.replace(hour=0, minute=0, second=0, microsecond=0)
    if time > time_date:
        time = time_date + timedelta(days=1)


    while time.date() in HOLIDAY_2024_date or time.weekday() in [5, 6]:
        time = time + timedelta(days=1)
    return time

