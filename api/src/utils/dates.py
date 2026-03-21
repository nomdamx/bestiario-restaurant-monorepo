from datetime import UTC, date, datetime, timedelta, timezone
from math import floor
from zoneinfo import ZoneInfo


def create_timestampt():
    time = date_now() + timedelta(days=30)
    return floor(time.timestamp())


def date_now():
    return datetime.now(UTC)


MX_TZ = ZoneInfo("America/Mexico_City")


def get_operational_date(now: datetime | None = None) -> date:
    now = now or datetime.now(tz=MX_TZ)

    if now.hour < 6:
        return (now - timedelta(days=1)).date()

    return now.date()
