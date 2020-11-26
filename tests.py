import unittest
import numpy as np
import os
import gen_test_data


class TestGenTestData(unittest.TestCase):
    def test_generate_test_data(self):
        gen_test_data.generate_test_data(1, 1)
        self.assertTrue(os.path.isfile("test_data/game0"))

    def test_flip_board(self):
        gen_test_data.flip_board("test_data/game0")
        self.assertTrue(os.path.isfile("test_data/game0-d"))

    def test_create_board(self):
        interface = gen_test_data.create_board(["j4", "a2", "b4"])
        self.assertEqual({(9, 3), (0, 1), (1, 3)}, set(interface.game.move_list))

    def test_read_from_file(self):
        interface = gen_test_data.read_from_file("testgame")
        self.assertEqual({(4, 10), (2, 10)}, set(interface.game.move_list))

    def test_convert_to_move(self):
        self.assertEqual("c4", gen_test_data._convert_to_move("2, 3"))
        self.assertEqual("c5", gen_test_data._convert_to_move("2, 4"))
        self.assertEqual("a1", gen_test_data._convert_to_move("0, 0"))

    def test_flip_move(self):
        self.assertEqual("5, 4", gen_test_data._flip_move("(5, 6)"))
        self.assertEqual("2, 5", gen_test_data._flip_move("(8, 5)"))




if __name__ == '__main__':
    unittest.main()
