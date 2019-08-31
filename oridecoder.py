from struct import *
import json

csv_output = False
json_output = True

test_line = '2016-06-19T07:59:14Z,123,123,1C4200F301C81C4100F501C81C4100F501C91C4100F501C91C4100F501C81C4100F501C91C4100F501C91C4100F301C91C4100F301C81C4100F301C81C4100F301C81C4100F501C91C4100F301C91C4100F301C81C4100F301C81C4100F301C81C4100F301C81C4200F301C81C4200F301C91C4200F301C91C4200F301C91C4200F301C91C4200F301C91C4200F301C81C4200F301C81C4200F301C81C4200F301C91C4300F301C91C4300F301C91C4300F301C91C4300F301CA1C4200F301CA1C4200F301C91C4200F301C91C4200F301C91C4200F301C91C4200F301C91C4200F301C81C4200F301C81C4200F301C91C4100F301C91C4100F301C91C4100F301C81C4100F501C81C4100F501C81C4100F501C81C4100F501C81C4100F301C91C4100F301C91C4100F301C81C4200F301C91C4200F301C91C4200F301C91C4100F301C91C4100F301C91C4200F301C91C4200F301C91C4200F301C91C4200F301C91C4200F301C91C4200F301C91C4200F301C91C4200F301C91C4200F301C91C4200F301C91C4300F301C91C4300F301C91C4300F301C91C4300F301C91C4300F301C91C4200F301C91C4200F301C91C4200F301C91C4100F301C91C4100F301C91C4200F301C91C4200F301C91C4200F301C91C4200F301C91C4200F301C91C4200F501C81C4100F301C81C4100F301C91C4100F301C91C4100F501C81C4100F301C81C4100F301C91C4200F301C91C4200F301C81C4200F301C81C4200F301C91C4200F301C91C4200F301C81C4200F301C81C4200F301C91C4200F301C91C4200F301C91C4300F301C91C4300F301CA1C4200F301C91C4200F301C91C4200F301C91C4200F301C91C4200F301C91C4300F301C91C4200F301C91C4200F301C91C4200F301C91C4200F301C91C4200F301C91C4200F301C91C4100F301C91C4100F301C81C4100F301C81C4100F501C81C4100F501C81C4100F501C81C4100F501C81C4100F301C81C4100F301C81C4100F301C91C4100F501C91C4100F301C8'

fields = test_line.split(",")

print ("Sample Starts @ ", fields[0])
print ("Sample Rate: \t", fields[1], "Hz")
print ("N = \t\t\t", fields[2])


for i in range(0, len(fields[3]),12):
    print(i)

    value = fields[3][i:i+12]

    value = bytearray.fromhex(value)
    #print(value)

    (x, y, z) = unpack('>hhh', value)

    nT = 100000

    x = (x / 15000) * nT
    y = (y / 15000) * nT
    z = (z / 15000) * nT

    x = round(x, 2)
    y = round(y, 2)
    z = round(z, 2)

    if csv_output is True:

        print(fields[0] + "," + str(x) + "," + str(y) + "," + str(z))

    elif json_output is True:

        json_data = json.dumps({'timestamp': fields[0], 'x': x, 'y': y, 'z': z}, sort_keys=True, indent=None,
                               separators=(',', ':'))
        print(json_data)



