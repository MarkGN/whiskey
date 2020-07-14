import context
import unittest

from test_deck import TestDeck
from test_army import TestArmy

TESTS = [TestArmy, TestDeck]


def main():
    # """"""
    # suite = unittest.TestSuite()
    # runner = unittest.TextTestRunner()
    # for test in TESTS:
    #     suite.addTest(unittest.makeSuite(test))
    # runner.run(suite)
    unittest.main()


if __name__ == "__main__":
    main()
