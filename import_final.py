import glob
import os
import re
import sched
import shutil
import smtplib
import statistics
import time
from struct import *

import pandas as pd
from influxdb import InfluxDBClient

# print(datetime.datetime.now())

s = sched.scheduler(time.time, time.sleep)

dirChange = 'cd /home/rayf/'
delInvalidFile = 'find . -name "*.csv" -size -30k -delete'

os.system(dirChange)

def sendemail(from_addr, to_addr_list, cc_addr_list,
              subject, message,
              login, password,
              smtpserver='smtp.gmail.com:587'):
    header = 'From: %s\n' % from_addr
    header += 'To: %s\n' % ','.join(to_addr_list)
    header += 'Cc: %s\n' % ','.join(cc_addr_list)
    header += 'Subject: %s\n\n' % subject
    message = header + message

    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login, password)
    problems = server.sendmail(from_addr, to_addr_list, message)
    server.quit()
    return problems


def do_something(sc):
    # print("Begin function: ")
    # print(datetime.datetime.now())
    # do your stuff
    os.system(delInvalidFile)

    work_list = glob.glob("data/*/*.csv")
    # print(work_list)
    # print("work list")

    for m in work_list:
        # print("check is working")

        station = re.search("/(.*)/",m).group(1)
        file = re.search(station+"/(.*)",m).group(1)
        pathway = re.search("/(.*)",m).group(1)

        if file[0:3] == "fin":
            shutil.move(m, "encode/" + pathway)

        else:
            # decode the file
            csv_output = True
            # json_output = False
            df = pd.read_csv(m)
            # shutil.copyfile(m,"incode/" + m[5:])

            line = ["Time,X,Y,Z"]

            lines = [str(df["Time"][d])
                     + "," +
                     str(df["Rate"][d]) + ","
                     + str(df["N"][d]) + ","
                     + str(df["Data"][d]) for d in range(len(df))]

            avgLine = []
            eptX = []
            eptY = []
            eptZ = []

            # print(len(lines[0])<100)
            if len(lines[0]) < 100:
                # print("I'm working!!!")
                shutil.move(m, "blank_data/"+pathway)
                sendemail( from_addr='aaaa.zhao@g.northernacademy.org',
                        to_addr_list=['azhao@northernacademy.org'],
                        cc_addr_list=['lin.feng@g.northernacademy.org'],
                             subject='Import Problem',
                             message='Hello! You just get a group of empty data from the machine.',
                               login='aaaa.zhao@g.northernacademy.org',
                            password='qwer1234')
                # do_something()

                continue

            for d in lines:
                fields = d.split(",")
                # print(fields[0])
                for i in range(0, len(fields[3]), 12):
                    value = fields[3][i:i + 12]

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
                        a = i / 12 * 0.02
                        line.append(fields[0][:19] + str(a)[1:4] + "Z," + str(x) + "," + str(y) + "," + str(z))
                        eptX.append(x)
                        eptY.append(y)
                        eptZ.append(z)
                        # print('This is each line')
                        # print(fields[0][:19] + str(a)[1:4] + "Z," + str(x) + "," + str(y) + "," + str(z))
                x = statistics.mean(eptX)
                y = statistics.mean(eptY)
                z = statistics.mean(eptZ)
                # avgLine.append(x)
                # avgLine.append(y)
                # avgLine.append(z)
                avgLine.append({
                    "measurement": station+"avg",
                    "time": str(fields[0][:19]+"Z"),
                    "fields": {
                        "X": float(x),
                        "Y": float(y),
                        "Z": float(z)
                    }
                })

            thefile = open('decode/' + station + '/de' + file, 'w+')
            # print("The file, line 137")
            # print('decode/' + m[5:16] + '/de' + m[17:])
            # print("This is avg line")
            # print(avgLine)
            for item in line:
                thefile.write("%s\n" % item)

            # import the decode file into database

            # convert sample data to line protocol (with nanosecond precision)
            dfa = pd.read_csv('decode/' + station + '/de' + file)

            json_body = [
                {
                    "measurement": station,
                    "time": str(dfa["Time"][a]),
                    "fields": {
                        "X": float(dfa["X"][a]),
                        "Y": float(dfa["Y"][a]),
                        "Z": float(dfa["Z"][a])
                    }
                } for a in range(len(dfa))]

            try:
                client = InfluxDBClient(host='aworldbridgelabs.com', port=8086, database="RayESP", username='rayf', password='RayESP8010')
                client.write_points(json_body)
                client = InfluxDBClient(host='aworldbridgelabs.com', port=8086, database="RayESP", username='rayf', password='RayESP8010')
                client.write_points(avgLine)

                os.rename(m, "data/" + station + '/fin' + file)
                # print("Renamed file: line 177")
                # print("data/" + m[5:16] + '/fin' + m[17:])
                shutil.move("data/" + station + '/fin' + file, "encode/" + station + '/fin' + file)

            except Exception:
                print("something wrong about client.write_points!")
                shutil.move(m, "error/" + pathway)
                sendemail(from_addr='aaaa.zhao@g.northernacademy.org',
                          to_addr_list=['azhao@northernacademy.org'],
                          cc_addr_list=['lin.feng@g.northernacademy.org'],
                          subject='Import Problem',
                          message='Hello! It seems like there are some influxDB importing problem about the method, '
                                  'client.write_points',
                          login='aaaa.zhao@g.northernacademy.org',
                          password='qwer1234')
            continue

    # print("function done: ")
    # print(datetime.datetime.now())

    s.enter(20, 1, do_something, (sc,))

s.enter(20, 1, do_something, (s,))
s.run()