import pytest
import mock
from mock import MagicMock, patch
mymodule = MagicMock(return_value = 3)

import sys
sys.modules["grovepi"] = mymodule

import pytest_mock
import mock
import grovepi
import unittest


sys.path.append('../lib/')
sys.path.append('../')

from sensor import Sensor 
from sensorvalue import SensorValue
from sensorconfig import SensorConfig
from config import Config

import iothelper





# Running Tests
# Run this command pytest --capture=no  
# This will also show the print statements




# def test_configloading():
#     settings = Config.loadfile('../settings.yaml')
#     assert settings != None
#     assert settings["core"] != None 

# def test_configsensorvalues():
#     settings = Config.loadfile('../settings.yaml')

#     config = Config()
#     config.initializeconfig(settings)

#     # for item in config.configuredsensors:
#     #     print str(item)
#     assert config.location != ""
#     assert len(config.configuredsensors) > 1

#     for item in config.configuredsensors:
#         assert item.port != ""
#         assert item.name != ""


@mock.patch('sensor.Sensor', autospec=True)
def test_correctsensorgetscalled(mocker):
    
    settings = Config.loadfile('../settings.yaml')

    config = Config()
    config.initializeconfig(settings)
    data = iothelper.getsensordata("loudness", False, config)

    #mocker.getloudnessinfo.assert_called_once()



def test_configsensorvalues(mocker):
    
    settings = Config.loadfile('../settings.yaml')

    config = Config()
    config.initializeconfig(settings)


    print "port " + str(config.configuredsensors['loudness'].port)
    print "port " + str(config.configuredsensors['loudness'].name)

 
    assert config.configuredsensors['loudness'].port == 1
    sensor = Sensor(config)

    data = sensor.getloudnessinfo(config)

    assert data != None

    for item in data:
        print "Sensor value: " + str(item.value)



def test_filenametest():
    '''Perform a basic test to see how unit tests show up'''
    assert True

