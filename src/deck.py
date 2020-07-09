import random


class Card:
    def __init__(self, rank):
        self.rank = rank

    def value(self):
        return self.rank


class Deck:
    def __init__(self):
        self.deck = [Card(rank) for rank in (range(1, 27))]
        random.shuffle(self.deck)
        self.discard = []

    def reveal(self):
        with_replacement = False
        if with_replacement:
            return Card(random.randint(1, 26))
        c = self.deck.pop()
        self.discard.append(c)
        # We can shuffle early with viz [[ if len(self.deck) < k ]]
        if not self.deck:
            self.deck, self.discard = self.deck + self.discard, []
            random.shuffle(self.deck)
        return c
