
import pandas as pd

from influxdb import InfluxDBClient

# convert the time to timestamp
import calendar, time
# import csv
# df = pd.read_csv('data/part.csv')
# df.head()
# # convert minute precision to nanosecond precision
# df["time"] = [str(calendar.timegm(time.strptime(str(df["time"][t]), '%Y-%m-%dT%H:%M:%SZ'))) + "000000000" for t in range(len(df))]
# df.head()
# # export as csv
# ns_precision = df
# ns_precision.to_csv('data/part_ns.csv', index=False)


#convert csv's to line protocol

#convert sample data to line protocol (with nanosecond precision)


# lines = ["price"
# + ","
# + "latitude=" + str(df["latitude"][d]) + ","
# + "longitude=" + str(df["longitude"][d]) + ","
# + "message=" + str(df["message"][d])
# + " " + str(df["time"][d]) for d in range(len(df))]
# thefile = open('data/part.txt', 'w')
# for item in lines:
#     thefile.write("%s\n" % item)


# client = InfluxDBClient(host='localhost', port=8086)
df = pd.read_csv("data/partN.csv")
# json_body = []
client = InfluxDBClient(host='10.11.90.15', port=8086, username='rayf', password='rayf')
client.create_database('RayESP')
client.switch_database('RayESP')

json_body = [
    {
        "measurement": "pri",
        "time": str(df["time"][a]),
        "fields": {
            "x": str(df["x"][a]),
            "y": str(df["y"][a]),
            "z": str(df["z"][a])
        }
    } for a in range(len(df))]
client.write_points(json_body)

# "latitude": str(df["latitude"][a]),
# "longitude": str(df["longitude"][a]),
# "message": str(df["message"][a])

# "x": str(df["xxx"][a]),
# "y": str(df["yyy"][a]),
# "z": str(df["zzz"][a])

# for a in range(len(df)):
#     json_body.append(
#         {
#             "measurement": "esp",
#             "time": str(df["time"][a]),
#             "fields": {
#                 "latitude": str(df["Latitude"][a]),
#                 "longitude": str(df["Longitude"][a]),
#                 "message": str(df["Message"][a])
#             }
#         })
