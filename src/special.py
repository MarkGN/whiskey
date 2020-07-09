# This file lists all specials: what they're called, what they do,
# and how they're parametrised.
# There's also a dictionary, so you can check for if a given special
# is being used correctly.

agent_specials = {
    # If an agent is attacked other than during a clash, can it counter,
    # as with a choreographed fight scene
    # Can counter up to arg1 enemies
    "choreo": 1,
    # Does an agent have magic spells
    # There's a bonus if the spell is from arg1 discipline.
    "magic": None,
    # Can an agent regenerate during combat
    # Each turn, with probability arg1,
    # recovers randint(1,arg2) hp
    "regenerate": (1.0, 1),
}

agent_specials = {hash(k): agent_specials[k] for k in agent_specials.keys()}
