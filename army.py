import engine, random

class Army:
	def __init__(self, agents):
		self.agents = agents
		self.dead = []
		self.deck = engine.Deck()

	def __str__(self):
		return "\n, ".join([str(a) for a in self.agents]) + "\n"

	def battle(self, enemy):
	    while self.agents and enemy.agents:
	    	# Decide who will fight who, currently random
	    	random.shuffle(self.agents)
	    	random.shuffle(enemy.agents)
	    	width = min(len(self.agents), len(enemy.agents))
	    	depth = min(2*width, max(len(self.agents), len(enemy.agents)))
	    	outnumber = len(self.agents) > len(enemy.agents)

	    	# Perform combat
	    	for i in range(depth):
	    		# Evenly matched agents can hurt each other ...
	    		if i < width:
	    			self.agents[i].clash(enemy.agents[i], self.deck, True)
	    		# ... whereas unmatched agents can take free potshots at the enemy ...
	    		elif outnumber:
	    			self.agents[i].clash(enemy.agents[i-width], self.deck, False)
	    		# ... or theirs can at ours.
	    		else:
	    			enemy.agents[i].clash(self.agents[i-width], enemy.deck, False)

	    	# Remove dead agents from consideration
	    	# TODO: DRY violation, refactor if possible
	    	self.agents, self.dead = [a for a in self.agents if a.is_alive()], self.dead+[a for a in self.agents if not a.is_alive()]
	        enemy.agents, enemy.dead = [a for a in enemy.agents if a.is_alive()], enemy.dead+[a for a in enemy.agents if not a.is_alive()]

def test():
	wins = 0
	perfect_wins = 0
	num_its = 100
	for j in range(num_its):
		a1 = Army([engine.Agent(engine.agents["PC"]) for i in range(4)])
		# a2 = Army([engine.Agent(engine.agents["heartbreaker"]) for i in range(1)])
		a2 = Army([engine.Agent(engine.agents["swelling"]) for i in range(6)])
		a1.battle(a2)
		if a1.agents:
			wins += 1
			if len(a1.agents) == 4:
				perfect_wins += 1
	print "Wins, flawless wins, runs:", wins, perfect_wins, num_its

test()