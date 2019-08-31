
import datetime
print(datetime.datetime.now())
from struct import *
import pandas as pd
import os
import shutil

#decode the file
csv_output = True
json_output = False
df = pd.read_csv("data/party.csv")
line=["time,x,y,z"]

lines = [str(df["Time"][d])
         + "," +
         str(df["X"][d]) + ","
         + str(df["Y"][d]) + ","
         + str(df["Z"][d])for d in range(len(df))]

for d in lines:
    fields = d.split(",")
    for i in range(0, len(fields[3]),12):
        value = fields[3][i:i+12]

        value = bytearray.fromhex(value)

        (x, y, z) = unpack('>hhh', value)

        nT = 100000

        x = (x / 15000) * nT
        y = (y / 15000) * nT
        z = (z / 15000) * nT

        x = round(x, 2)
        y = round(y, 2)
        z = round(z, 2)

        if csv_output is True:
            line.append(fields[0] + "," + str(x) + "," + str(y) + "," + str(z))
            print(fields[0] + "," + str(x) + "," + str(y) + "," + str(z))
            thefile = open('data/partyy.csv', 'w')
        for item in line:
            thefile.write("%s\n" % item)
        shutil.move("data/party.csv","incode/party.csv")



#import the decode file into database
from influxdb import InfluxDBClient

#convert sample data to line protocol (with nanosecond precision)
dfa = pd.read_csv("data/partyy.csv")

client = InfluxDBClient(host='10.11.90.15', port=8086, username='rayf', password='rayf')
client.create_database('RayESP')
client.switch_database('RayESP')

json_body = [
    {
        "measurement": "ESP",
        "time": str(dfa["time"][a]),
        "fields": {
            "x": str(dfa["x"][a]),
            "y": str(dfa["y"][a]),
            "z": str(dfa["z"][a])
        }
    } for a in range(len(dfa))]

client.write_points(json_body)
shutil.move("data/partyy.csv","decode/partyy.csv")
print(datetime.datetime.now())