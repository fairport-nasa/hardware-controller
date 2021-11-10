from influxdb import InfluxDBClient
import qwiic
import os
import random
import time

device = qwiic.create_device("QwiicProximity")
device.begin()

client = InfluxDBClient('localhost',8086,'root','root','sensors')
client.create_database('sensors')

while True:
    json_body = [
    {
        "measurement": "proximity",
        "time":"2021-11-03T23:00:"+str(random.randint(0,60))+"z",
        "fields": {
            "value": device.proximity
        }
    }
    ]
    client.write_points(json_body)
    result = client.query('select value from proximity;')
    os.system("clear")
    for r in result.get_points():
        print("value: ",r["value"])
    time.sleep(12)
