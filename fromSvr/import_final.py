import datetime
print(datetime.datetime.now())
from struct import *
import pandas as pd
import os
import shutil
import glob
import sched, time
from influxdb import InfluxDBClient
import smtplib

s = sched.scheduler(time.time, time.sleep)
def sendemail(from_addr, to_addr_list, cc_addr_list,
              subject, message,
              login, password,
              smtpserver='smtp.gmail.com:587'):
    header  = 'From: %s\n' % from_addr
    header += 'To: %s\n' % ','.join(to_addr_list)
    header += 'Cc: %s\n' % ','.join(cc_addr_list)
    header += 'Subject: %s\n\n' % subject
    message = header + message

    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login,password)
    problems = server.sendmail(from_addr, to_addr_list, message)
    server.quit()
    return problems

def do_something(sc):
    print("Begin function: ")
    print(datetime.datetime.now())
    # do your stuff
    work_list = glob.glob("data/*/*.csv")
    print(work_list)

    for m in work_list:
        print("check is working")
        print(m)
        if m[17:20] == "fin":
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
                        a = i/12*0.02
                        line.append(fields[0][:19] + str(a)[1:4] + "Z," + str(x) + "," + str(y) + "," + str(z))
                        print(fields[0][:19] + str(a)[1:4] + "Z," + str(x) + "," + str(y) + "," + str(z))
                    thefile = open('decode/' + m[5:16] + '/de'+ m[17:], 'w')
                    for item in line:
                        thefile.write("%s\n" % item)
                    # shutil.move('data/de' + m[5:],"decode/de" + m[5:])

            print("decode successful: ")
            print(datetime.datetime.now())





            #import the decode file into database

            #convert sample data to line protocol (with nanosecond precision)
            dfa = pd.read_csv('decode/' + m[5:16] + '/de'+ m[17:])

                        #client.create_database('RayESP')
            #client.switch_database('RayESP')

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

            try:
                client = InfluxDBClient(host='localhost', port=8086, database="RayESP", username='rayf', password='RayESP8010')
                client.write_points(json_body)


                os.rename(m, "data/" + m[5:16] + '/fin' + m[17:])
                shutil.move("data/" + m[5:16] + '/fin' + m[17:],"encode/" + m[5:16] + '/fin' + m[17:])
                print("import and move successful: ")
                print(datetime.datetime.now())

            except Exception:
                print("something wrong about client.write_points!")
                shutil.move(m, "error/"+m[5:])
                sendemail(from_addr    = 'aaaa.zhao@g.northernacademy.org',
                          to_addr_list = ['lin.feng@g.northernacademy.org'],
                          cc_addr_list = ['lin.feng@g.northernacademy.org'],
                          subject      = 'Import Problem',
                          message      = 'Hello! It seems like there are some influxDB importing problem about the method, client.write_points',
                          login        = 'aaaa.zhao@g.northernacademy.org',
                          password     = 'qwer1234')
            continue





    print("function done: ")
    print(datetime.datetime.now())

    # do_something()


    s.enter(30, 1, do_something, (sc,))

s.enter(30, 1, do_something, (s,))
s.run()