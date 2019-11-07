"""
Helper functions which can be called from any other layer. (but mainly from the business logic layer)
"""

import time
from datetime import datetime
import data_handler



def pretty_datetime_for_ui(dt):
    timestamp = (dt - datetime(1970, 1, 1)).total_seconds()
    old_time = dt
    current_time = datetime.now()
    time_delta = current_time - old_time
    total_minutes = (time_delta.total_seconds() // 60)
    total_hours = total_minutes // 60
    total_days = total_hours // 24

    if time_delta.total_seconds() < 60:
        return 'Few seconds ago'
    elif (time_delta.total_seconds() / 60) < 2:
        return '1 minute ago'
    elif total_hours < 1:
        return f'{int(total_minutes)} minutes ago'
    elif total_days < 1:
        return f'{int(total_hours)} hour ago'
    else:
        return time.strftime("%Y %m/%d %H:%M", time.localtime(timestamp))


def __preformat_for_sort(data):
    if isinstance(data, str):
        return data.lower()
    else:
        return data
