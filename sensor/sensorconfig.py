

class SensorConfig(object):
    location = ''
    logfile = ''
    alerts = ''
    pollinginterval = ''
    displaymode = ''
    configuredsensors = []
    snsarn = ''


    def __init__(self, settings):
        self.location = settings["core"]["location"]
        self.logfile = settings["core"]["logfile"]
        self.alertsenabled = settings["core"]["alertsenabled"]
        self.pollinginterval = settings["core"]["pollinginterval"]
        self.displaymode = settings["core"]["displaymode"]
        self.configuredsensors = settings["core"]["configuredsensors"]
        self.snsarn = settings["core"]["snsarn"]


    def isconfigvalid(self, supportedsensors):

        for sensor in self.configuredsensors:
            if sensor not in supportedsensors:
                print "The " + sensor + "sensor is not supported"
                return False

        return True
    