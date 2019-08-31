# import datetime
# time = "2016-06-21T06:04:00Z"
# dt = datetime.datetime.timestamp(2016-06-21T06:04:00Z)
# print(dt)

import calendar, time
dt = calendar.timegm(time.strptime('2016-06-21T06:04:00Z', '%Y-%m-%dT%H:%M:%SZ'))
print(dt)

# calendar.timegm(time.strptime(df["time"][t], '%Y-%m-%dT%H:%M:%SZ'))