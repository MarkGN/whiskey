# This file lists all specials: what they're called, what they do,
# and how they're parametrised.
# There's also a dictionary, so you can check for if a given special
# is being used correctly.

# I call it agent_specials because I mean to add item specials,
# aura specials, etc, in good time

agent_specials = {
    # If an agent is attacked other than during a clash, can it counter,
    # as with a choreographed fight scene
    # NB: this is deprecated with multiclash rules
    # TODO: consider changing such that we instead get +combat
    # when 1v2-ing? Kind of ridiculous, but I need a tank special.
    # Can counter up to $arg1 enemies
    "choreo": 1,
    # Do we get +arg1 combat and +arg2 damage when 2v1-ing an enemy
    # NB: this is an attempted striker ability. Interpret as "easier to
    # win the fight if the enemy is busy"
    # "flanker": (3, (0, [2])),
    # Can we absorb up to $arg1 damage to allies per round
    # NB: this is an attempted tank ability, but hmm.
    # "lifelink": 5,
    # Does an agent have magic spells
    # There's a bonus if the spell is from $arg1 discipline.
    "magic": None,
    # Do we get +$arg1 in the first round of battle
    "quick": 4,
    # Can an agent regenerate during combat
    # Each turn, with probability $arg1,
    # recovers randint(1,$arg2) hit points
    "regenerate": (1.0, 1),
}

# agent_specials = {hash(k): agent_specials[k] for k in agent_specials.keys()}
