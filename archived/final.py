
import datetime
print(datetime.datetime.now())
from struct import *
import pandas as pd
import os
import shutil
import glob
work_list = glob.glob("data/*.csv")

for m in work_list:
    #decode the file
    csv_output = True
    json_output = False
    df = pd.read_csv(m)
    shutil.copyfile(m,"incode/" + m[5:])


    line=["time,x,y,z"]

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
                thefile = open('decode/de' + m[5:], 'w')
            for item in line:
                thefile.write("%s\n" % item)
            # shutil.move('data/de' + m[5:],"decode/de" + m[5:])
        # shutil.move("data/party.csv","incode/party.csv")
    print("convert successful")





    #import the decode file into database
    from influxdb import InfluxDBClient

    #convert sample data to line protocol (with nanosecond precision)
    dfa = pd.read_csv("decode/de" + m[5:])

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

    print(datetime.datetime.now())
    os.remove(m)
    print("import successful")
