import time
import grovepi
import atexit
import logging
import json
import sys
import datetime
import sensorvalue



def main():
    location = 'Jons Office'
    readdustsensor(location)

def writetofile(data):
    with open('dustdata.csv', 'ab') as f:
        f.write(data.writecsv() + '\n')


def readdustsensor(location):
    atexit.register(grovepi.dust_sensor_dis)

    print("Reading from the dust sensor")
    grovepi.dust_sensor_en()
    while True:
        try:
                    [new_val,lowpulseoccupancy] = grovepi.dustSensorRead()
                    if new_val:
                            print(lowpulseoccupancy)
                            sensordata = SensorValue(lowpulseoccupancy, 'none', 'Dust', location)
                            writetofile(sensordata)
                    time.sleep(5) 

        except IOError:
            print ("Error")
            
if __name__ == '__main__':
    main()

