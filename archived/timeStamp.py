import pandas as pd
import calendar, time
# import csv
df = pd.read_csv('data/alaska.csv')
df.head()
# convert minute precision to nanosecond precision
df["time"] = [str(calendar.timegm(time.strptime(df["time"][t], '%Y-%m-%dT%H:%M:%SZ'))) + "000000000" for t in range(len(df))]
df.head()
# export as csv
ns_precision = df
ns_precision.to_csv('data/alaska_ns.csv', index=False)