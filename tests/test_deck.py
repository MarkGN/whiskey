import context
import deck, unittest


class TestDeck(unittest.TestCase):
    def test_size(self):
        d = deck.Deck()
        assert len(d.deck) == 26, "Deck should have 26 cards"
        assert False
