from sys import stderr
from mctsagent import mctsagent
from gamestate import gamestate
from gtpinterface import gtpinterface
import time
import random


if __name__ == "__main__":
    for i in range(10000):
        agent = mctsagent(gamestate(11))
        interface = gtpinterface(agent)
        interface.gtp_time([30])
        while interface.game.winner() == interface.game.PLAYERS["none"]:
            print(interface.gtp_genmove([])[1])
        output_file = open("test_data/game" + str(i), "w")
        print("finished game " + str(i) + "\n" + str(interface.gtp_show([])[1]))
        output_file.write(str(interface.game.move_list))
