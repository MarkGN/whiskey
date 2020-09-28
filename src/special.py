# This file lists all specials: what they're called, what they do,
# and how they're parametrised.
# There's also a dictionary, so you can check for if a given special
# is being used correctly.

# I call it agent_specials because I mean to add item specials,
# aura specials, etc, in good time

agent_specials = {
    # Does an agent have magic spells
    # There's a +$arg2 bonus if the spell is from $arg1 discipline.
    "magic": None,
    # Do we get +arg1 combat vs every opponent after the first:
    # Conservation of Ninjutsu
    # "ninjutsu": 1,
    # Do we get +$arg1 in the first round of battle
    "quick": 4,
    # Can an agent regenerate during combat
    # Each turn, with probability $arg1,
    # recovers randint(1,$arg2) hit points
    "regenerate": (1.0, 1),
    # If we hit someone, they can't act again for $arg1 rounds
    # They can still defend if attacked
    "stagger": 1,
}

# agent_specials = {hash(k): agent_specials[k] for k in agent_specials.keys()}
