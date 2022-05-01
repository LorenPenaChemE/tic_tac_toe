"""
Tic-tac-toe
Loren Pena
Purpose of this is to create a tictactoe game is arrays and bitboards.
I dont think I fully got rid of the bugs, but its pretty close.
"""

import time
from enum import Enum


class GameBoardPlayer(Enum):
    """
    An enum that represents a player on a game board; it's used to denote:
    . which player occupies a space on the board (can be NONE if unoccupied)
    . which player is the winner of the game (can be DRAW)
    """
    NONE = 0
    X = 1
    O = 2
    DRAW = 3

    def __str__(self):
        if self.value == 0:
            return str(" ")
        else:
            return str(self.name)


class ArrayGameBoard:
    """A class that represents a rectangular game board"""

    def __init__(self, nrows, ncols):
        if nrows < 0 or isinstance(nrows, int) != True:
            raise ValueError("Cant have negative rows or not integer")
        else:
            self.nrows = nrows

        if ncols < 0 or isinstance(ncols, int) != True:
            raise ValueError("Cant have negative cols or not integer")
        else:
            self.ncols = ncols

        self.array = [GameBoardPlayer.NONE for _ in range(nrows * ncols)]

    def get_nrows(self):
        return self.nrows

    def get_ncols(self):
        return self.ncols

    def set(self, row, col, value):
        """Set the value at (row, col)"""
        if row < 0 or row > self.nrows:
            raise IndexError("Row is out of index")
        if col < 0 or col > self.ncols:
            raise IndexError("Col is out of index")

        self.array[row * self.ncols + col] = value

    def get(self, row, col):
        """Get the value at (row, col)"""
        return self.array[row * self.ncols + col]

    def get_winner(self):
        col_state = False
        row_state = False
        d_state = False
        dd_state = False

        if GameBoardPlayer.NONE not in self.array:
            return GameBoardPlayer.DRAW
        for row in range(self.nrows):
            for col in range(self.ncols - 1):
                if self.get(row, col) == GameBoardPlayer.NONE:
                    break
                else:
                    if self.get(row, col) == self.get(row, col + 1):
                        col_state = True
                    else:
                        col_state = False
            if col_state == True:
                return self.get(row, col)

        for row in range(self.nrows):
            for col in range(self.ncols - 1):
                if self.get(col, row) == GameBoardPlayer.NONE:
                    break
                else:
                    if self.get(col, row) == self.get(col + 1, row):
                        row_state = True
                    else:
                        row_state = False
            if row_state == True:
                return self.get(col, row)

        if self.nrows == self.ncols:
            for row in range(self.nrows - 1):
                if self.get(row, row) == GameBoardPlayer.NONE:
                    break
                else:
                    if self.get(row, row) == self.get(row + 1, row + 1):
                        d_state = True
                    else:
                        d_state = False
            if d_state == True:
                return self.get(row, row)

            for row in range(self.nrows - 1):
                if self.get(self.nrows - row - 1, row) == GameBoardPlayer.NONE:
                    break
                else:
                    if self.get(self.nrows - 1 - row, row) == self.get(self.nrows - 1 - row - 1, row + 1):
                        dd_state = True
                    else:
                        dd_state = False
            if dd_state == True:
                return self.get(self.nrows - row - 1, row)

            if col_state == False:
                return (GameBoardPlayer.NONE)
            if row_state == False:
                return (GameBoardPlayer.NONE)
            if d_state == False:
                return (GameBoardPlayer.NONE)
            if dd_state == False:
                return (GameBoardPlayer.NONE)

    def __str__(self):
        s = ""
        middle = ""
        for col in range(self.ncols):
            if col < self.ncols - 1:
                middle += "-+"
            else:
                middle += "-"

        for row in range(self.nrows):
            for col in range(self.ncols):
                if col < self.ncols - 1:
                    s += f"{self.get(row, col)}" + str("|")
                else:
                    s += f"{self.get(row, col)}"
            if row < self.nrows - 1:
                s += "\n" + middle + "\n"
        return s


