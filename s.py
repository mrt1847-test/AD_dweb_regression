
from datetime import datetime, timedelta

time1 = "2025-09-25 14:00:01"
time2 = "2025-09-25 14:00:00"

dt1 = datetime.strptime(time1, "%Y-%m-%d %H:%M:%S")
dt2 = datetime.strptime(time2, "%Y-%m-%d %H:%M:%S")
n_dt2 = dt2 + timedelta(seconds=2)
print(dt1)
print(dt2)
print(n_dt2)

assert dt1 < n_dt2