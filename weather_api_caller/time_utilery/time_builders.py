from datetime import datetime, timedelta

time_format = '%Y-%m-%d %H:%M'


def convert_to_date_time(formatted_time: str):
    return datetime.strptime(formatted_time, time_format)


def get_today() -> datetime:
    date = datetime.today().strftime(time_format)
    return convert_to_date_time(date)


def get_tomorrow(date: datetime = get_today()):
    one_day = timedelta(days=1)
    return date + one_day


def get_yesterday(date: datetime = get_today()):
    one_day = timedelta(days=1)
    return date - one_day


def convert_to_local(localtime_epoch):
    utc_datetime = datetime.fromtimestamp(localtime_epoch).strftime(time_format)
    return convert_to_date_time(utc_datetime)
