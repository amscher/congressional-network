import time
from calendar import monthrange
from datetime import datetime, timedelta

def now():
  return datetime.now()

def get(str):
  str = str[:10]
  time_struct = time.strptime(str, "%Y-%m-%d")
  dt = datetime.fromtimestamp(time.mktime(time_struct))
  return dt

def monthdelta(d1, d2):
  delta = 0
  while True:
    mdays = monthrange(d1.year, d1.month)[1]
    d1 += timedelta(days=mdays)
    if d1 <= d2:
        delta += 1
    else:
        break
  return delta