import names, random

def d6():
    return random.randint(1,6)

class Character():

    hobbies = [["painting/drawing", "writing", "modelling", "dance/gymnastics", "music", "photography"], ["adopting cats", "cooking", "gardening", "knitting", "mechanical/computer maintenance", "yoga"],["celebrity gossip", "literature", "memes", "music", "movies/TV", "video games"], ["science", "history", "foreign languages", "literature", "music", "programming"], ["bicycling", "tennis/baseball", "soccer/basketball", "martial arts", "running/swimming", "dance/gymnastics"], ["travel", "Japanese tea ceremony", "conspiracy theories", "politics", "TTRPGs", "urban legends"]]

    def __init__(self, age=None, surname=None):
        self.hobbies = [Character.hobbies[d6()-1][d6()-1] for _ in range(random.randint(2,3))]
        ns = names.get_full_name()
        self.first_name = ns.split()[0]
        self.surname = surname if surname else ns.split()[1]
        self.age = age if age else 12
        hexaco_ixes = random.sample(range(6),random.randint(2,4))
        hexaco = "hexaco"
        self.hexaco = "".join([hexaco[i].upper() if i in hexaco_ixes else hexaco[i] for i in range(6)])
    
def create_family(number=None):
    num_members = number if number else max(d6(),d6())
    ages = [12, 36, 10, 39, 15, 17]
    name = names.get_last_name()
    return {Character(age=ages[i], surname=name) for i in range(num_members)}
        
fam = create_family()
print()
for c in fam:
    print(c.first_name, c.surname, c.hobbies, c.age, c.hexaco)
