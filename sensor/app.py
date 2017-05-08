import time
import grovepi
import atexit
import json
import sys

import argparse

from datetime import datetime


# get import working from a directory
from sensorvalue import SensorValue
from config import settings

def main():
    
    # two collections that really matter
    #one is the list of sensors that are supported by this code.
    supportedsensors = ['loudness', 'airquality', 'gas', 'tempandhumidity']
    
    #two is the list of sensors configured in the settings.yaml file
    configuredsensors = settings["core"]["configuredsensors"]


    if not isconfigvalid(supportedsensors):
        print 'Configuration is invalid'
        return

    sensordatafile = getsensorfilename()

    
    parser = argparse.ArgumentParser(description='Use this to poll sensor data from raspberry pi and the grove pi')
    parser.add_argument(
        '-p', '--poll', help='Poll all sensors in the config file at the configured interval', action='store_true')

    parser.add_argument('-s', '--sensortest', help='Name of the sensor to test. Supported sensors: ' + str(supportedsensors), default='nosensor')

    parser.add_argument('-m', '--mock', help='Do a mock sensor test', action='store_true')
    args = vars(parser.parse_args())

    parser.print_usage()

    mockingmode = False
    if args['mock']:
        mockingmode = True

    if args['poll']:
            startautopolling(configuredsensors, mockingmode)

    if args['sensortest'] in supportedsensors:
        sensordata = getsensordata(args['sensortest'], mockingmode)

        if sensordata != None:
            for data in sensordata:
                if data == None:
                    print 'No data was returned by the sensor'
                else:
                    print data.yaml()

    if args['sensortest'] in ['nosensor'] and args['sensortest'] not in supportedsensors:
        print 'the sensor ' +  args['sensortest'] + ' is not supported'
        print 'currently using a dictionary called supportedsensors at the top of this file to manage this list'
        print 'supported sensors: ' + str(supportedsensors)

    if args['sensortest'] == "all":
        print "Looping through the sensors " + str(supportedsensors)
        for item in supportedsensors:
            data = getsensordata(item, mockingmode)
            for item in data:
                print item.yaml()



def isconfigvalid(supportedsensors):
    configuredsensors = settings["core"]["configuredsensors"]

    for sensor in configuredsensors:
        if sensor not in supportedsensors:
            print "The " + sensor + "sensor is not supported"
            return False

    return True
        
    
    

def getsensorconfig(sensorname):
    if sensorname in settings.keys():
        print sensorname + " is configured for port " + str(settings[sensorname]["port"])

        return settings[sensorname]["port"]
    else:
        print "missing config value for " + sensorname
        return

    
    

def getsensordata(sensorname, enablemocking):

    
    if enablemocking:
        return

    if sensorname == "loudness":
        return getloudnessinfo(sensorname)
    if sensorname == "airquality":
        return getairqualitysensorvalue(sensorname)
    if sensorname == "gas":
        return getgassensorvalue(sensorname)
    if sensorname == "tempandhumidity":
        return gettempandhumidity(sensorname)
    if sensorname == "dust":
        return readdustsensor(sensorname)


def startautopolling(configuredsensors, enablemocking):
    
    print "Starting to Autopoll the sensors"
    pollinginterval = settings["core"]["pollinginterval"]

    #start the polling loop
    while True:
        if pollinginterval != settings["core"]["pollinginterval"]:
            print "polling interval changed from " + str(pollinginterval) + " to " + settings["core"]["pollinginterval"]
            pollinginterval = settings["core"]["pollinginterval"]
        
        #check for a new polling interval
        values = []

        for item in configuredsensors:
            values.append(getsensordata(item, enablemocking))

        writetofile(values)

        time.sleep(pollinginterval)

    

        # getairqualitysensorvalue()
        # getgassensorvalue(location, gas_sensor_pin)
        # https://github.com/DexterInd/GrovePi/blob/master/Software/Python/grove_gas_sensor.py



def writetofile(data):
    with open(sensorfilename, 'ab') as f:
        for item in data:
            f.write(item.writecsv() + '\n')


def getsensorfilename():
    return "sensorlog" + datetime.now().strftime('%Y%m%d%H%M%S') + ".log" 


def readdustsensor(sensorname):
    
    sensordata = []

    pin = getsensorconfig(sensorname)

    atexit.register(grovepi.dust_sensor_dis)

    print("Reading from the dust sensor")
    grovepi.dust_sensor_en()

    try:
                [new_val,lowpulseoccupancy] = grovepi.dustSensorRead()

                print "new_val: " + str(new_val)
                print "lowpulseoccupancy: " + str(lowpulseoccupancy)

                if new_val:
                    print(lowpulseoccupancy)
                    sensordata.append(SensorValue(lowpulseoccupancy, 'none', 'Dust', 'location'))

    except IOError:
        print ("Error")
            
    return sensordata

def gettempandhumidity(sensorname):
    
    pin = getsensorconfig(sensorname)
    dht_sensor_type = 0             # change this depending on your sensor type - see header comment


    try:
        [temp,humidity] = grovepi.dht(pin,dht_sensor_type)
        print "temp =", temp, " humidity =", humidity
        
        sensordata = []
        sensordata.append(SensorValue(temp, 'none', 'temp', 'location'))
        sensordata.append(SensorValue(humidity, 'none', 'humidity', 'location'))

    except IOError:
        print "Error"
    return sensordata
    

def getloudnessinfo(sensorname):
    
    sensordata = []
    pin = getsensorconfig(sensorname)
    try:
        # Read the sound level
        sensor_value = grovepi.analogRead(pin)
        sensordata.append(SensorValue(sensor_value, 'none', 'Loudness', 'location'))
    
    except IOError:
        print ("Error")
    
    return sensordata


def getgassensorvalue(sensorname):
    
    sensordata = []
    pin = getsensorconfig(sensorname)
    
    grovepi.pinMode(pin,"INPUT")
    try:
        # Get sensor value
        sensor_value = grovepi.analogRead(pin)

        # Calculate gas density - large value means more dense gas
        density = (float)(sensor_value / 1024)
        sensordata.append(SensorValue(sensor_value, 'none', 'Gas', 'location'))

    except IOError:
        print ("Error")

    return sensordata



def getairqualitysensorvalue(sensorname):
    
    sensordata = []
    pin = getsensorconfig(sensorname)

    grovepi.pinMode(pin,"INPUT")

    try:
        # Get sensor value
        sensor_value = grovepi.analogRead(pin)

        if sensor_value > 700:
            print ("High pollution")
        elif sensor_value > 300:
            print ("Low pollution")
        else:
            print ("Air fresh")
        sensordata.append(SensorValue(sensor_value, 'none', 'airquality', 'location'))
    except IOError:
        print ("Error")
        
    return sensordata


if __name__ == '__main__':
    main()

