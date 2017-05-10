import sys
import time
import grovepi
import atexit
import json
import sys
import logging
from __future__ import print_function

sys.path.append('lib/')


import argparse

from datetime import datetime

# get import working from a directory
from sensorvalue import SensorValue
from sensorconfig import SensorConfig
from sensor import Sensor
import notifier

def main():
    
    # two collections that really matter
    #one is the list of sensors that are supported by this code.
    supportedsensors = ['loudness', 'airquality', 'gas', 'tempandhumidity']

    sensorconfig = SensorConfig(settings)


    #two is the list of sensors configured in the settings.yaml file

    if not sensorconfig.isconfigvalid(supportedsensors):
        print 'Configuration is invalid'
        return

    sensordatafile = getsensorfilename()

    
    parser = argparse.ArgumentParser(description='Use this to poll sensor data from raspberry pi and the grove pi')
    parser.add_argument(
        '-p', '--poll', help='Poll all sensors in the config file at the configured interval', action='store_true')

    parser.add_argument('-s', '--sensortest', help='Name of the sensor to test. Supported sensors: ' + str(supportedsensors), default='nosensor')

    parser.add_argument('-m', '--mock', help='Do a mock sensor test', action='store_true')
    parser.add_argument('-n', '--notify', help='Perform a notification test', action='store_true')

    args = vars(parser.parse_args())

    parser.print_usage()

    mockingmode = False
    if args['mock']:
        mockingmode = True

    # if args['notify']:
    #     notifier.sendnotification("Test message",  "Test subject")

    if args['poll']:
            startautopolling(sensorconfig.configuredsensors, mockingmode, sensorconfig)

    if args['sensortest'] in supportedsensors:
        sensordata = getsensordata(args['sensortest'], mockingmode, sensorconfig)

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


    # The all case loops through all of the configured sensors and prints out there values
    if args['sensortest'] == "all":
        print "Looping through the sensors " + str(sensorconfig.configuredsensors)
        for item in sensorconfig.configuredsensors:
            data = getsensordata(item, mockingmode, sensorconfig)

            if data == None:
                print "No Data was returned"
                print "Exiting...."
                return

            for item in data:
                print item.yaml()




def getsensorconfig(sensorname):
    if sensorname in settings.keys():
        print sensorname + " is configured for port " + str(settings[sensorname]["port"])

        return settings[sensorname]["port"]
    else:
        print "missing config value for " + sensorname
        return


def getsensordata(sensorname, enablemocking, sensorconfig):

    sensor = Sensor(sensorconfig)

    if enablemocking:
        return

    try:

        if sensorname == "loudness":
            return sensor.getloudnessinfo(sensorname)
        if sensorname == "airquality":
            return sensor.getairqualitysensorvalue(sensorname)
        if sensorname == "gas":
            return sensor.getgassensorvalue(sensorname)
        if sensorname == "tempandhumidity":
            return sensor.gettempandhumidity(sensorname)
        if sensorname == "dust":
            return sensor.readdustsensor(sensorname)
    except:
        print sys.exc_info()[0]



def startautopolling(configuredsensors, enablemocking, sensorconfig):
    
    print "Starting to Autopoll the sensors"
    pollinginterval = settings["core"]["pollinginterval"]
    sensordatafile = getsensorfilename()

    #start the polling loop
    while True:
        if pollinginterval != settings["core"]["pollinginterval"]:
            print "polling interval changed from " + str(pollinginterval) + " to " + settings["core"]["pollinginterval"]
            pollinginterval = settings["core"]["pollinginterval"]
        
        #check for a new polling interval
        values = []

        for item in configuredsensors:
            sensorvalue = getsensordata(item, enablemocking, sensorconfig)
            if sensorvalue != None:
                values.append(sensorvalue)

        writetofile(values, sensordatafile)

        time.sleep(pollinginterval)

        # getairqualitysensorvalue()
        # getgassensorvalue(location, gas_sensor_pin)
        # https://github.com/DexterInd/GrovePi/blob/master/Software/Python/grove_gas_sensor.py



def writetofile(data, sensordatafile):
    with open(sensordatafile, 'ab') as f:
        for items in data:
            for item in items:
                f.write(item.writecsv() + '\n')


def getsensorfilename():
    return "sensorlog" + datetime.now().strftime('%Y%m%d%H%M%S') + ".log" 


if __name__ == '__main__':
    main()

