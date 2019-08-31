from influxdb import InfluxDBClient
import pandas as pd

#convert sample data to line protocol (with nanosecond precision)
dfa = pd.read_csv("decode/ESP_2_Kodiak_2016-04-28.csv")

client = InfluxDBClient(host='10.11.90.15', port=8086, username='rayf', password='rayf')
client.create_database('MachineLearning')
client.switch_database('MachineLearning')

json_body = [
    {
        "measurement": "Kodiak_2016_04_28",
        "Time": str(dfa["Time"][a]),
        "fields": {
            "X": float(dfa["X"][a]),
            "Y": float(dfa["Y"][a]),
            "Z": float(dfa["Z"][a])
        }
    } for a in range(len(dfa))]

client.write_points(json_body)
print("done")