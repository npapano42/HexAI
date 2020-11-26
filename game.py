import numpy as np
import constants as const
import DisjointSet


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
        self.moves = [(x, y) for x in range(board_size) for y in range(board_size)]
        self.djs = DisjointSet.DisjointSet(board_size)


    def has_won(self, color) -> bool:
        """
        Checks if the given color has won, employing an optimized disjoint set algorithm.
        When has_won is called, the disjoint sets are evaluated for a winner.

        Parameters:
            color : int
                the color to check (red = 1, blue = 2)

        Returns:
            a boolean if the color has won (true) or not (false)
        """
        # if color == const.RED: # evaluate top/down
        #     for next_set in self.djs.sets:
        #
        # else: # evaluate left/right

    def print_board(self):
        """
        Prints the board to console
        """
        for i in range(self.board[0].size):
            print(' ' * i + str(self.board[i]))

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

    def make_move(self, x: int, y: int, color: int) -> bool:
        """
        Makes a move at (x, y) by placing the color at that location, if it is available.
        If available, plays move and removes location from list of available moves

        Parameters:
            x : int
                the x coordinate of the location
            y : int
                the y coordinate of the location
            color : int
                the color to place at (x,y) on the board [note: see constants for numbering]

        Returns:
            True if move was successful, false if location was taken
        """
        if self.is_empty(x, y):
            self.board[x][y] = color
            self.moves.remove((x, y))
            for loc_x, loc_y in self._get_neighbors_by_color(x, y, color):
                self.djs.union_sets(self.djs.get_node(x, y), self.djs.get_node(loc_x, loc_y))
            self.djs.visualize()
            return True
        return False

    def is_empty(self, x: int, y: int) -> bool:
        """
        Checks to see if location (x, y) is empty, meaning no move has been played there already

        Parameters:
            x : int
                the x coordinate of the location
            y : int
                the y coordinate of the location

        Returns:
            True if empty, false otherwise
        """
        return self.board[x][y] == 0

    def get_random_empty_moves(self, n: int) -> np.ndarray:
        """
        Gets random empty locations on the board, such that the locations have a value of 0.

        Parameters:
            n : int
                number of moves to get

        Returns:
            An ndarray of tuples, each of which has a value of 0 on the board.
        """
        return np.random.default_rng().choice(self.moves, n, replace=False)


if __name__ == '__main__':
    game_board = Game()
    is_red = True
    while game_board.turn < game_board.board_size ** 2:
        game_board.print_board()
        player_color = const.BLUE
        if is_red:
            player_color = const.RED
        while True:
            line_in = input('please input a move in format \"row col\"\n')
            coords = line_in.split(' ')
            if game_board.make_move(int(coords[0]), int(coords[1]), player_color):
                break
            else:
                print("Move already taken!")

        game_board.turn += 1
        is_red = not is_red
