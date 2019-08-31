import datetime
print(datetime.datetime.now())
from struct import *
import pandas as pd

csv_output = True
json_output = False
df = pd.read_csv("data/part.csv")
line=["time, x, y, z"]

lines = [str(df["time"][d])
         + "," +
         str(df["latitude"][d]) + ","
         + str(df["longitude"][d]) + ","
         + str(df["message"][d])for d in range(len(df))]

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
            thefile = open('data/partN.csv', 'w')
        for item in line:
            thefile.write("%s\n" % item)
