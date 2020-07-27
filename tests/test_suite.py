# import context
import unittest

import tests.test_deck
import tests.test_army

TESTS = [tests.test_deck.TestDeck, tests.test_army.TestArmy]

import sys


def main():
    """"""
    unittest.main()


if __name__ == "__main__":
    main()
