import src.deck as deck, src.agent as agent
import random


class Army:
    def __init__(self, agents):
        self.agents = agents
        self.dead = []
        self.deck = deck.Deck()

    def __str__(self):
        return "\n, ".join([str(a) for a in self.agents]) + "\n"

    # TODO: this entire method is a DRY violation. Refactor if possible.
    # Also, it remains to be seen whether we keep the outnumber mechanic.
    def battle(self, enemy):
        turn_number = 0
        while self.agents and enemy.agents:
            # Decide who will fight who, currently random
            random.shuffle(self.agents)
            random.shuffle(enemy.agents)

            # width: number of clashes
            width = min(len(self.agents), len(enemy.agents))
            # depth: maximum number of agents fighting. No more than one may take
            # potshots at any given opponent.
            depth = min(2 * width, max(len(self.agents), len(enemy.agents)))
            outnumber = len(self.agents) > len(enemy.agents)

            battle_context = Battle_Context(self, enemy, turn_number)
            # Perform combat
            for i in range(depth):
                # Evenly matched agents can hurt each other ...
                s_agent = self.agents[i % len(self.agents)]
                e_agent = enemy.agents[i % len(enemy.agents)]
                if i < width:
                    # There's a mathematically interesting phenomenon,
                    # if we don't randomise,
                    # wherein the defender has a statistical edge.
                    # If self wins early, it's already used its good cards and so
                    # it fails its free attacks;
                    # whereas if it loses early, enemy has a fresh deck and its
                    # free attacks can hit just fine.
                    if random.randint(0, 1):
                        s_agent.clash(e_agent, self.deck, True, battle_context)
                    else:
                        e_agent.clash(s_agent, self.deck, True, battle_context)

                # ... whereas unmatched agents can take free potshots at the enemy ...
                elif outnumber:
                    if s_agent.has_special("magic") and s_agent.get_mp() > 0:
                        s_agent.cast_spell(self, enemy)
                    else:
                        s_agent.clash(
                            enemy.agents[i - width], self.deck, False, battle_context
                        )
                # ... or theirs can at ours.
                else:
                    if e_agent.has_special("magic") and e_agent.get_mp() > 0:
                        e_agent.cast_spell(enemy, self)
                    else:
                        e_agent.clash(
                            self.agents[i - width], enemy.deck, False, battle_context
                        )

            # Remove dead agents from consideration
            self.agents, self.dead = (
                [a for a in self.agents if a.is_alive()],
                self.dead + [a for a in self.agents if not a.is_alive()],
            )
            enemy.agents, enemy.dead = (
                [a for a in enemy.agents if a.is_alive()],
                enemy.dead + [a for a in enemy.agents if not a.is_alive()],
            )
            for a in self.agents + enemy.agents:
                if a.has_special("regenerate"):
                    p, n = a.get_special("regenerate")
                    if random.random() < p:
                        a.recover_hp(random.randint(1, n))
            turn_number += 1


class Battle_Context:
    def __init__(self, own_army, enemy_army, turn_number):
        self.own_army = own_army
        self.enemy_army = enemy_army
        self.turn_number = turn_number


def simulate(army1_func, army2_func, its):
    wins = 0
    perfect_wins = 0
    for _ in range(its):
        a1 = army1_func()
        a1_size = len(a1.agents)
        a2 = army2_func()
        a1.battle(a2)
        if a1.agents:
            wins += 1
            if len(a1.agents) == a1_size:
                perfect_wins += 1
    print("Wins, flawless wins, runs:", wins, perfect_wins, its)


if __name__ == "__main__":
    simulate(
        lambda: Army([agent.Agent("PC") for i in range(4)]),
        lambda: Army(
            [agent.Agent("tank minion") for i in range(8)]
            + [agent.Agent("caster minion") for i in range(6)]
        ),
        100,
    )