class BitGameBoard:
    """A class that represents a rectangular game board as a 1D bitarray"""

    def __init__(self, nrows, ncols):
        if nrows < 0 or isinstance(nrows, int) != True:
            raise ValueError("Cant have negative rows or not integer")
        else:
            self.nrows = nrows

        if ncols < 0 or isinstance(ncols, int) != True:
            raise ValueError("Cant have negative cols or not integer")
        else:
            self.ncols = ncols
        self.board = 0

    def get_nrows(self):
        return (self.nrows)

    def get_ncols(self):
        return (self.ncols)

    def set(self, row, col, player):
        position = (col + (row * self.nrows)) * 2
        if player == GameBoardPlayer.X:
            self.board |= player.value << position

        if player == GameBoardPlayer.O:
            self.board |= player.value << position

    def get(self, row, col):
        position = (col + (row * self.nrows)) * 2
        bitboard_insert = self.board >> position
        binary_test = 0b11
        test_output = bitboard_insert & binary_test
        if bin(test_output) == bin(GameBoardPlayer.NONE.value):
            return (GameBoardPlayer.NONE)
        elif bin(test_output) == bin(GameBoardPlayer.X.value):
            return (GameBoardPlayer.X)
        elif bin(test_output) == bin(GameBoardPlayer.O.value):
            return (GameBoardPlayer.O)
        return position

    def __str__(self):
        s = ""
        middle = ""
        for col in range(self.ncols):
            if col < self.ncols - 1:
                middle += "-+"
            else:
                middle += "-"

        for row in range(self.nrows):
            for col in range(self.ncols):
                if col < self.ncols - 1:
                    s += f"{self.get(row, col)}" + str("|")
                else:
                    s += f"{self.get(row, col)}"
            if row < self.nrows - 1:
                s += "\n" + middle + "\n"
        return s

    def get_winner(self):
        col_state = False
        row_state = False
        d_state = False
        dd_state = False

        for row in range(self.nrows):
            for col in range(self.ncols - 1):
                if self.get(row, col) == GameBoardPlayer.NONE:
                    break
                else:
                    if self.get(row, col) == self.get(row, col + 1):
                        col_state = True
                    else:
                        col_state = False
            if col_state == True:
                return self.get(row, col)

        for row in range(self.nrows):
            for col in range(self.ncols - 1):
                if self.get(col, row) == GameBoardPlayer.NONE:
                    break
                else:
                    if self.get(col, row) == self.get(col + 1, row):
                        row_state = True
                    else:
                        row_state = False
            if row_state == True:
                return self.get(col, row)

        if self.nrows == self.ncols:
            for row in range(self.nrows - 1):
                if self.get(row, row) == GameBoardPlayer.NONE:
                    break
                else:
                    if self.get(row, row) == self.get(row + 1, row + 1):
                        d_state = True
                    else:
                        d_state = False
            if d_state == True:
                return self.get(row, row)

            for row in range(self.nrows - 1):
                if self.get(self.nrows - row - 1, row) == GameBoardPlayer.NONE:
                    break
                else:
                    if self.get(self.nrows - 1 - row, row) == self.get(self.nrows - 1 - row - 1, row + 1):
                        dd_state = True
                    else:
                        dd_state = False
            if dd_state == True:
                return self.get(self.nrows - row - 1, row)

            if col_state == False:
                return (GameBoardPlayer.NONE)
            if row_state == False:
                return (GameBoardPlayer.NONE)
            if d_state == False:
                return (GameBoardPlayer.NONE)
            if dd_state == False:
                return (GameBoardPlayer.NONE)


class TicTacToeBoard:
    """
    A class that represents a Tic Tac Toe game board.
    It's a thin wrapper around the actual game board
    """
    NROWS = 3
    NCOLS = 3

    def __init__(self):
        # The two game boards can be used interchangeably.
        self.board = ArrayGameBoard(self.NROWS, self.NCOLS)
        # self.board = BitGameBoard(self.NROWS, self.NCOLS)

    def set(self, row, col, value):
        if self.board.get(row, col) != GameBoardPlayer.NONE:
            raise ValueError(f"{row} {col} already has {self.board.get(row, col)}")
        self.board.set(row, col, value)

    def get(self, row, col):
        return self.board.get(row, col)

    def get_winner(self):
        return self.board.get_winner()

    def __str__(self):
        return self.board.__str__()


class HumanPlayer:
    """A class that represents a human planer"""

    def __init__(self, side):
        self.side = side

    def __str__(self):
        return f"Human player {self.side}"

    def get_move(self, board):
        """Get a move from the player; the board parameter is unused for now"""
        start = time.perf_counter()
        while True:
            try:
                moves = input(f"Please input move for {self} (row column): ")
                row, col = moves.split()
                return int(row), int(col), (time.perf_counter() - start)
            except ValueError as e:
                print(f"Invalid input '{moves}':", e)


