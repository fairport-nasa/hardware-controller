from influxdb import InfluxDBClient
import os
import datetime
import time

import qwiic_proximity
import qwiic_bme280

#initialize influx client
client = InfluxDBClient('localhost',8086,'root','root','sensors')
client.create_database('sensors')

#create sensor array
daSensors = []
daSensors += [[qwiic_proximity.QwiicProximity(),"proximity"]]
daSensors += [[qwiic_bme280.QwiicBme280(),"temperature_celsius"]]

#tell every sensor to begin
for daSensor in daSensors:
    daSensor[0].begin()

#the rest of the code should repeat indefinetly
while True:
    
    #clear the screen
    os.system("clear")
    
    #repeat for every sensor
    for daSensor in daSensors:
        
        #get the value of the sensor
        get_result = getattr(daSensor[0],daSensor[1])
        
        #display the current value of the sensor
        print(daSensor[1],get_result)
        
        #create json object to add to influx
        json_body = [
            {
                "measurement": daSensor[1],
                "time": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%Sz"),
                "fields": {
                    "value": get_result
                }
            }
        ]
        
        #write the json object to influx
        client.write_points(json_body)
    
    #sleep a bit to reduce disk usage and resource usage
    time.sleep(2)
