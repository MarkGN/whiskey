# A module for running simulations of my Whiskey TT RPG system, intended for design and playtesting
import copy, json, random, special


class Agent:

    # load agents
    # TODO make it possible to load from multiple different lists, to permit multiple balances
    f = open("./agent.json")
    agent_types = json.load(f)

    def __init__(self, agent_type=None):

        # TODO: could we cut half of this and have the entire statblock just be agent_json?
        agent_json = copy.deepcopy(Agent.agent_types[agent_type])
        self._combat = agent_json["combat"]
        self._dmg = agent_json["damage"]
        self._max_hp = self._hp = agent_json["hp"]
        if "special" in agent_json.keys():
            _special = agent_json["special"]
            for k in _special.keys():
                if _special[k] == {}:
                    try:
                        _special[k] = special.agent_specials[hash(k)]
                    except:
                        raise Exception("Failed to parse special called " + k)
                        # _special.pop(k,None)
            self._special = {hash(k): _special[k] for k in _special.keys()}
        else:
            self._special = {}
        if "mp" in agent_json.keys():
            self._mp = agent_json["mp"]
        else:
            self._mp = 0

        traits = ["strong", "nimble", "tough"]
        if self.has_special("magic"):
            traits += ["fey"]
        self._traits = random.sample(traits, 1)

        for trait in self._traits:
            if trait == "fey":
                # possibly also empower spells somehow?
                self._mp += (self._mp + 2) // 5
            elif trait == "nimble":
                self._combat += 1
            elif trait == "strong":
                expected_dmg = (
                    self._dmg["fixed"] + sum((d - 1 for d in self._dmg["mod"])) // 2
                )
                self._dmg["fixed"] += expected_dmg // 5
                if expected_dmg % 5 >= 2 and self._dmg["mod"]:
                    self._dmg["mod"][-1] += 1
            elif trait == "tough":
                self._hp += (self._hp + 2) // 5

    def __str__(self):
        return "Agent: " + str((self._traits[0], self._hp))

    def get_combat(self):
        return self._combat

    def get_hp(self):
        return self._hp

    def set_hp(self, hp):
        self._hp = hp

    def get_mp(self):
        return self._mp

    def set_mp(self, mp):
        self._mp = mp

    def has_special(self, special):
        return hash(special) in self._special.keys()

    def get_special(self, special):
        if self.has_special(special):
            return self._special[hash(special)]
        else:
            return None

    def harm(self, damage):
        if damage > 0:
            self.set_hp(self.get_hp() - damage)

    def recover_hp(self, hp):
        if hp > 0:
            self.set_hp(min(self._max_hp, self.get_hp() + hp))

    def is_alive(self):
        return self._hp > 0

    def hit(self, enemy, check_value):
        dmg = self._dmg["fixed"] + sum([check_value % mod for mod in self._dmg["mod"]])
        enemy.harm(dmg)

    # returns a success/fail and the card value
    def check(self, target, deck):
        v = deck.reveal().value()
        vs = v + self.get_combat()
        if v >= 24:
            hit = True
        elif v <= 3:
            hit = False
        else:
            hit = vs > target + 13
        return (hit, vs if hit else 27 - v + self.get_combat())

    # duel :: is it a duel, ie can the enemy fight back enough to land a hit
    def clash(self, enemy, deck, duel=True):
        (t, check_value) = self.check(enemy.get_combat(), deck)
        if t:
            winner, loser = self, enemy
        else:
            winner, loser = enemy, self
        if t or duel or winner.has_special("choreo"):
            winner.hit(loser, check_value)

    # This is dummy spell code to test functionality
    def cast_spell(self, army, enemy_army):
        self.set_mp(self.get_mp() - 1)

    # Available actions are clash; snipe; and cast.
    # TODO
    def choose_action(self, army, enemy):
        return "clash"
