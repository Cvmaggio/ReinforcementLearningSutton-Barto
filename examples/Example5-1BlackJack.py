import random

#Source1: https://stackoverflow.com/questions/24407586/nested-comprehension-in-python-to-generate-a-deck-of-cards

class BlackJack():
    def __init__(self):
        self.deck = self.getFreshDeck()
        self.dHand = []
        self.pHand = []

    def getFreshDeck(self):
        #Source1: adapted from user4322779's answer
        deck = ([(rank) for i in range(4) for rank in [str(n) for n in range(2, 11)] + list('JQKA')])
        random.shuffle(deck)
        return deck

    def dealNewHand(self):
        self.dHand.append(self.deck.pop())
        self.pHand.append(self.deck.pop())
        self.dHand.append(self.deck.pop())
        self.pHand.append(self.deck.pop())
        return [self.dHand,self.pHand]

    def dealNewHandWithReplacement(self):
        self.dHand.append(self.)

    def pHit(self):
        self.pHand.append(self.deck.pop())
        if sum(self.pHand)


blackJack = BlackJack()
print(blackJack.dealNewHand())
print(blackJack.deck)
