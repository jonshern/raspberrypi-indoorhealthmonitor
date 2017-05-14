import yaml
from sensorconfig import SensorConfig

class IOTConfig(object):
    location = ''
    logfile = ''
    alerts = ''
    pollinginterval = ''
    displaymode = ''
    configuredsensors = dict()
    snsarn = ''

    def __init__(self):
        self.location = ""
        self.logfile = ""
        self.alertsenabled = ""
        self.pollinginterval = ""
        self.displaymode = ""
        self.configuredsensors = dict()
        self.snsarn = ""
        
        



    # def __init__(self, location, logfile, alertsenabled, pollinginterval, displaymode, configuredsensors, snsarn):
    #     self.location = location
    #     self.logfile = logfile
    #     self.alerts = alertsenabled
    #     self.pollinginterval = pollinginterval
    #     self.displaymode = displaymode
    #     self.configuredsensors = configuredsensors
    #     self.snsarn = snsarn

    def initializefromdictionary(self, settings):
        self.location = settings["core"]["location"]
        self.logfile = settings["core"]["logfile"]
        self.alertsenabled = settings["core"]["alertsenabled"]
        self.pollinginterval = settings["core"]["pollinginterval"]
        self.displaymode = settings["core"]["displaymode"]

        for item in settings["core"]["configuredsensors"]:
            sensor = SensorConfig(item['name'], item['port'])
            self.configuredsensors[item['name']] = sensor

    def initializefromfile(self, filename):
        with open(filename, "r") as f:
            settings = yaml.load(f)

        self.initializefromdictionary(settings)






    def isconfigvalid(self, supportedsensors):

        for sensor in self.configuredsensors:
            if sensor not in supportedsensors:
                print "The " + sensor + "sensor is not supported"
                return False

        return True
    