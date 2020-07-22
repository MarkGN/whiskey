import context
import unittest

from test_deck import TestDeck
from test_army import TestArmy

TESTS = [TestArmy, TestDeck]

import sys


def main():
    # """"""
    # suite = unittest.TestSuite()
    # runner = unittest.TextTestRunner()
    # for test in TESTS:
    #     suite.addTest(unittest.makeSuite(test))
    # runner.run(suite)
    print("My sys path is:", sys.path)
    unittest.main()


if __name__ == "__main__":
    main()
