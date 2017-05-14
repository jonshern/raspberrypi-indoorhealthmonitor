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




@mock.patch('config.Config', autospec=True)
def test_parameterstest(mocker):

    args = iothelper.parser_args(['-sloudness'])

    iothelper.main(args)


    #mocker.getloudnessinfo.assert_called_once()

