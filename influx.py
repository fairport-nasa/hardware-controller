from influxdb import InfluxDBClient
import os
import datetime
import time

import qwiic_proximity
import qwiic_bme280

client = InfluxDBClient('localhost',8086,'root','root','sensors')
client.create_database('sensors')

daSensors = []

daSensors += [[qwiic_proximity.QwiicProximity(),"proximity"]]
daSensors += [[qwiic_bme280.QwiicBme280(),"temperature_celsius"]]

for daSensor in daSensors:
    daSensor[0].begin()

while True:
    os.system("clear")
    for daSensor in daSensors:
        get_result = getattr(daSensor[0],daSensor[1])
        print(daSensor[1],get_result)
        json_body = [
            {
                "measurement": daSensor[1],
                "time": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%Sz"),
                "fields": {
                    "value": get_result
                }
            }
        ]
        client.write_points(json_body)
    time.sleep(2)