def ttt_game():
    """
    Play a round of Tic Tac Toe, until there's either a winner, or the game
    is a draw.
    """
    ttt_board = TicTacToeBoard()
    player1 = HumanPlayer(GameBoardPlayer.X)
    player2 = HumanPlayer(GameBoardPlayer.O)
    current_player = player1

    print(ttt_board)
    while True:
        row, col, duration = current_player.get_move(ttt_board)
        print(f"{current_player} makes move ({row} {col}) in {duration:.6f} seconds")
        try:
            ttt_board.set(row, col, current_player.side)
        except (ValueError, IndexError) as e:
            # ValueError if the space is already occupied, IndexError if off-grid
            print(e)
            continue
        print(ttt_board)

        winner = ttt_board.get_winner()
        if winner is GameBoardPlayer.DRAW:
            print("Game is a draw")
            break
        elif winner is GameBoardPlayer.NONE:
            # Switch player
            current_player = player1 if current_player is player2 else player2
        else:
            # There's a winner
            print(f"{current_player} wins")
            break


def test_game_board():
    gb = BitGameBoard(3, 3)
    gb1 = BitGameBoard(3, 3)
    gb2 = BitGameBoard(3, 3)
    gb3 = BitGameBoard(3, 3)
    gb4 = BitGameBoard(3, 3)
    gb5 = BitGameBoard(3, 3)
    try:
        gb1.get(100, 100)
        print("gb1.get(100, 100) fails to raise IndexError")
    except IndexError:
        print("gb1.get(100, 100) correctly raises IndexError")

    print(f"winner of board with 1 row of X is '{gb1.get_winner()}'")

    try:
        gb1.set(100, 100, GameBoardPlayer.O)
        print("gb1.set(100, 100, GameBoardPlayer.O) fails to raise IndexError")
    except IndexError:
        print("gb1.set(100, 100, GameBoardPlayer.O) correctly raises IndexError")
    print(f"winner of empty board is '{gb.get_winner()}'")
    print(gb)
    gb.set(0, 0, GameBoardPlayer.X)
    gb.set(0, 1, GameBoardPlayer.X)
    gb.set(0, 2, GameBoardPlayer.X)
    gb.set(1, 0, GameBoardPlayer.X)
    gb.set(1, 1, GameBoardPlayer.X)
    gb.set(1, 2, GameBoardPlayer.X)
    gb.set(2, 0, GameBoardPlayer.X)
    gb.set(2, 1, GameBoardPlayer.X)
    gb.set(2, 2, GameBoardPlayer.X)
    print(gb)
    print(f"winner of full board is '{gb.get_winner()}'")
    gb1.set(0, 0, GameBoardPlayer.X)
    gb1.set(0, 1, GameBoardPlayer.X)
    gb1.set(0, 2, GameBoardPlayer.X)
    print(gb1)
    print(f"winner of board with 1 row of X is '{gb1.get_winner()}'")
    print("gb1.get(0, 0) returns", gb1.get(0, 0))
    print("gb1.get(0, 1) returns", gb1.get(0, 1))
    print("gb1.get(0, 2) returns", gb1.get(0, 2))

    gb2.set(1, 0, GameBoardPlayer.X)
    gb2.set(1, 1, GameBoardPlayer.X)
    gb2.set(1, 2, GameBoardPlayer.X)
    print(gb2)
    print(f"winner of board with 1 column of X is '{gb2.get_winner()}'")

    gb3.set(0, 0, GameBoardPlayer.X)
    gb3.set(1, 0, GameBoardPlayer.X)
    gb3.set(2, 0, GameBoardPlayer.X)
    print(gb3)
    print(f"winner of board with 1 row of X is '{gb3.get_winner()}'")

    gb4.set(0, 2, GameBoardPlayer.O)
    gb4.set(1, 1, GameBoardPlayer.O)
    gb4.set(2, 0, GameBoardPlayer.O)
    print(gb4)
    print(f"winner of board with diagonal of O is '{gb4.get_winner()}'")

    gb5.set(0, 0, GameBoardPlayer.O)
    gb5.set(1, 1, GameBoardPlayer.O)
    gb5.set(2, 2, GameBoardPlayer.O)
    print(gb5)
    print(f"winner of board with diagonal of O is '{gb5.get_winner()}'")


if __name__ == '__main__':
    c = test_game_board()