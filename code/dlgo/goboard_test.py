import unittest

from dlgo.goboard import Board, GameState, Move
from dlgo.gotypes import Player, Point


class BoardTest(unittest.TestCase):
    def test_capture(self):
        board = Board(19, 19)
        board.place_stone(Player.black, Point(2, 2))
        board.place_stone(Player.white, Point(1, 2))
        self.assertEqual(Player.black, board.get(Point(2, 2)))
        board.place_stone(Player.white, Point(2, 1))
        self.assertEqual(Player.black, board.get(Point(2, 2)))
        board.place_stone(Player.white, Point(2, 3))
        self.assertEqual(Player.black, board.get(Point(2, 2)))
        board.place_stone(Player.white, Point(3, 2))
        self.assertIsNone(board.get(Point(2, 2)))

    def test_capture_two_stones(self):
        board = Board(19, 19)
        board.place_stone(Player.black, Point(2, 2))
        board.place_stone(Player.black, Point(2, 3))
        board.place_stone(Player.white, Point(1, 2))
        board.place_stone(Player.white, Point(1, 3))
        self.assertEqual(Player.black, board.get(Point(2, 2)))
        self.assertEqual(Player.black, board.get(Point(2, 3)))
        board.place_stone(Player.white, Point(3, 2))
        board.place_stone(Player.white, Point(3, 3))
        self.assertEqual(Player.black, board.get(Point(2, 2)))
        self.assertEqual(Player.black, board.get(Point(2, 3)))
        board.place_stone(Player.white, Point(2, 1))
        board.place_stone(Player.white, Point(2, 4))
        self.assertIsNone(board.get(Point(2, 2)))
        self.assertIsNone(board.get(Point(2, 3)))

    def test_capture_is_not_suicide(self):
        board = Board(19, 19)
        board.place_stone(Player.black, Point(1, 1))
        board.place_stone(Player.black, Point(2, 2))
        board.place_stone(Player.black, Point(1, 3))
        board.place_stone(Player.white, Point(2, 1))
        board.place_stone(Player.white, Point(1, 2))
        self.assertIsNone(board.get(Point(1, 1)))
        self.assertEqual(Player.white, board.get(Point(2, 1)))
        self.assertEqual(Player.white, board.get(Point(1, 2)))

    def test_remove_liberties(self):
        board = Board(5, 5)
        board.place_stone(Player.black, Point(3, 3))
        board.place_stone(Player.white, Point(2, 2))
        white_string = board.get_go_string(Point(2, 2))
        self.assertCountEqual(
            [Point(2, 3), Point(2, 1), Point(1, 2), Point(3, 2)],
            white_string.liberties)
        board.place_stone(Player.black, Point(3, 2))
        white_string = board.get_go_string(Point(2, 2))
        self.assertCountEqual(
            [Point(2, 3), Point(2, 1), Point(1, 2)],
            white_string.liberties)

    def test_empty_triangle(self):
        board = Board(5, 5)
        board.place_stone(Player.black, Point(1, 1))
        board.place_stone(Player.black, Point(1, 2))
        board.place_stone(Player.black, Point(2, 2))
        board.place_stone(Player.white, Point(2, 1))

        black_string = board.get_go_string(Point(1, 1))
        self.assertCountEqual(
            [Point(3, 2), Point(2, 3), Point(1, 3)],
            black_string.liberties)


class GameTest(unittest.TestCase):
    def test_new_game(self):
        start = GameState.new_game(19)
        next_state = start.apply_move(Move.play(Point(16, 16)))

        self.assertEqual(start, next_state.previous_state)
        self.assertEqual(Player.white, next_state.next_player)
        self.assertEqual(Player.black, next_state.board.get(Point(16, 16)))

    def test_boards_with_same_stones_are_equal(self):
        left = Board(19, 19)
        right = Board(19, 19)
        left.place_stone(Player.black, Point(3, 3))
        right.place_stone(Player.black, Point(3, 3))
        self.assertEqual(left, right)

        right.place_stone(Player.white, Point(5, 5))
        self.assertNotEqual(left, right)

    def test_ko(self):
        game = GameState.new_game(5)
        for player_move in [
                Point(2, 3),  # black
                Point(3, 3),  # white
                Point(3, 2),  # black
                Point(2, 4),  # white
                Point(4, 3),  # black
                Point(4, 4),  # white
                Point(1, 1),  # black, filler to keep colors alternating
                Point(3, 5),  # white
                Point(3, 4),  # black captures the white stone at 3-3
        ]:
            move = Move.play(player_move)
            self.assertTrue(game.is_valid_move(move), str(player_move))
            game = game.apply_move(move)

        self.assertIsNone(game.board.get(Point(3, 3)))
        # White may not retake immediately: that repeats the previous position.
        self.assertFalse(game.is_valid_move(Move.play(Point(3, 3))))

        game = game.apply_move(Move.play(Point(5, 5)))  # white plays a ko threat
        game = game.apply_move(Move.play(Point(5, 1)))  # black answers elsewhere
        # With two new stones on the board, retaking no longer repeats a position.
        self.assertTrue(game.is_valid_move(Move.play(Point(3, 3))))
        game = game.apply_move(Move.play(Point(3, 3)))
        self.assertIsNone(game.board.get(Point(3, 4)))

    def test_move_outside_the_board_is_not_valid(self):
        game = GameState.new_game(9)
        self.assertFalse(game.is_valid_move(Move.play(Point(16, 17))))
        self.assertFalse(game.is_valid_move(Move.play(Point(0, 1))))
        self.assertTrue(game.is_valid_move(Move.play(Point(9, 9))))


if __name__ == '__main__':
    unittest.main()
