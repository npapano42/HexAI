import operator
import random
import time
from copy import deepcopy
from math import sqrt, log
from queue import Queue
from sys import stderr

import numpy as np
from tensorflow import keras

from gamestate import gamestate

inf = float('inf')
model = keras.models.load_model('CNN_hex_model')

class node:
	"""
	Node for MCTS. Stores the move applied to reach this node from its parent,
	stats for the associated game position, children, parent and outcome
	(outcome == none unless the position ends the game).
	"""

	def __init__(self, move=None, parent=None):
		"""
		Initialize a new node with optional move and parent and initially empty
		children list and rollout statistics and unspecified outcome.
		"""
		self.move = move
		self.parent = parent
		self.N = 0  # times this position was visited
		self.Q = 0  # average reward (wins-losses) from this position
		self.children = []
		self.outcome = gamestate.PLAYERS["none"]

	def add_children(self, children):
		"""
		Add a list of nodes to the children of this node.
		"""
		self.children += children

	def set_outcome(self, outcome):
		"""
		Set the outcome of this node (i.e. if we decide the node is the end of
		the game)
		"""
		self.outcome = outcome

	def value(self, explore):
		"""
		Calculate the UCT value of this node relative to its parent, the parameter
		"explore" specifies how much the value should favor nodes that have
		yet to be thoroughly explored versus nodes that seem to have a high win
		rate.
		Currently explore is set to zero when choosing the best move to play so
		that the move with the highest winrate is always chosen. When searching
		explore is set to EXPLORATION specified above.
		"""
		# unless explore is set to zero, maximally favor unexplored nodes
		if self.N == 0:
			if explore == 0:
				return 0
			else:
				return inf
		else:
			return self.Q / self.N + explore * sqrt(2 * log(self.parent.N) / self.N)


class mctsagent:
	"""
	Basic no frills implementation of an agent that preforms MCTS for hex.
	"""
	EXPLORATION = 1

	def __init__(self, state=gamestate(11)):
		self.root_state = deepcopy(state)
		self.root = node()		

	def best_move(self):
		"""
		Return the best move according to the current tree.
		"""
		if self.root_state.winner() != gamestate.PLAYERS["none"]:
			return gamestate.GAMEEND

		# choose the move of the most simulated node breaking ties randomly
		max_value = max(self.root.children, key=lambda n: n.N).N
		max_nodes = [n for n in self.root.children if n.N == max_value]
		best_child = random.choice(max_nodes)
		return best_child.move

	def move(self, move):
		"""
		Make the passed move and update the tree appropriately.
		"""
		for child in self.root.children:
			# make the child associated with the move the new root
			if move == child.move:
				child.parent = None
				self.root = child
				self.root_state.play(child.move)
				return

		# if for whatever reason the move is not in the children of
		# the root just throw out the tree and start over
		self.root_state.play(move)
		self.root = node()

	def search(self, time_budget):
		"""
		Search and update the search tree for a specified amount of time in seconds.
		"""
		start_time = time.clock()
		num_rollouts = 0

		# do until we exceed our time budget
		while time.clock() - start_time < time_budget:
			node, state = self.select_node()
			turn = state.turn()
			outcome = self.roll_out(state)
			self.backup(node, turn, outcome)
			num_rollouts += 1

		stderr.write("Ran " + str(num_rollouts) + " rollouts in " + str(time.clock() - start_time) + " sec\n")
		stderr.write("Node count: " + str(self.tree_size()) + "\n")

	def select_node(self):
		"""
		Select a node in the tree to preform a single simulation from.
		"""
		node = self.root
		state = deepcopy(self.root_state)

		# stop if we find reach a leaf node
		while len(node.children) != 0:
			# descend to the maximum value node, break ties at random
			max_value = max(node.children, key=lambda n: n.value(self.EXPLORATION)).value(self.EXPLORATION)
			max_nodes = [n for n in node.children if n.value(self.EXPLORATION) == max_value]
			node = random.choice(max_nodes)
			state.play(node.move)

			# if some child node has not been explored select it before expanding
			# other children
			if node.N == 0:
				return node, state

		# if we reach a leaf node generate its children and return one of them
		# if the node is terminal, just return the terminal node
		if self.expand(node, state):
			node = random.choice(node.children)
			state.play(node.move)
		return node, state

	def roll_out(self, state):
		"""
		Simulate an entirely random game from the passed state and return the winning
		player.
		"""
		moves = state.moves()

		while state.winner() == gamestate.PLAYERS["none"]:
			x = []
			for i in moves:
				new_state = deepcopy(state)
				new_state.play(i)
				x.append(new_state.board)
			y = np.array([game for game in x])
			y = np.expand_dims(y, 3)
			prediction = model.predict(y)
			prediction = prediction.flatten().tolist()
			res = {moves[i]: prediction[i] for i in range(len(moves))}
			move = max(res.items(), key=operator.itemgetter(1))[0] if state.turn() == gamestate.PLAYERS["white"] else min(res.items(), key=operator.itemgetter(1))[0]
			state.play(move)
			moves.remove(move)

		return state.winner()

	def backup(self, node, turn, outcome):
		"""
		Update the node statistics on the path from the passed node to root to reflect
		the outcome of a randomly simulated playout.
		"""
		# note that reward is calculated for player who just played
		# at the node and not the next player to play
		reward = -1 if outcome == turn else 1

		while node != None:
			node.N += 1
			node.Q += reward
			reward = -reward
			node = node.parent

	def expand(self, parent, state):
		"""
		Generate the children of the passed "parent" node based on the available
		moves in the passed game state and add them to the tree.
		"""
		children = []
		if state.winner() != gamestate.PLAYERS["none"]:
			# game is over at this node so nothing to expand
			return False

		for move in state.moves():
			children.append(node(move, parent))

		parent.add_children(children)
		return True

	def set_gamestate(self, state):
		"""
		Set the root state of the tree to the passed game state, this clears all
		the information stored in the tree since none of it applies to the new
		state.
		"""
		self.root_state = deepcopy(state)
		self.root = node()

	def tree_size(self):
		"""
		Count nodes in tree by BFS.
		"""
		Q = Queue()
		count = 0
		Q.put(self.root)
		while not Q.empty():
			node = Q.get()
			count += 1
			for child in node.children:
				Q.put(child)
		return count
