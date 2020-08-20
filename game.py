import numpy as np
import constants as const


class Game:
    def __init__(self, board_size: int = 11):
        """
        Constructs a game with a given board size

        Parameters:
            board_size : int
                the size of the board
        """
        self.turn = 0
        self.board_size = board_size
        self.board = np.zeros((board_size, board_size), dtype=np.int8)

    # TODO: save some intermediate work to speed up computation for future calls in the same game
    # TODO: test aggressively, IS NOT CONFIRMED TO WORK
    def has_won(self, color) -> bool:
        """
        Checks if the given color has won

        Parameters:
            color : int
                the color to check (red = 1, blue = 2)

        Returns:
            a boolean if the color has won (true) or not (false)
        """
        if self.turn < self.board_size * 2:
            return False

        seen_nodes = set()
        chain = []
        if color == const.BLUE:  # blue: check vertically for win
            for i in range(self.board_size):
                if self.board[i][0] == color:
                    # add all starting nodes
                    seen_nodes.add((i, 0))
                    chain.append((i, 0))

            while len(chain) != 0:  # while nodes are unvisited
                next_node = chain.pop()
                neighbors = self._get_neighbors_by_color(next_node[0], next_node[1],
                                                         self.board[next_node[0]][next_node[1]])
                for n in neighbors:
                    if n[0] == self.board_size - 1:  # if a neighbor is on the other side, chain exists, game over
                        return True
                    if n not in seen_nodes:  # if n hasn't been seen, mark as seen and add to list
                        seen_nodes.add(n)
                        chain.append(n)

        else:  # red: check horizontally for win
            for i in range(self.board_size):
                if self.board[0][i] == color:
                    seen_nodes.add((0, i))
                    chain.append((0, i))

            while len(chain) != 0:  # while nodes are unvisited
                next_node = chain.pop()
                neighbors = self._get_neighbors_by_color(next_node[0], next_node[1],
                                                         self.board[next_node[0]][next_node[1]])
                for n in neighbors:
                    if n[1] == self.board_size - 1:  # if a neighbor is on the other side, chain exists, game over
                        return True
                    if n not in seen_nodes:  # if n hasn't been seen, mark as seen and add to list
                        seen_nodes.add(n)
                        chain.append(n)
        return False

    def print_board(self):
        """
        Prints the board to console
        """
        for i in range(self.board[0].size):
            print(' '*i + str(self.board[i]))

    def _get_all_neighbors(self, x: int, y: int) -> set:
        """
        Gets a set of (x, y) tuples to all neighboring tiles of a given location
        Parameters:
            x : int
                the x coordinate of the location to get the neighbors of
            y : int
                the y coordinate of the location to get the neighbors of

        Returns:
            set of tuples of all neighboring tiles to the given tile in (x, y) format
        """
        neighbors = set()
        # ex. for (1,1), 6 neighbors are (1,0), (0,1), (0,2), (1,2), (2,0), and (2,1)
        if x > 0:
            neighbors.add((x - 1, y))
        if y > 0:
            neighbors.add((x, y - 1))
            if x < self.board_size - 1:
                neighbors.add((x + 1, y - 1))

        if x < self.board_size - 1:
            neighbors.add((x + 1, y))

        if y < self.board_size - 1:
            neighbors.add((x, y + 1))
            if x > 0:
                neighbors.add((x - 1, y + 1))
        return neighbors

    def _get_neighbors_by_color(self, x: int, y: int, color: int) -> set:
        """
        Gets a set of (x, y) tuples to all neighboring tiles of a given location that match the given color
        Parameters:
            x : int
                the x coordinate of the location to get the neighbors of
            y : int
                the y coordinate of the location to get the neighbors of
            color : int
                the color of the location (red = 1, blue = 2)

        Returns:
            list of tuples of all neighboring tiles to the given tile in (x, y) format that match the given color
        """
        return {(x, y) for (x, y) in self._get_all_neighbors(x, y) if self.board[x][y] == color}


if __name__ == '__main__':
    game_board = Game()
    is_red = True
    while game_board.turn < game_board.board_size ** 2:
        game_board.print_board()
        line_in = input('please input a move in format \"row col\"\n')
        coords = line_in.split(' ')
        if is_red:
            game_board.board[int(coords[0])][int(coords[1])] = const.RED
        else:
            game_board.board[int(coords[0])][int(coords[1])] = const.BLUE

        game_board.turn += 1
        is_red = not is_red
