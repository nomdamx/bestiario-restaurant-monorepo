from datetime import datetime,timedelta
from math import floor
from zoneinfo import ZoneInfo

def create_timestampt():
    time = datetime.now() + timedelta(days=30)
    return floor(time.timestamp())


MX_TZ = ZoneInfo("America/Mexico_City")

def get_operational_date(now: datetime | None = None):
    now = now or datetime.now(tz=MX_TZ)

    if now.hour < 6:
        return (now - timedelta(days=1)).date()

    return now.date()