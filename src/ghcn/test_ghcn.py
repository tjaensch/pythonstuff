import unittest
from ghcn import GHCN

# Tests
class Testghcn(unittest.TestCase):
    """docstring for Testghcn"""
    def setUp(self):
        ghcn = GHCN()
        self.stationIds = ghcn.getIDs()

    def test_getIDs(self):
        self.assertTrue(len(self.stationIds) > 103000)

# __main__
if __name__ == '__main__':
    unittest.main()
# End __main__