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
    
    sensordatafile = getsensorfilename()
    supportedsenors = ['loudness', 'airquality', 'gas', 'tempandhumidity']
    
    parser = argparse.ArgumentParser(description='Use this to poll sensor data from raspberry pi and the grove pi')
    parser.add_argument(
        '-p', '--poll', help='Poll all sensors in the config file at the configured interval', action='store_true')

    parser.add_argument('-s', '--sensortest', help='Name of the sensor to test. Supported sensors: ' + str(supportedsenors), default='nosensor')

    parser.add_argument('-m', '--mock', help='Do a mock sensor test', action='store_true')
    args = vars(parser.parse_args())

    parser.print_usage()


    sensordata = SensorValue(5, 'none', 'Loudness', 'location')
    print sensordata.yaml()


    mockingmode = False
    if args['mock']:
        mockingmode = True

    if args['poll']:
            startautopolling(supportedsenors)

    if args['sensortest'] in supportedsenors:
        pin = getsensorconfig(args['sensortest'])
        sensortest(args['sensortest'], pin, mockingmode)

    if args['sensortest'] in ['nosensor'] and args['sensortest'] not in supportedsenors:
        print 'the sensor ' +  args['sensortest'] + ' is not supported'
        print 'currently using a dictionary called supportedsensors at the top of this file to manage this list'
        print 'supported sensors: ' + str(supportedsenors)

    if args['sensortest'] == "all":
        print "Testing all sensors"
        for item in supportedsenors:
            pin = getsensorconfig(item)
            sensortest(item, pin, mockingmode)



def getsensorconfig(sensorname):
    if sensorname in settings.keys():
        print sensorname + " is configured for port " + str(settings[sensorname]["port"])

        return settings[sensorname]["port"]
    else:
        print "missing config value for " + sensorname
        return

    
    

def getsensordata(sensorname, enablemocking):

    print 'Testing ' + sensorname + ' on port ' + str(pin)
    


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


def startautopolling(supportedsenors):
    while True:
        print "autopolling"

        for item in supportedsenors:
            
        
        values.append(getloudnessinfo(pin))


        # getairqualitysensorvalue()
        # getgassensorvalue(location, gas_sensor_pin)
        # https://github.com/DexterInd/GrovePi/blob/master/Software/Python/grove_gas_sensor.py



def getsensorfilename():
    return "sensorlog" + datetime.now().strftime('%Y%m%d%H%M%S') + ".log" 



def gettempandhumidity(senorname):
    
    pin = getsensorconfig(sensorname)

    try:
        [temp,humidity] = grovepi.dht(pin,1)
        print "temp =", temp, " humidity =", humidity
        
        sensordata = []
        sensordata.append(SensorValue(temp, 'none', 'temp', 'location'))
        sensordata.append(SensorValue(humidity, 'none', 'humidity', 'location'))

    except IOError:
        print "Error"
    return sensordata
    

def getloudnessinfo(sensorname):
    
    pin = getsensorconfig(sensorname)
    try:
        # Read the sound level
        sensor_value = grovepi.analogRead(pin)
        sensordata = SensorValue(sensor_value, 'none', 'Loudness', 'location')
    
    except IOError:
        print ("Error")
    
    return sensordata


def getgassensorvalue(sensorname):
    
    pin = getsensorconfig(sensorname)
    
    grovepi.pinMode(pin,"INPUT")
    try:
        # Get sensor value
        sensor_value = grovepi.analogRead(pin)

        # Calculate gas density - large value means more dense gas
        density = (float)(sensor_value / 1024)

        print("sensor_value =", sensor_value, " density =", density)
        sensordata = SensorValue(sensor_value, 'none', 'Gas', 'location')

    except IOError:
        print ("Error")

    return sensordata



def getairqualitysensorvalue(sensorname):
    
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

        sensordata = SensorValue(sensor_value, 'none', 'airquality', 'location')
        print("sensor_value =", sensor_value)

    except IOError:
        print ("Error")
        
    return sensordata


if __name__ == '__main__':
    main()

