import pytest
import mock
from mock import MagicMock, patch

import sys

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



def test_parampolling():

    args = iothelper.parser_args(['-p', '-sloudness'])

    print str(args)

    assert args['sensortest'] == 'loudness'
    assert args['configfile'] == 'settings.yaml'
    assert args['poll'] == True



def test_paramloudness():
    
    args = iothelper.parser_args(['-sloudness'])

    print str(args)

    assert args['sensortest'] == 'loudness'
    assert args['configfile'] == 'settings.yaml'
    assert args['poll'] == False