import pytest
import sys
import pytest_mock
import mock
import grovepi
sys.path.append('../lib/')
sys.path.append('../')

from sensor import Sensor 
from sensorvalue import SensorValue
from sensorconfig import SensorConfig
from config import Config


# import app
import grovepi





    # @mock.patch('app.grovepi.analogRead')
    
    # def test_tempandhumidity(self, mock_tempandhumidity):
    #     gettempandhumidity('fakesensor')
    #     mock_tempandhumidity.remove.assert_called_with('fakesensor')

    # def test_tempandhumidity(self, mock_analogread):
    #     getloudnessinfo('fakesensor')
    #     mock_tempandhumidity.remove.assert_called_with(4)

def test_configloading():
    settings = Config.loadfile('../settings.yaml')
    assert settings != None
    assert settings["core"] != None 

def test_configsensorvalues():
    settings = Config.loadfile('../settings.yaml')

    config = Config()
    config.initializeconfig(settings)

    # for item in config.configuredsensors:
    #     print str(item)
    assert config.location != ""
    assert len(config.configuredsensors) > 1
    
    for item in config.configuredsensors:
        assert item.port != ""
        assert item.name != ""




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

