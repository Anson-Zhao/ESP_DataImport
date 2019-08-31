from struct import *
import datetime
import pandas as pd
import os
import shutil
import glob
import sched, time
from influxdb import InfluxDBClient
print("begin!")

s = sched.scheduler(time.time, time.sleep)
def do_something(sc):
    print("Begin function: ")
    print(datetime.datetime.now())

    # grab all csv file under the path
    work_list = glob.glob("data/*.csv")
    print(work_list)

    #check every file before working
    for m in work_list:
        #move the file if it's decoded already
        if m[5:8] == "fin":
            print("check is working")
            print(m)
            shutil.move(m, "encode/" + m[5:])

        else:
            #decode the file
            csv_output = True
            df = pd.read_csv(m)

            #add the head line
            line=["Time,X,Y,Z"]

            #grab every line in one file into array: lines
            lines = [str(df["Time"][d])
                     + "," +
                     str(df["Rate"][d]) + ","
                     + str(df["N"][d]) + ","
                     + str(df["Data"][d])for d in range(len(df))]

            #decode every line in the array: lines
            for d in lines:
                fields = d.split(",")
                #decode one line
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

                    #put decoded lines into array: line
                    if csv_output is True:
                        a = i/12*0.02
                        line.append(fields[0][:19] + str(a) + "Z," + str(x) + "," + str(y) + "," + str(z))
                        print(fields[0][:19] + str(a)[1:4] + "Z," + str(x) + "," + str(y) + "," + str(z))

            #write the lines into the decode file's path
            thefile = open('decode/de' + m[5:], 'w')
            for item in line:
                thefile.write("%s\n" % item)
            print("finish decoded file")

            #import the decode file into database
            dfa = pd.read_csv("decode/de" + m[5:])
            print("1")

            client = InfluxDBClient(host='10.11.90.15', port=8086, username='rayf', password='rayf')
            client.create_database('RayESP')
            client.switch_database('RayESP')
            print("connected")

            #convert datas to json
            json_body = [
                {
                    "measurement": "test_test",
                    "Time": str(dfa["Time"][a]),
                    "fields": {
                        "X": str(dfa["X"][a]),
                        "Y": str(dfa["Y"][a]),
                        "Z": str(dfa["Z"][a])
                    }
                } for a in range(len(dfa))]
            client.write_points(json_body)
            print("finish import")

            # rename and move the file
            os.rename(m, "data/fin" + m[5:])
            shutil.move("data/fin" + m[5:],"encode/fin" + m[5:])
            print("move rename done")
            print(datetime.datetime.now())

    print("function done: ")
    print(datetime.datetime.now())
    s.enter(1, 1, do_something, (sc,))

# run itself every 60 seconds
s.enter(1, 1, do_something, (s,))
s.run()