import time
import grovepi
import atexit
import logging
import json
import time.sleep as sleep
import sys

class SensorValue(object):
    unit = ''
    value = ''
    timestamp = ''
    sensor = ''
    location = ''

    def __init__(self, value, unit, sensor, location):
        self.unit = unit
        self.value = value
        self.timestamp = datetime.datetime.now()
        self.sensor = sensor
        self.location = location

    def writecsv(self):
        return self.location + "," + self.sensor + "," + self.timestamp + "," + self.value + "," + self.unit 
     

def main():
    
    # how do i manage the interval of all of the sensors?
    # i could just set it up as as a chron job and then either write the value to a file or a web service.

    sound_sensor_pin = 4 
    air_sensor_pin = 0

    sensor_polling_interval = 10

    location = 'Jons Office'

    sensorcollection = []

    while True:

        sound_data = getsoundinfo(location, sound_sensor_pin)
        print sound_data
        sensorcollection.append(sound_data)





        writetofile(data)
        time.sleep(sensor_polling_interval)



    # readdustsensor()
    # getairqualitysensorvalue()


def writetofile(data):
    with open('test1', 'ab') as f:
        for item in data:
            f.write(item.writecsv())

def gettempandhumidity():
    return 10


def getlightinfo():
    return 10

def getgasinfo():
    return 100

def getsoundinfo(location, sound_sensor):
    try:
        # Read the sound level
        sensor_value = grovepi.analogRead(sound_sensor)
        return SensorValue(sensor_value, 'none', 'Sound', location)

    except IOError:
        print ("Error")



def readdustsensor():
    print("Reading from the dust sensor")
    grovepi.dust_sensor_en()
    while True:
        try:
            [new_val,lowpulseoccupancy] = grovepi.dustSensorRead()
            print grovepi.dustSensorRead()
            if new_val:
                print(lowpulseoccupancy)
                logging.info('Dust Sensor Value: ' + str(lowpulseoccupancy))
            time.sleep(5) 

        except IOError:
            print ("Error")
        

def getairqualitysensorvalue(air_sensor_pin):

    grovepi.pinMode(air_sensor_pin,"INPUT")

    while True:
        try:
            # Get sensor value
            sensor_value = grovepi.analogRead(air_sensor_pin)

            if sensor_value > 700:
                print ("High pollution")
            elif sensor_value > 300:
                print ("Low pollution")
            else:
                print ("Air fresh")

            print("sensor_value =", sensor_value)
            time.sleep(.5)

        except IOError:
            print ("Error")



if __name__ == '__main__':
    main()

