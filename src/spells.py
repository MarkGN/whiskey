# This file lists all spells.
# I'm not sure how to implement this well, so for now, I'll just have
# descriptive strings.
# Do I put all the code here, or what? Maybe there are parametrised spells?
# Like, an agent might have blitz 3 and later learn blitz 5.
# Some spells might be variable. D&D has fireball, but no half-fireball;
# this might make sense for some abilities in this system, but not all.

spells = {

    "blitz": "1 mana: gain +3 combat ueot",

    "heal": "1 mana: heal target by up to 3 hp. Can't be cast during battle",

    "leader": "1 mana: up to 4 targets each gain +1 combat ueot",

    "striker": "1 mana: inflict double dmg ueot",

    "tank": "1 mana: gain temporary HP worth 20% of max_hp ueob. Clash with up to 2 enemies ueot",
}

# spells = {hash(k): spells[k] for k in spells.keys()}