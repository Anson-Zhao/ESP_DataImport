import glob
import os
import pandas as pd
import influxdb
work_list = glob.glob("data/*/*.csv")
print(work_list)
print("RayTest" + work_list[0][5:16])
print('decode/' + work_list[0][5:16] + '/de'+ work_list[0][17:])
import smtplib

# print(work_list)
# print(work_list[0][5:7])
# print("incode"+ work_list[0][4:])
#
# print("\""+work_list[0]+"\"")
# print("incode/" + "\""+work_list[0]+"\"")
# file = work_list[0][0]
# print("\""+file+"\"")

# for m in work_list:
#     print(m)
#     print("incode"+m[4:])
#     os.remove(m)


# df = pd.read_csv("data/1.csv")
# for z in range(0,50):
#     a = 0.02*z
#     print(str(df["time"][0])[:19]+str(a)[1:4]+"Z")


# os.rename("data/123","data/12234")

# def sendemail(from_addr, to_addr_list, cc_addr_list,
#               subject, message,
#               login, password,
#               smtpserver='smtp.gmail.com:587'):
#     header  = 'From: %s\n' % from_addr
#     header += 'To: %s\n' % ','.join(to_addr_list)
#     header += 'Cc: %s\n' % ','.join(cc_addr_list)
#     header += 'Subject: %s\n\n' % subject
#     message = header + message
#
#     server = smtplib.SMTP(smtpserver)
#     server.starttls()
#     server.login(login,password)
#     problems = server.sendmail(from_addr, to_addr_list, message)
#     server.quit()
#     return problems
#
# sendemail(from_addr    = 'aaaa.zhao@g.northernacademy.org',
#           to_addr_list = ['lin.feng@g.northernacademy.org'],
#           cc_addr_list = ['lin.feng@g.northernacademy.org'],
#           subject      = 'Import Problem',
#           message      = 'Hello! It seems like there are some influxDB importing problem about the file, test_for_final.',
#           login        = 'aaaa.zhao@g.northernacademy.org',
#           password     = 'qwer1234')
mystring = '11BAF7C90A3811B5F7D30A4011BAF7CE0A4211C4F7BD0A3C11C8F7B40A3311C2F7BA0A3011B9F7CA0A3711B3F7D30A4011BAF7CD0A4211C5F7BC0A3B11C8F7B30A3311C2F7BA0A3211B9F7CA0A3811B6F7D30A4011BBF7CB0A4211C5F7BA0A3C11C8F7B30A3311C0F7BC0A3211B9F7CB0A3811B6F7D30A4011BCF7CB0A4211C5F7BA0A3B11C7F7B30A3311BFF7BD0A3211B7F7CD0A3A11B6F7D30A4011BEF7C90A4011C7F7B90A3A11C8F7B40A3211BFF7BE0A3311B7F7CE0A3B11B6F7D30A4211BEF7C70A4011C7F7B80A3A11C7F7B40A3311BEF7C10A3311B6F7CF0A3B11B6F7D20A4211BEF7C60A4011C7F7B70A3A11C7F7B40A3211BCF7C10A3311B6F7CF0A3B11B7F7D20A4211BFF7C50A4011C8F7B70A3811C7F7B50A3211BCF7C30A3311B6F7D00A3B11B9F7D00A42'
b = bytes.fromhex(mystring)
# b = mystring.encode()
print(b)