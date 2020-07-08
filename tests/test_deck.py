import unittest

import deck

class TestDeck(unittest.TestCase):
	def test_init(self):
		super(TestDeck,unittest.TestCase).__init__()
		d = deck.Deck()
		self.assertEqual(len(d.deck),26)
