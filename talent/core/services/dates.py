from datetime import date
from datetime import timedelta


def get_date_range_for_filtering(*, date_filter: str):
    today = date.today()
    yesterday = today - timedelta(days=1)

    if date_filter == "TODAY":
        return (today, today)
    if date_filter == "YESTERDAY":
        return (yesterday, yesterday)
    if date_filter == "LAST_7_DAYS":
        return (today - timedelta(days=7), today)
    if date_filter == "LAST_15_DAYS":
        return (today - timedelta(days=15), today)
    if date_filter == "LAST_30_DAYS":
        return (today - timedelta(days=30), today)
    if date_filter == "LAST_45_DAYS":
        return (today - timedelta(days=45), today)
    if date_filter == "LAST_90_DAYS":
        return (today - timedelta(days=90), today)

    raise ValueError(f"Invalid date filter {date_filter}")
