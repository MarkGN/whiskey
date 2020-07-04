# A module for running simulations of my Whiskey TT RPG system, intended for design and playtesting
import copy, json, random

class Card:
    def __init__(self,rank):
        self.rank=rank

    def value(self):
        return self.rank

global deck
deck = [Card(rank) for rank in (range(1,27))]
random.shuffle(deck)
global discard
discard = []

def reveal():
    if True:
        return Card(random.randint(1,26))
    global deck, discard
    c = deck.pop()
    discard.append(c)
    if not deck:
        deck, discard = deck + discard, []
        random.shuffle(deck)
    return c

# returns a success/fail and the card value
def check(skill, target):
    v = reveal().value()
    vs = v+skill
    if v >= 24:
        return (True, vs)
    elif v <= 3:
        return (False, vs)
    else:
        return (vs > target+13, vs)

class Agent:
    global traits
    traits = ["strong", "nimble", "tough"]

    def __init__(self,trait=None,combat=10, dmg={"fixed":1,"mod":[5]}, hp=8, json_ix=None):
        self._special={}
        if json_ix:
            j = copy.deepcopy(json_ix)
            self._combat = j["combat"]
            self._dmg = j["damage"]
            self._hp = j["hp"]
            if "special" in j.keys():
                self.special = set(j["special"])
        else:
            self._combat=combat
            self._dmg=dmg
            self._hp=hp
        self._traits = [trait] if trait else random.sample(traits,1)
        for trait in self._traits:
            if trait=="nimble":
                self._combat += 1
            elif trait=="strong":
                self._dmg["fixed"] += 1
            elif trait=="tough":
                self._hp += 3

    def __str__(self):
        return "Agent: " + str((self._traits[0],self._combat,self._dmg,self._hp))

    def get_combat(self):
        return self._combat

    def has_special(self,special):
        return special in self._special

    def harm(self, damage):
        self._hp -= damage

    def is_alive(self):
        return self._hp > 0

    def hit(self, enemy, check_value):
        dmg = self._dmg["fixed"] + sum([check_value%mod for mod in self._dmg["mod"]])
        enemy.harm(dmg)

    #TODO Give Agents an alignment, and draw from their side's deck
    def clash(self, enemy, duel=True):
        (t,check_value) = check(self.get_combat(), enemy.get_combat())
        if t:
            winner,loser = self,enemy
        else:
            winner,loser = enemy,self
        if duel or t or winner.has_special("choreo"):
            true_check_value = check_value if t else 27-check_value+self.get_combat()+enemy.get_combat()
            winner.hit(loser, true_check_value)

# load enemies
f = file("./agent.json")
agents = json.load(f)

#TODO After I implement 2 decks, make each draw from the correct one.
def battle(army1, army2):
    ar1,ar2=army1,army2
    global deck
    while ar1 and ar2:
        if len(ar1) == len(ar2):
            (a1,a2) = (ar1,ar2) if random.randint(0,1) else (ar2,ar1)
        elif len(ar1) >= len(ar2):
            a1,a2 = ar1,ar2
        else:
            a1,a2 = ar2,ar1
        width = len(a2)
        for i in range(width):
            ar1[i].clash(ar2[i])
            if i+width<len(a1):
                a1[i+width].clash(a2[i],False)
        ar1 = [a for a in ar1 if a.is_alive()]
        ar2 = [a for a in ar2 if a.is_alive()]
        random.shuffle(ar1)
        random.shuffle(ar2)
    if not ar1 and not ar2:
        print "WTF, both armies got wiped", army1, army2
    return ar1,ar2

def test1():
    a, b = Agent(), Agent()
    a.clash(b)
    a.clash(b)
    print a,b

def test2():
    wins = 0
    perfect_wins = 0
    for i in range(1000):
        a1 = [Agent(json=agents["PC"]) for i in range(4)]
        a2 = [Agent(json=agents["heartbreaker"]) for i in range(1)]

        a1,a2=battle(a1,a2)
        if a1:
            wins += 1
        if len(a1)==4:
            perfect_wins += 1
    print wins, perfect_wins
    for a in a1:
        print a

def test3():
    wins = 0
    perfect_wins = 0
    for i in range(100):
        a1 = [Agent(json_ix=agents["PC"]) for i in range(4)]
        a2 = [Agent(json_ix=agents["heartbreaker"]) for i in range(1)]
        # a2 = [Agent(json_ix=agents["swelling"]) for i in range(3)]+[Agent(json_ix=agents["endocarditis"]) for i in range(3)]
        a3,a4=battle(a1,a2)
        if a3:
            wins += 1
        else:
            print "heroes"
            for a in a1:
                print a
            print "villains"
            for a in a2:
                print a
        if len(a3)==4:
            perfect_wins += 1
    print wins, perfect_wins



test3()
