import mock
import unittest


from app import gettempandhumidity 
from app import getloudnessinfo

class SensorTestCase(unittest.TestCase):
    
    @mock.patch('app.grovepi.analogRead')
    
    # def test_tempandhumidity(self, mock_tempandhumidity):
    #     gettempandhumidity('fakesensor')
    #     mock_tempandhumidity.remove.assert_called_with('fakesensor')

    def test_tempandhumidity(self, mock_analogread):
        getloudnessinfo('fakesensor')
        mock_tempandhumidity.remove.assert_called_with(4)
