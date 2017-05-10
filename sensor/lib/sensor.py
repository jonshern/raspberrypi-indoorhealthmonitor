import time
import grovepi
import atexit

from sensorvalue import SensorValue
from sensorconfig import SensorConfig

class Sensor(object):
    sensorconfig = ''

    def __init__(self, config):
        self.sensorconfig = config




    def readdustsensor(self, sensorname):
        
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

    def gettempandhumidity(self, sensorname):
        
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
        

    def getloudnessinfo(self, sensorname):
        
        sensordata = []
        pin = getsensorconfig(sensorname)
        try:
            # Read the sound level
            sensor_value = grovepi.analogRead(pin)
            sensordata.append(SensorValue(sensor_value, 'none', 'Loudness', 'location'))
        
        except IOError:
            print ("Error")
        
        return sensordata


    def getgassensorvalue(self, sensorname):
        
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


    def getairqualitysensorvalue(self, sensorname):
        
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


