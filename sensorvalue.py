from datetime import datetime
import datetime

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