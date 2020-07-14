import unittest, agent, army


class TestArmy(unittest.TestCase):
    def test_size(self):
        a = army.Army([agent.Agent("PC") for _ in range(7)])
        self.assertEqual(len(a.agents), 7)
        