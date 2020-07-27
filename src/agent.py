# Methods and data pertaining to individual agents == characters
import copy, json, random
import src.special as special


class Agent:

    # load agents
    # TODO make it possible to load from multiple different lists, to permit multiple balances
    # TODO make this work locally, not just from the test suite
    # import os, sys
    # sys.path.insert(1, os.path.join(sys.path[0], "../data"))
    f = open("data/agent.json")
    agent_types = json.load(f)
    # In a complete game, there'd be noncombat traits too
    # I have about enough to give characters 2, and add Obsessive
    generic_traits = ["nimble", "obsessive", "quick", "strong", "tough"]

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
                        _special[k] = special.agent_specials[k]
                    except:
                        raise Exception("Failed to parse special called " + k)
                        # _special.pop(k,None)
            # self._special = {hash(k): _special[k] for k in _special.keys()}
            self._special = _special
        else:
            self._special = {}
        if "mp" in agent_json.keys():
            self._mp = agent_json["mp"]
        else:
            self._mp = 0

        # Traits typically improve some major trait by 20% or equivalent
        traits = Agent.generic_traits
        if self.has_special("magic"):
            traits = Agent.generic_traits + ["fey"]
        self._traits = random.sample(traits, 2)
        if "obsessive" in self._traits:
            # Obsessive doubles the effect of one other trait
            obsess = 2
        else:
            obsess = 1
        for trait in self._traits:
            if trait == "fey":
                # possibly also empower spells somehow?
                self._mp += obsess * (self._mp + 2) // 5
            elif trait == "nimble":
                self._combat += obsess
            elif trait == "quick":
                self._special["quick"] = obsess * special.agent_specials["quick"]
            elif trait == "strong":
                e = self.expected_dmg()
                self._dmg["fixed"] += obsess * e // 5
                if (obsess * e) % 5 >= 2:
                    if self._dmg["mod"]:
                        self._dmg["mod"][-1] += obsess
                    else:
                        self._dmg["mod"] = [1 + obsess]
            elif trait == "tough":
                self._hp += obsess * (self._hp + 2) // 5
            if trait != "obsess":
                # If we have >= 3 traits and one is obsessive, only the first is doubled
                obsess = 1

    def __str__(self):
        return "Agent: " + str((self._traits[0], self._hp))

    def get_combat(self, battle_context):
        speed = (battle_context.turn_number == 0) and self.get_special("quick", 0)
        return self._combat + speed

    def get_hp(self):
        return self._hp

    def set_hp(self, hp):
        self._hp = hp

    def get_mp(self):
        return self._mp

    def set_mp(self, mp):
        self._mp = mp

    def has_special(self, special):
        return special in self._special.keys()

    def get_special(self, special, null=None):
        if self.has_special(special):
            return self._special[special]
        else:
            return null

    def harm(self, damage):
        if damage > 0:
            self.set_hp(self.get_hp() - damage)

    def recover_hp(self, hp):
        if hp > 0:
            self.set_hp(min(self._max_hp, self.get_hp() + hp))

    def expected_dmg(self):
        return self._dmg["fixed"] + sum((d - 1 for d in self._dmg["mod"])) // 2

    def is_alive(self):
        return self._hp > 0

    def hit(self, enemy, check_value):
        dmg = self._dmg["fixed"] + sum([check_value % mod for mod in self._dmg["mod"]])
        enemy.harm(dmg)

    # returns a success/fail and the card value
    def check(self, target, battle_context, deck):
        v = deck.reveal().value()
        vs = v + self.get_combat(battle_context)
        if v >= 26:
            hit = True
        elif v <= 1:
            hit = False
        else:
            hit = vs > target + 13
        # This method is slightly fairer
        # return (hit, vs if hit else 27 - v + self.get_combat(battle_context))
        # This method is much easier mental arithmetic
        return (hit, vs)

    # duel :: is it a duel, ie can the enemy fight back enough to land a hit
    # Note that I'm considering cutting/amending the duel mechanic, as the current form is
    # arguably un-fun.
    def clash(self, enemy, deck, duel, battle_context):
        (t, check_value) = self.check(
            enemy.get_combat(battle_context), battle_context, deck
        )
        if t:
            winner, loser = self, enemy
        else:
            winner, loser = enemy, self
        if t or duel or winner.has_special("choreo"):
            winner.hit(loser, check_value)

    # This is dummy spell code to test functionality
    def cast_spell(self, army, enemy_army):
        self.set_mp(self.get_mp() - 1)

    # Actions include charge, defend, and cast
    # TODO
    def choose_action(self, army, enemy):
        return "none"

    # A lazy challenge rating type heuristic. May not work for extreme values; ignores specials
    def power_level(self):
        return (
            1.2 ** self._combat
            * self.get_hp()
            * (2 * self._dmg["base"] + sum(m - 1 for m in self._dmg["mod"]))
        )
