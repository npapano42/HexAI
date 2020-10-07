import numpy as np
import constants as const
import game as g


class AI:
    # TODO: add typing for network once finalized
    def __init__(self, game: g.Game, network):
        """
        Constructs an AI given a game and network

        Parameters:
            game : Game
                The game object containing the board for the AI to look over
            network: ??
                The network that will take in a board state and output the
        """
        self.game = game
        self.network = network

    def mcts(self) -> tuple:
        """
        Short for Monte Carlo Tree Search. Selects promising moves on the game tree
        based on the network output, performs rollouts on them, and returns the value back up the tree.

        Returns:
            The best move based on the result of the rollouts
        """
        # rollout (expansion + simulation)
        # moves = select_moves()
        # Backpropagation
        return 0, 0


class Node:
    def __init__(self):
        self.wins = 0
        self.playouts = 0
        self.nodes = []
