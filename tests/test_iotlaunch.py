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
from iotconfig import IOTConfig

import iothelper




@patch.object(IOTConfig, 'initializefromfile')
def test_parameterstest(mocker):

    args = iothelper.parser_args(['-sloudness'])

    iothelper.main(args)


    #mocker.getloudnessinfo.assert_called_once()

