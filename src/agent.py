# A module for running simulations of my Whiskey TT RPG system, intended for design and playtesting
import copy, json, random

class Agent:

    global agent_types
    # load agents
    # TODO make it possible to load from multiple different lists, to permit multiple balances
    f = file("./agent.json")
    agent_types = json.load(f)


    def __init__(self,agent_type=None):

        # TODO: could we cut half of this and have the entire statblock just be j?
        agent_json = copy.deepcopy(agent_types[agent_type])
        self._combat = agent_json["combat"]
        self._dmg = agent_json["damage"]
        self._hp = agent_json["hp"]
        if "special" in agent_json.keys():
            self._special = set(agent_json["special"])
        else:
            self._special={}
        if "mana" in agent_json.keys():
            self._mana = agent_json["mana"]
        else:
            self._mana=0

        traits = ["strong", "nimble", "tough"]
        self._traits = random.sample(traits,1)

        # TODO strong should surely vary depending on base stats,
        # viz 1/5 of expected base damage, to put it in line with the others.
        for trait in self._traits:
            if trait=="nimble":
                self._combat += 1
            elif trait=="strong":
                expected_dmg = self._dmg["fixed"] + sum((d-1 for d in self._dmg["mod"]))//2
                self._dmg["fixed"] += (expected_dmg+2)//5
            elif trait=="tough":
                self._hp += (self._hp + 2) // 5

    def __str__(self):
        return "Agent: " + str((self._traits[0],self._hp))

    def get_combat(self):
        return self._combat

    def get_hp(self):
        return self._hp

    def set_hp(self, hp):
        self._hp = hp

    def get_mana(self):
        return self._mana

    def set_mana(self, mp):
        self._mana = mp

    def has_special(self,special):
        return special in self._special

    def harm(self, damage):
        self.set_hp(self.get_hp() - damage)

    def is_alive(self):
        return self._hp > 0

    def hit(self, enemy, check_value):
        dmg = self._dmg["fixed"] + sum([check_value%mod for mod in self._dmg["mod"]])
        enemy.harm(dmg)

    # returns a success/fail and the card value
    # TODO, if this is generalised beyond a combat engine: allow the use of other stats than combat
    def check(self, target, deck):
        v = deck.reveal().value()
        vs = v+self.get_combat()
        if v >= 24:
            hit = True
        elif v <= 3:
            hit = False
        else:
            hit = vs > target + 13
        return (hit, vs if hit else 27-v+self.get_combat())


    # duel: is it a duel, ie can the enemy fight back enough to land a hit
    def clash(self, enemy, deck, duel=True):
        (t,check_value) = self.check(enemy.get_combat(), deck)
        if t:
            winner,loser = self,enemy
        else:
            winner,loser = enemy,self
        if duel or t or winner.has_special("choreo"):
            winner.hit(loser, check_value)

    # This is a really dumb dummy spell to test functionality
    def cast_spell(self, army, enemy_army):
        # print "magic is happening!"
        self.set_mana(self.get_mana() - 1)
        for agent in army.agents:
            agent._combat += 1