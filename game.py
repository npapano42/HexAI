import numpy as np


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
        self.board = np.zeros((board_size, board_size), dtype=int)

    def has_won(self, color) -> bool:
        """
        checks if the given color has won

        Parameters:
            color : int
                the color to check (red = 1, blue = 2)

        Returns:
            a boolean if the color has won (true) or not (false)
        """
        pass

    def print_board(self):
        """
        prints the board
        """
        for i in range(self.board[0].size):
            for j in range(i):
                print(' ', end='')
            print(self.board[i])

    def _get_all_neighbors(self, x: int, y: int) -> list:
        """
        gets a list of (x, y) tuples to all neighboring tiles of a given location
        Parameters:
            x : int
                the x coordinate of the location to get the neighbors of
            y : int
                the y coordinate of the location to get the neighbors of

        Returns:
            list of tuples of all neighboring tiles to the given tile in (x, y) format
        """
        neighbors = []
        # ex. for (1,1), 6 neighbors are (1,0), (0,1), (0,2), (1,2), (2,0), and (2,1)
        if x > 0:
            neighbors.append((x - 1, y))
        if y > 0:
            neighbors.append((x, y - 1))
            if x < self.board_size - 1:
                neighbors.append((x + 1, y - 1))

        if x < self.board_size - 1:
            neighbors.append((x + 1, y))

        if y < self.board_size - 1:
            neighbors.append((x, y + 1))
            if x > 0:
                neighbors.append((x - 1, y + 1))
        return neighbors

    def _get_neighbors_by_color(self, x: int, y: int, color: int) -> list:
        """
        gets a list of (x, y) tuples to all neighboring tiles of a given location that match the given color
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
        pass


if __name__ == '__main__':
    game_board = Game()
    is_red = False
    while game_board.turn < game_board.board_size ** 2:
        game_board.print_board()
        line_in = input('please input a move in format \"row col\"\n')
        coords = line_in.split(' ')
        if is_red:
            game_board.board[int(coords[0])][int(coords[1])] = 1
        else:
            game_board.board[int(coords[0])][int(coords[1])] = 2

        game_board.turn += 1
        is_red = not is_red
