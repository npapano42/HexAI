from sys import stderr
from mctsagent import mctsagent
from gamestate import gamestate
from gtpinterface import gtpinterface
import time
import random


def generate_test_data(rollout_time=30, game_amt=10000):
    """
    Generates test data from MCTS rollouts, writing to a folder

    rollout_time: time MCTS uses to explore the game tree
    iterations: the number of games to generate
    """
    # i controls name of file
    for i in range(413, game_amt):
        agent = mctsagent(gamestate(11))
        interface = gtpinterface(agent)
        interface.gtp_time([rollout_time])
        while interface.game.winner() == interface.game.PLAYERS["none"]:
            print(interface.gtp_genmove([])[1])
        output_file = open("test_data/game" + str(i), "w")
        print("finished game " + str(i) + "\n" + str(interface.gtp_show([])[1]))
        output_file.write(str(interface.game.move_list))


def rotate_board(input_file):
    # line = input_file.readline()
    agent = mctsagent(gamestate(11))
    interface = gtpinterface(agent)
    input_file = open("test_data_better/game5", "r")

    line = input_file.readline()
    # split moves
    moves = line.split("), (")
    # slice off brackets
    moves[0] = moves[0][2:]
    moves[-1] = moves[-1][:-2]

    for move in moves:
        print(move)
        coords = move.split(", ", maxsplit=1)
        x = chr(ord('a') + int(coords[0]))
        y = str(int(coords[1]) + 1)
        print(x, y)
        interface.gtp_play([(x, y), interface.game.turn()])

    print(str(interface.gtp_show([])[1]))


def rewind_board():
    pass


if __name__ == "__main__":
    generate_test_data()

