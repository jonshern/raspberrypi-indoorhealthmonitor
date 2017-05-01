import time
import grovepi
import atexit
import logger



def main():
    logger = logging.getlogger('indoorhealthmonitor')
    logger.setLevel(logging.DEBUG)

    # create file handler which logs even debug messages
    fh = logging.FileHandler('healthmonitor.log')
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    readdustsensor()


    getairqualitysensorvalue()

def gettempandhumidity():
    return 10



def getlightinfo():
    return 10

def getgasinfo():
    return 100


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

