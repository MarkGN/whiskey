# Methods and data pertaining to individual agents
import copy, json, random
import src.special as special


class Agent:

    combat = hash("combat")
    damage_base = hash("damage_base")
    damage_die = hash("damage_die")
    hp = hash("hp")
    mp = hash("mp")

    # load agents
    # TODO make it possible to load from multiple different lists, to permit multiple balances
    f = open("data/agent.json")
    agent_types = json.load(f)
    # In a complete game, there'd be noncombat traits too
    generic_traits = ["nimble", "obsessive", "quick", "strong", "tough"]

    def __init__(self, agent_type=None):

        # TODO: change all the getter/setters to get_stat(self, stat, ?value, ?diff)
        agent_json = copy.deepcopy(Agent.agent_types[agent_type])
        self.stats=self.max_stats={}
        for stat in agent_json["stats"]:
            self.max_stats[stat] = self.stats[stat] = agent_json["stats"][stat]
        if "special" in agent_json.keys():
            _special = agent_json["special"]
            for k in _special.keys():
                if _special[k] == {}:
                    try:
                        _special[k] = special.agent_specials[k]
                    except:
                        _special.pop(k,None)
                        raise Exception("Failed to parse special called " + k)
            self._special = {hash(k): _special[k] for k in _special.keys()}
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
                self.set_stat(Agent.combat, 1, True)
            elif trait == "quick":
                self._special["quick"] = obsess * special.agent_specials["quick"]
            elif trait == "strong":
                # Note: currently unbalanced: does not scale
                self.set_stat(Agent.damage_base, obsess*self.expected_dmg()*2//7)
            elif trait == "tough":
                self.set_stat(Agent.hp, obsess * (self.get_stat(Agent.hp) + 2) // 5 )
            if trait != "obsess":
                # If we have >= 3 traits and one is obsessive, only the first is doubled
                obsess = 1

    def __str__(self):
        return "Agent: " + str((self._traits, self.get_stat(Agent.hp)))
    
    def get_stat(self, stat, battle_context=None):
        if stat == Agent.combat:
            if battle_context and (battle_context.turn_number == 0) and self.get_special("quick", 0):
                return self.stats[Agent.combat] + self.get_special(hash("quick"))
        return self.stats[stat]
    
    def set_stat(self, stat, value, diff=False):
        if diff:
            self.stats[stat] += value
            self.max_stats[stat] += value
        else:
            self.stats[stat] = value
            self.max_stats[stat] = value

    # eg losing HP or MP, stat drain or bolster
    # TODO make it so that this can't erase bonus HP when clamped
    def set_temp_stat(self, stat, value, diff=False, clamped=False):
        if diff:
            self.stats[stat] += value
        else:
            self.stats[stat] = value
        if clamped:
            self.stats[stat] = min(self.max_stats[stat], max(0, self.stats[stat]))
    
    def pay_stat(self, stat, value):
        if self.get_stat(stat) < value:
            return False
        else:
            self.set_temp_stat(self, stat, -value, True)
            return True

    def has_special(self, special):
        return special in self._special.keys()

    def get_special(self, special, null=None):
        if self.has_special(special):
            return self._special[special]
        else:
            return null

    def harm(self, damage):
        if damage > 0:
            self.set_temp_stat(Agent.hp, -damage, True)

    def recover_hp(self, hp):
        if hp > 0:
            self.set_temp_stat(Agent.hp, hp, True, True)

    def expected_dmg(self):
        return self.get_stat(Agent.damage_base) + 7*self.get_stat(Agent.damage_die)//2

    def is_alive(self):
        return self.get_stat(Agent.hp) > 0

    def hit(self, enemy, check_value):
        dmg = self.get_stat(Agent.damage_base) + check_value * self.get_stat(Agent.damage_die)
        enemy.harm(dmg)

    # returns a success/fail and a die value
    def check(self, target, battle_context, deck):
        return (self.get_stat(Agent.combat, battle_context) + deck.reveal().value() > target, random.randint(1,6))

    def clash(self, enemy, deck, battle_context):
        (t, check_value) = self.check(
            enemy.get_combat(battle_context), battle_context, deck
        )
        if t:
            winner, loser = self, enemy
        else:
            winner, loser = enemy, self
        winner.hit(loser, check_value)

    # This is dummy spell code to test functionality
    def cast_spell(self, battle_context):
        self.set_temp_stat(Agent.mp, -1, True)

    # Actions include advance, stand ground, defend, and cast a spell while doing any of the above
    # TODO
    def choose_action(self, battle_context):
        return "none"

    # A challenge rating type heuristic. May not work for extreme values; ignores specials
    def power_level(self):
        return 1.2 ** self.get_stat(Agent.combat) * self.get_stat(Agent.hp) * self.expected_dmg()
