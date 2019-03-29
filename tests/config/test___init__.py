import os
import tempfile
import unittest

from src.config import AppConfig


class TestConfigReader(unittest.TestCase):
    def setUp(self):
        self.goodpath = tempfile.mkstemp(suffix='.ini')[1]
        self.badpath = tempfile.mkstemp(suffix='.ini')[1]
        with open(self.goodpath, 'w') as goodconf:
            goodconf.write('[kadebot]\napi_key = somekey:thatworks\n')
        with open(self.badpath, 'w') as badconf:
            badconf.write('[kadebot]\napikey = somekey:thatworks\n')

    def tearDown(self):
        if os.path.exists(self.goodpath):
            os.remove(self.goodpath)
        if os.path.exists(self.badpath):
            os.remove(self.badpath)

    def test_valid(self):
        config = AppConfig(self.goodpath)
        assert config.valid

    def test_invalid(self):
        config = AppConfig(self.badpath)
        assert not config.valid


if __name__ == '__main__':
    unittest.main()
