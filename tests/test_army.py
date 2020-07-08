import unittest, agent, army

class TestArmy(unittest.TestCase):
	"""docstring for TestArmy"""
	def __init__(self, arg):
		super(TestArmy,unittest.TestCase).__init__()
		a = army.Army([agent.Agent("PC") for in range(7)])
		self.assertEqual(len(a.agents),7)
