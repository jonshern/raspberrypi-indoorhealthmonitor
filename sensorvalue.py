from datetime import datetime
import datetime
import yaml

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
        return self.location + "," + self.sensor + "," + str(self.timestamp) + "," + str(self.value) + "," + self.unit 
    
    def yaml(self):
        return yaml.dump(self.__dict__)

    # @staticmethod
    # def load(data):
    #    values = yaml.safe_load(data)
    #    return SensorValue(values["sensor"], values["value"], values["timestamp"], values["unit"], values["location"])
    