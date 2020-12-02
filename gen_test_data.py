import os

from gamestate import gamestate
from gtpinterface import gtpinterface
from mctsagent import mctsagent


def generate_test_data(rollout_time=30, game_amt=10000):
    """
    Generates test data from MCTS rollouts, writing to a folder

    rollout_time: time MCTS uses to explore the game tree
    iterations: the number of games to generate
    """
    # i controls name of file
    for i in range(game_amt):
        agent = mctsagent(gamestate(11))
        interface = gtpinterface(agent)
        interface.gtp_time([rollout_time])
        while interface.game.winner() == interface.game.PLAYERS["none"]:
            print(interface.gtp_genmove([])[1])
        output_file = open("test_data/game" + str(i), "w")
        print("finished game " + str(i) + "\n" + str(interface.gtp_show([])[1]))
        output_file.write(str(interface.game.move_list))
        output_file.close()


def _flip_board(input_file_name):
    """
    Flips a board given an input file. Writes a new flipped board back in the same location, with the suffix -d attached

    input_file_name: the path to the file (ex. test_data/test_game)
    ex. test_data/test_game creates test_data/test_game-d
    """

    # read given file into a game
    interface = read_from_file(input_file_name)
    agent_diag = mctsagent(gamestate(11))
    interface_diag = gtpinterface(agent_diag)

    # apply all moves
    for move in interface.game.move_list:
        turn = 'w' if interface_diag.game.turn() == 1 else 'b'
        flip_move = _flip_move(str(move))
        interface_diag.gtp_play([turn, _convert_to_move(flip_move)])

    # write game to file
    flip_file = open(input_file_name + "-d", "w")
    flip_file.write(str(interface_diag.game.move_list))
    flip_file.close()


def create_board(move_list):
    """
    Takes a list of gtpinterface-valid moves (ex. ["j4", "a2", "b4"]) and creates a gtpinterface from them
    The gtpinterface has an attached gamestate object (called game) that has the current state of the board after the entire list of moves has been played

    move_list: list of gtpinterface-valid moves

    Returns a gtpinterface of the game with all moves in move_list played
    """
    agent = mctsagent(gamestate(11))
    interface = gtpinterface(agent)

    for move in move_list:
        # assign color and play
        turn = 'w' if interface.game.turn() == 1 else 'b'
        interface.gtp_play([turn, move])

    return interface


def read_from_file(input_file_name):
    """
    Reads in a file generated from generate_test_data(), applying all moves and returns the interface of the game

    Returns a gtpinterface of the game
    """
    return create_board(_get_move_list(input_file_name))


def _get_move_list(input_file_name):
    """
    Gets the move list from an input file

    input_file_name: a string that is the file name

    Returns a list of gtpinterface-valid moves
    """
    input_file = open(input_file_name, "r")
    line = input_file.readline()
    # split moves
    file_moves = line.split("), (")
    # slice off brackets
    file_moves[0] = file_moves[0][2:]
    file_moves[-1] = file_moves[-1][:-2]
    return [_convert_to_move(move) for move in file_moves]


def _convert_to_move(move):
    """
    Converts a string-based move (ex. read from a game file) coordinate move into a valid letter and number gtp_move

    Returns letter number combo of a move
    ex. convert_to_move("2, 3") -> "c4"
    """
    coords = move.split(", ", maxsplit=1)
    return str(chr(ord('a') + int(coords[0]))) + str(int(coords[1]) + 1)


def _flip_move(move):
    """
    Flips a move such that an input string move with braces ex. "(2, 8)", is flipped to the diagonally opposite position on the board "8, 2"

    Returns the flipped move in string format, without braces
    """
    move = move[1: -1].split(", ")
    move[0] = 11 - int(move[0]) - 1
    move[1] = 11 - int(move[1]) - 1
    return str(move)[1:-1]


def sort_games(test_data_folder):
    """
    Sorts games generated from generate_test_data into folders based on the winner, ignoring games without winners

    test_data_folder: the folder where games are placed
    """
    for game_file in os.listdir(test_data_folder):
        file_name = test_data_folder + "/" + game_file
        interface = read_from_file(file_name)
        if interface.gtp_winner([])[1] == "none":
            print("no win")
        elif interface.gtp_winner([])[1] == "white":
            os.rename(file_name, "white_wins/" + game_file)
        else:  # black wins
            os.rename(file_name, "black_wins/" + game_file)


def flip_and_rollback_all_boards():
    """
    Calls _flip_board and _rollback_game on all the games in their sorted locations
    """
    # flip games
    loc = "white_wins/"
    for game_file in os.listdir(loc):
        _flip_board(loc + game_file)
    loc = "black_wins/"
    for game_file in os.listdir(loc):
        _flip_board(loc + game_file)

    # rollback games
    loc = "white_wins/"
    for game_file in os.listdir(loc):
        _rollback_game(loc + game_file)
    loc = "black_wins/"
    for game_file in os.listdir(loc):
        _rollback_game(loc + game_file)


def _rollback_game(input_file_name):
    # read given file into a game
    moves = _get_move_list(input_file_name)

    for i in range(len(moves)):
        rollback_moves = moves[:(-1*i-1)]

        # if the rollback results in an empty move
        if len(rollback_moves) == 0:
            continue

        agent = mctsagent(gamestate(11))
        interface = gtpinterface(agent)

        # apply all moves
        for move in rollback_moves:
            turn = 'w' if interface.game.turn() == 1 else 'b'
            interface.gtp_play([turn, move])

        # write game to file
        flip_file = open(input_file_name + "-rollback-" + str(i+1), "w")
        flip_file.write(str(interface.game.move_list))
        flip_file.close()


if __name__ == "__main__":
    sort_games("test_data")
    flip_and_rollback_all_boards()
