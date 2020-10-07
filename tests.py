import unittest
import game
import numpy as np
import constants as const


class TestGameMethods(unittest.TestCase):
    def test__get_all_neighbors(self):
        g = game.Game()
        self.assertEqual(set(g._get_all_neighbors(1, 1)), {(1, 0), (2, 0), (0, 1), (2, 1), (0, 2), (1, 2)})
        self.assertEqual(set(g._get_all_neighbors(0, g.board_size - 1)),
                         {(0, g.board_size - 2), (1, g.board_size - 2), (1, g.board_size - 1)})
        self.assertEqual(set(g._get_all_neighbors(g.board_size - 1, 0)), {(g.board_size - 2, 0),
                                                                          (g.board_size - 2, 1), (10, 1)})
        self.assertEqual(set(g._get_all_neighbors(0, 0)), {(1, 0), (0, 1)})
        self.assertEqual(set(g._get_all_neighbors(g.board_size - 1, g.board_size - 1)),
                         {(g.board_size - 1, g.board_size - 2), (g.board_size - 2, g.board_size - 1)})
        self.assertEqual(set(g._get_all_neighbors(1, 0)), {(0, 0), (0, 1), (1, 1), (2, 0)})

    def test__get_neighbors_by_color(self):
        g = game.Game()
        g.board[0][1] = const.RED
        g.board[1][0] = const.RED
        g.board[1][1] = const.RED
        g.board[2][0] = const.BLUE
        g.board[2][1] = const.BLUE

        self.assertEqual(set(g._get_neighbors_by_color(1, 1, const.BLUE)), {(2, 0), (2, 1)})
        self.assertEqual(set(g._get_neighbors_by_color(0, 0, const.RED)), {(1, 0), (0, 1)})
        self.assertEqual(set(g._get_neighbors_by_color(3, 3, const.BLUE)), set())

    def test_has_won(self):
        pass

    def test_make_move(self):
        g = game.Game()
        g.board[0][0] = const.RED
        self.assertEqual(g.make_move(0, 0, const.RED), False)
        self.assertEqual(g.make_move(0, 0, const.BLUE), False)
        self.assertEqual(g.make_move(0, 1, const.BLUE), True)
        self.assertEqual(g.make_move(0, 1, const.RED), False)
        self.assertEqual(g.make_move(1, 0, const.RED), True)

    def test_is_empty(self):
        g = game.Game()
        g.board[0][0] = const.RED
        self.assertEqual(g.is_empty(0, 0), False)
        self.assertEqual(g.is_empty(0, 1), True)

    def test_get_random_empty_moves(self):
        g = game.Game(3)
        g.make_move(0, 0, const.RED)
        g.make_move(1, 0, const.BLUE)
        g.make_move(0, 2, const.RED)

        expected = np.array([[0, 1], [2, 0], [1, 1], [1, 2], [2, 1], [2, 2]]).flatten()
        actual = g.get_random_empty_moves(6).flatten()
        expected.sort()
        actual.sort()

        for i in range(len(expected)):
            if expected[0] == actual[0]:
                expected = expected[1:]
                actual = actual[1:]

        self.assertEqual(len(expected), 0)
        self.assertEqual(len(actual), 0)


class TestAIMethods(unittest.TestCase):
    def test_mcts(self):
        pass


if __name__ == '__main__':
    unittest.main()
