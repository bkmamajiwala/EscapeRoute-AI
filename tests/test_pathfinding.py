import unittest
from src.ai_engine import AStar, Dijkstra

class TestPathfinding(unittest.TestCase):

    def setUp(self):
        # Sample graph for testing
        self.graph = {
            'A': {'B': 1, 'C': 4},
            'B': {'A': 1, 'C': 2, 'D': 5},
            'C': {'A': 4, 'B': 2, 'D': 1},
            'D': {'B': 5, 'C': 1}
        }

    def test_a_star(self):
        # Test A* algorithm
        start = 'A'
        goal = 'D'
        path, cost = AStar(self.graph, start, goal)
        self.assertEqual(path, ['A', 'B', 'C', 'D'])
        self.assertEqual(cost, 4)

    def test_dijkstra(self):
        # Test Dijkstra's algorithm
        start = 'A'
        goal = 'D'
        path, cost = Dijkstra(self.graph, start, goal)
        self.assertEqual(path, ['A', 'B', 'C', 'D'])
        self.assertEqual(cost, 4)

    def test_no_path(self):
        # Test case where no path exists
        graph_no_path = {
            'A': {'B': 1},
            'B': {'A': 1},
            'C': {}
        }
        start = 'A'
        goal = 'C'
        path, cost = AStar(graph_no_path, start, goal)
        self.assertEqual(path, [])
        self.assertEqual(cost, float('inf'))

if __name__ == '__main__':
    unittest.main()