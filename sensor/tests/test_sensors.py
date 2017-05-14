import pytest
from mock import MagicMock, patch
mymodule = MagicMock()

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

import app





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


def test_configsensorvalues(mocker):
    


    mymodule = MagicMock()
    sys.modules["grovepi"] = mymodule


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





    # print str(data.value)



    # mymodule.assert_called_once()


    # for item in config.configuredsensors:
    #     print str(item)
    # assert config.location != ""
    # assert len(config.configuredsensors) > 1

    # for item in config.configuredsensors:
    #     assert item.port != ""
    #     assert item.name != ""




def test_filenametest():
    '''Perform a basic test to see how unit tests show up'''
    assert True

# def test_mockingstuff(mocker):
#     mocker.patch('sensor.Sensor.gettempandhumidity')
#     mocker.patch('sensor.Sensor.readdustsensor')
#     mocker.patch('sensor.Sensor.getloudnessinfo')
#     mocker.patch('sensor.Sensor.getgassensorvalue')
#     mocker.patch('sensor.Sensor.getairqualitysensorvalue'


#     config.pollinginterval = 10
    
#     data = app.getsensordata('loudness', False, config)

#     sensor.Sensor.assert_called_once_with('1')

    


# def test_mockinggrove(mocker):
#     mocker.patch('grovepi.grovepi.analogRead')

