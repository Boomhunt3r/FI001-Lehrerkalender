import calendar
import time
from datetime import datetime

def get_time():
    current_gmt = time.gmtime()
    timestamp = calendar.timegm(current_gmt)
    return timestamp

def convert_to_date(timestamp):
    date_time = datetime.fromtimestamp(timestamp)
    return date_time