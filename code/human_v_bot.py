# tag::play_against_your_bot[]
from dlgo import goboard
from dlgo import gotypes
from dlgo.agent.naive import RandomBot
from dlgo.utils import print_board, print_move, point_from_coords


def read_human_move(game):  # <1>
    while True:
        try:
            coords = input('-- ').strip().upper()
        except (EOFError, KeyboardInterrupt):  # <2>
            print('')
            return goboard.Move.resign()
        try:
            move = goboard.Move.play(point_from_coords(coords))
        except (IndexError, ValueError):
            print('Enter a coordinate like D4.')
            continue
        if not game.is_valid_move(move):
            print('%s is not a legal move.' % coords)
            continue
        return move


def main():
    board_size = 9
    game = goboard.GameState.new_game(board_size)
    bot = RandomBot()

    while not game.is_over():
        print(chr(27) + "[2J")
        print_board(game.board)
        if game.next_player == gotypes.Player.black:
            move = read_human_move(game)
        else:
            move = bot.select_move(game)
        print_move(game.next_player, move)
        game = game.apply_move(move)

    print_board(game.board)
    print('Winner: %s' % game.winner())


if __name__ == '__main__':
    main()
# <1> Re-prompt on typos and illegal moves instead of crashing on an assertion.
# <2> Ctrl-D or Ctrl-C resigns instead of raising.
# end::play_against_your_bot[]
