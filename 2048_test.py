# # tests for 2048 game
from Game2048 import Game2048
import unittest

class mergeOneColumnMethods(unittest.TestCase):
    def test_1(self):
        test1 = [2,2,4,4]
        game = Game2048(4)
        changed = game.mergeOneColumn(test1)
        self.assertEqual(test1, [4,8,0,0])
        self.assertEqual(changed, True)

    def test_0_space(self):
        test2 = [2,2,0,2]
        game = Game2048(4)
        changed = game.mergeOneColumn(test2)
        self.assertEqual(test2, [4,2,0,0])
        self.assertEqual(changed, True)

    def test_null(self):
        test3 = [0,0,0,0]
        game = Game2048(4)
        changed = game.mergeOneColumn(test3)
        self.assertEqual(test3, [0,0,0,0])
        self.assertEqual(changed, False)

    def test_no_merge(self):
        test4 = [2,4,8,16]
        game = Game2048(4)
        changed = game.mergeOneColumn(test4)
        self.assertEqual(test4, [2,4,8,16])
        self.assertEqual(changed, False)

    def test_partial_merge_column(self):
        test5 = [2, 2, 4, 8]
        game = Game2048(4)
        changed = game.mergeOneColumn(test5)
        self.assertEqual(test5, [4,4,8,0])
        self.assertEqual(changed, True)

    def test_merge_middle(self):
        test6 = [0,4,4,8]
        game = Game2048(4)
        changed = game.mergeOneColumn(test6)
        self.assertEqual(test6, [8,8,0,0])
        self.assertEqual(changed, True)

    def test_merge_and_shift(self):
        test7 = [0,0,4,4]
        game = Game2048(4)
        changed = game.mergeOneColumn(test7)
        self.assertEqual(test7, [8,0,0,0])
        self.assertEqual(changed, True)

    def test_merge_with_zeros_between(self):
        test8 = [0,4,0,4]
        game = Game2048(4)
        changed = game.mergeOneColumn(test8)
        self.assertEqual(test8, [8,0,0,0])
        self.assertEqual(changed, True)

    def test_merge_with_zeros_between_2(self):
        test9 = [2,0,2,0]
        game = Game2048(4)
        changed = game.mergeOneColumn(test9)
        self.assertEqual(test9, [4,0,0,0])
        self.assertEqual(changed, True)

    def test_trailing_zeros(self):
        test10 = [4,2,0,0]
        game = Game2048(4)
        changed = game.mergeOneColumn(test10)
        self.assertEqual(test10, [4,2,0,0])
        self.assertEqual(changed, False)

    def test_trailing_zeros(self):
        test11 = [4,4,4,4]
        game = Game2048(4)
        changed = game.mergeOneColumn(test11)
        self.assertEqual(test11, [8,8,0,0])
        self.assertEqual(changed, True)

    def test_longer_column(self):
        longer_test = [2,2,0,0,4,0,0,4,0,0,2]
        game = Game2048(4)
        changed = game.mergeOneColumn(longer_test)
        self.assertEqual(longer_test, [4, 8, 2, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(changed, True)

    def test_trailing_zeros(self):
        test12 = [0,0,0,0]
        game = Game2048(4)
        changed = game.mergeOneColumn(test12)
        self.assertEqual(test12, [0,0,0,0])
        self.assertEqual(changed, False)

class mergeBoardMethods(unittest.TestCase):
    def test_R(self):
        game = Game2048(4)
        game.board = [[0, 0, 0, 0],
                      [2, 0, 2, 2],
                      [0, 0, 2, 4],
                      [2, 2, 4, 8]]
        changed = game.mergeBoard("R")
        self.assertEqual(game.board, [[0, 0, 0, 0],
                                [0, 0, 2, 4],
                                [0, 0, 2, 4],
                                [0, 4, 4, 8]])
        self.assertEqual(changed, True)

    def test_L(self):
        game = Game2048(4)
        game.board = [[0, 0, 0, 0],
                [2, 0, 2, 2],
                [0, 0, 2, 4],
                [2, 2, 4, 8]]
        changed = game.mergeBoard("L")
        self.assertEqual(game.board, [[0, 0, 0, 0],
                                      [4, 2, 0, 0],
                                      [2, 4, 0, 0],
                                      [4, 4, 8, 0]])
        self.assertEqual(changed, True)

    def test_U(self):
        game = Game2048(4)
        game.board = [[0, 0, 0, 0],
                [2, 0, 2, 2],
                [0, 0, 2, 4],
                [2, 2, 4, 8]]
        changed = game.mergeBoard("U")
        self.assertEqual(game.board, [[4, 2, 4, 2],
                                      [0, 0, 4, 4],
                                      [0, 0, 0, 8],
                                      [0, 0, 0, 0]])
        self.assertEqual(changed, True)

    def test_D(self):
        game = Game2048(4)
        game.board = [[0, 0, 0, 0],
                      [2, 0, 2, 2],
                      [0, 0, 2, 4],
                      [2, 2, 4, 8]]
        changed = game.mergeBoard("D")
        self.assertEqual(game.board, [[0, 0, 0, 0],
                                      [0, 0, 0, 2],
                                      [0, 0, 4, 4],
                                      [4, 2, 4, 8]])
        self.assertEqual(changed, True)

    def test_no_changed(self):
        game = Game2048(4)
        game.board = [[0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]]
        
        changed = game.mergeBoard("D")
        self.assertEqual(game.board, [[0, 0, 0, 0],
                                      [0, 0, 0, 0],
                                      [0, 0, 0, 0],
                                      [0, 0, 0, 0]])
        self.assertEqual(changed, False)

    def test_U_2(self):
        game = Game2048(4)
        game.board = [[8, 2, 16, 2],
                      [4, 8, 4, 16],
                      [16, 2, 0, 0],
                      [4, 0, 0, 8]]
        changed = game.mergeBoard("U")
        self.assertEqual(game.board, [[8, 2, 16, 2],
                                      [4, 8, 4, 16],
                                      [16, 2, 0, 8],
                                      [4, 0, 0, 0]])
        self.assertEqual(changed, True)
        self.assertEqual(game.lockedBoardState(), False)

        

class lockedBoardStateMethods(unittest.TestCase):
    def test_locked(self):
        game = Game2048(4)
        game.board = [[8, 64, 32, 16],
                      [4, 8, 2, 64],
                      [2, 32, 8, 2],
                      [8, 4, 32, 4]]
        self.assertEqual(game.lockedBoardState(), True)

    def test_locked_2(self):
        game = Game2048(4)
        game.board = [[8, 2, 16, 2],
                      [4, 8, 4, 16],
                      [0, 16, 2, 4],
                      [4, 0, 4, 8]]
        self.assertEqual(game.lockedBoardState(), False)

    def test_locked_3(self):
        game = Game2048(4)
        game.board = [[8, 2, 16, 2],
                      [4, 8, 4, 16],
                      [8, 0, 16, 2],
                      [0, 4, 8, 4]]
        self.assertEqual(game.lockedBoardState(), False)

    def test_locked_4(self):
        game = Game2048(4)
        game.board = [[8, 2, 16, 2],
                      [4, 8, 4, 16],
                      [8, 16, 2, 8],
                      [2, 4, 8, 2]]
        self.assertEqual(game.lockedBoardState(), True)


if __name__ == '__main__':
    unittest.main()

