from __future__ import print_function
import sys
sys.path.append('lib/')
import time
import grovepi
import atexit
import json
import sys
import logging
import argparse
from datetime import datetime
# get import working from a directory
from sensorvalue import SensorValue
from sensorconfig import SensorConfig
from sensor import Sensor
from iotconfig import IOTConfig
import notifier

def main(args):
    
    supportedsensors = ['loudness', 'airquality', 'gas', 'tempandhumidity']

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # create a file handler
    handler = logging.FileHandler('hello.log')
    handler.setLevel(logging.INFO)

    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(handler)


    args = parser_args(sys.argv[1:])

    #Load and initialize the config file
    sensorconfig = IOTConfig()
    sensorconfig.initializefromfile(args['configfile'])

    #two is the list of sensors configured in the settings.yaml file

    if not sensorconfig.isconfigvalid(supportedsensors):
        print('Configuration is invalid')
        return

    sensordatafile = getsensorfilename()




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
                    print('No data was returned by the sensor')
                else:
                    print(data.yaml())

    if args['sensortest'] in ['nosensor'] and args['sensortest'] not in supportedsensors:
        print ('the sensor ' +  args['sensortest'] + ' is not supported')
        print ('currently using a dictionary called supportedsensors at the top of this file to manage this list')
        print ('supported sensors: ' + str(supportedsensors))


    # The all case loops through all of the configured sensors and prints out there values
    if args['sensortest'] == "all":
        print ("Looping through the sensors " + str(sensorconfig.configuredsensors))
        for item in sensorconfig.configuredsensors:
            data = getsensordata(item, mockingmode, sensorconfig)

            if data == None:
                print ("No Data was returned")
                print ("Exiting....")
                return

            for item in data:
                print (item.yaml())





def parser_args(args):
    
    print (str(args))

    parser = argparse.ArgumentParser(description='Use this to poll sensor data from raspberry pi and the grove pi')
    parser.add_argument(
        '-p', '--poll', help='Poll all sensors in the config file at the configured interval', action='store_true')
    parser.add_argument('-s', '--sensortest', help='Name of the sensor to test.', default='nosensor')
    parser.add_argument('-m', '--mock', help='Do a mock sensor test', action='store_true')
    parser.add_argument('-c', '--configfile', help='Specify Settings file', default='settings.yaml')
    parser.add_argument('-n', '--notify', help='Perform a notification test', action='store_true')
    args = vars(parser.parse_args(args))
    parser.print_usage()

    return args
    




def getsensordata(sensorname, enablemocking, sensorconfig):

    sensor = Sensor(sensorconfig)

    if enablemocking:
        return

    try:

        if sensorname == "loudness":
            return sensor.getloudnessinfo(sensorconfig)
        if sensorname == "airquality":
            return sensor.getairqualitysensorvalue(sensorconfig)
        if sensorname == "gas":
            return sensor.getgassensorvalue(sensorconfig)
        if sensorname == "tempandhumidity":
            return sensor.gettempandhumidity(sensorconfig)
        if sensorname == "dust":
            return sensor.readdustsensor(sensorconfig)
    except:
        print (sys.exc_info()[0])



def startautopolling(configuredsensors, enablemocking, sensorconfig):
    
    print ("Starting to Autopoll the sensors")
    pollinginterval = settings["core"]["pollinginterval"]
    sensordatafile = getsensorfilename()

    #start the polling loop
    while True:
        if pollinginterval != settings["core"]["pollinginterval"]:
            print ("polling interval changed from " + str(pollinginterval) + " to " + settings["core"]["pollinginterval"])
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
    main(sys.argv[1:])

