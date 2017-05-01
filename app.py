import time
import grovepi




def main():
    getairqualitysensorvalue()

def gettempandhumidity():
    return 10



def getlightinfo():
    return 10

def getgasinfo():
    return 100


    

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

