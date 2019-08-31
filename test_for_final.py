import datetime
print(datetime.datetime.now())
from struct import *
import pandas as pd
import os
import shutil
import glob
import sched, time
from influxdb import InfluxDBClient

s = sched.scheduler(time.time, time.sleep)
def do_something(sc):
    print("Begin function: ")
    print(datetime.datetime.now())
    # do your stuff
    work_list = glob.glob("data/*/*.csv")
    for m in work_list:
        print("check is working")
        print(m)
        if m[5:8] == "fin":
            shutil.move(m, "encode/" + m[5:])

        else:
            #decode the file
            csv_output = True
            #json_output = False
            df = pd.read_csv(m)
            # shutil.copyfile(m,"incode/" + m[5:])
            # print("copy file: ")
            # print(datetime.datetime.now())


            line=["Time,X,Y,Z"]

            lines = [str(df["Time"][d])
                     + "," +
                     str(df["Rate"][d]) + ","
                     + str(df["N"][d]) + ","
                     + str(df["Data"][d])for d in range(len(df))]

            for d in lines:
                fields = d.split(",")
                # print(fields[0])
                for i in range(0, len(fields[3]),12):
                    value = fields[3][i:i+12]
                    print('value0')
                    print(value)
                    value = bytearray.fromhex(value)
                    print("value")
                    print(value)


                    (x, y, z) = unpack('>hhh', value)

                    nT = 100000

                    x = (x / 15000) * nT
                    y = (y / 15000) * nT
                    z = (z / 15000) * nT

                    x = round(x, 2)
                    y = round(y, 2)
                    z = round(z, 2)

                    if csv_output is True:
                        # print(i)
                        a = i/12*0.02
                        line.append(fields[0][:19] + str(a)[1:4] + "Z," + str(x) + "," + str(y) + "," + str(z))
                        print(fields[0][:19] + str(a)[1:4] + "Z," + str(x) + "," + str(y) + "," + str(z))
                    thefile = open('decode/de' + m[5:], 'w')
                    for item in line:
                        thefile.write("%s\n" % item)
                    # shutil.move('data/de' + m[5:],"decode/de" + m[5:])

            print("decode successful: ")
            print(datetime.datetime.now())





            #import the decode file into database

            #convert sample data to line protocol (with nanosecond precision)
            dfa = pd.read_csv("decode/de" + m[5:])

            client = InfluxDBClient(host='10.11.90.15', port=8086, username='rayf', password='rayf')
            client.create_database('RayESP')
            client.switch_database('RayESP')

            json_body = [
                {
                    "measurement": m[5:16],
                    "time": str(dfa["Time"][a]),
                    "fields": {
                        "X": float(dfa["X"][a]),
                        "Y": float(dfa["Y"][a]),
                        "Z": float(dfa["Z"][a])
                    }
                } for a in range(len(dfa))]
            client.write_points(json_body)

            os.rename(m, "data/fin" + m[5:])
            shutil.move("data/fin" + m[5:],"encode/fin" + m[5:])
            print("import and move successful: ")
            print(datetime.datetime.now())


    print("function done: ")
    print(datetime.datetime.now())

# do_something()


    s.enter(1, 1, do_something, (sc,))

s.enter(1, 1, do_something, (s,))
s.run()