import time
import grovepi
import atexit
import json
import sys
import sensorvalue
import argparse
from config import settings
from datetime import datetime



def main():
    
    sensordatafile = getsensorfilename()
    supportedsenors = ['Loudness', 'AirQuality','Light', 'Gas', 'TempAndHumidity']
    



    parser = argparse.ArgumentParser(
    description='Get Sensor Data')
    parser.add_argument(
        '-p', '--poll', help='Poll all sensors in the config file at the configured interval', action='store_true')

    parser.add_argument('-s', '--sensortest', help='Name of the sensor to test', default='nosensor')
    args = vars(parser.parse_args())

    print len(args)

    if args['poll']:
            startautopolling()
    elif args['sensortest'] == 'nosensor':
        print 'Please specify a sensor name'
        print 'supported sensors:'
        print supportedsenors
    elif args['sensortest'] != 'nosensor':
        sensortest(args['sensortest'])
    else:
        print 'No arguments were specified so nothing will be done'
    

    # how do i manage the interval of all of the sensors?
    # i could just set it up as as a chron job and then either write the value to a file or a web service.

    # define ports each sensor will use.

    #get hooked up to analog port
    loudness_sensor_pin = 0

    # Connect the Grove Gas Sensor to analog port A0
    # SIG,NC,VCC,GND
    gas_sensor = 0
    light_sensor = 0 

    location = 'Jons Office'



def sensortest(sensorname):
    print 'Testing the sensor' + sensorname

    if sensorname == "Loudness":
        print getloudnessinfo(1)
    if sensorname == "AirQuality":
        print getairqualitysensorvalue()
    if sensorname == "Gas":
        print getgassensorvalue("something", 1)
    if sensorname == "TempAndHumidity":
        print "Temperature and Humidity"
    if sensorname == "Light":
        print "Light Sensor"




def startautopolling():
    while True:
        getairqualitysensorvalue()
        getgassensorvalue(location, gas_sensor_pin)
        # https://github.com/DexterInd/GrovePi/blob/master/Software/Python/grove_gas_sensor.py



def getsensorfilename():
    return "sensorlog" + datetime.now().strftime('%Y%m%d%H%M%S') + ".log" 


def getloudnessinfo(loudness_sensor_pin):
    try:
        # Read the sound level
        sensor_value = grovepi.analogRead(loudness_sensor)
        sensordata = SensorValue(sensor_value, 'none', 'Loudness', location)
        writetofile(sensordata)
    
    except IOError:
        print ("Error")


def getgassensorvalue(location, gas_sensor_pin):
    
    grovepi.pinMode(gas_sensor_pin,"INPUT")
    try:
        # Get sensor value
        sensor_value = grovepi.analogRead(gas_sensor)

        # Calculate gas density - large value means more dense gas
        density = (float)(sensor_value / 1024)

        print("sensor_value =", sensor_value, " density =", density)
        sensordata = SensorValue(sensor_value, 'none', 'Gas', location)
        writetofile(sensordata)

    except IOError:
        print ("Error")



def getairqualitysensorvalue():
    air_sensor = 0

    grovepi.pinMode(air_sensor,"INPUT")

    while True:
        try:
            # Get sensor value
            sensor_value = grovepi.analogRead(air_sensor)

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

