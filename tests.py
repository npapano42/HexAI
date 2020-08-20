import unittest
import game
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

    def test_get_neighbors_by_color(self):
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


if __name__ == '__main__':
    unittest.main()
