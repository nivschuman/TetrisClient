from Square import Square
from TShape import TShape
from Line import Line
from ZShapeL import ZShapeL
from ZShapeR import ZShapeR
from LShapeR import LShapeR
from LShapeL import LShapeL
from Exceptions import CannotMoveException
import pygame
import random


# todo make lose condition clearer
class Board:
    def __init__(self, length, width, block_sizes):
        self.__board = []
        for i in range(width):
            col = []
            for j in range(length):
                col.append(0)

            self.__board.append(col)

        self.__length = length
        self.__width = width
        self.__block_sizes = block_sizes

        self.__tetrinos = [
            TShape(block_sizes, length, width),
            Square(block_sizes, length, width),
            Line(block_sizes, length, width),
            ZShapeL(block_sizes, length, width),
            ZShapeR(block_sizes, length, width),
            LShapeR(block_sizes, length, width),
            LShapeL(block_sizes, length, width)
        ]
        random.shuffle(self.__tetrinos)
        self.__currentIdx = 0
        self.update_piece()

        self.__copy_tetrino = None
        self.update_copy()

        self.__playable = True

    @property
    def length(self):
        return self.__length

    @property
    def width(self):
        return self.__width

    @property
    def block_sizes(self):
        return self.__block_sizes

    @property
    def board(self):
        return self.__board

    @property
    def playable(self):
        return self.__playable

    # perform move and return how many lines were cleared
    def move_piece(self, move_type):
        cleared = 0
        if move_type == "down":
            try:
                self.__tetrinos[self.__currentIdx].move_down(self.__board)
            except CannotMoveException:
                for pos in self.__tetrinos[self.__currentIdx].get_positions():
                    self.__board[pos.row][pos.col] = 1
                cleared = self.update_board()
                self.__change_piece()
        elif move_type == "right":
            self.__tetrinos[self.__currentIdx].move_right(self.__length, self.__board)
        elif move_type == "left":
            self.__tetrinos[self.__currentIdx].move_left(self.__board)
        elif move_type == "drop":
            stop = False
            while not stop:
                try:
                    self.__tetrinos[self.__currentIdx].move_down(self.__board)
                    self.update_piece()
                except CannotMoveException:
                    stop = True
                    for pos in self.__tetrinos[self.__currentIdx].get_positions():
                        self.__board[pos.row][pos.col] = 1
                    cleared = self.update_board()
                    self.__change_piece()

        self.update_piece()
        return cleared

    def rotate_piece(self, direction):
        if direction == "left":
            self.__tetrinos[self.__currentIdx].rotate_left(self.__length, self.__width, self.__board)
        elif direction == "right":
            self.__tetrinos[self.__currentIdx].rotate_right(self.__length, self.__width, self.__board)

        self.update_piece()

    # removes current 2s from the board and places 2s according to current tetrino
    def update_piece(self):
        for i in range(len(self.__board)):
            for j in range(len(self.__board[i])):
                if self.__board[i][j] == 2:
                    self.__board[i][j] = 0

        for pos in self.__tetrinos[self.__currentIdx].get_positions():
            self.__board[pos.row][pos.col] = 2

        self.update_copy()

    def update_copy(self):
        for i in range(len(self.__board)):
            for j in range(len(self.__board[i])):
                if self.__board[i][j] == 3:
                    self.__board[i][j] = 0

        self.__copy_tetrino = self.__tetrinos[self.__currentIdx].__copy__()

        stop = False
        while not stop:
            try:
                self.__copy_tetrino.move_down(self.__board)
            except CannotMoveException:
                stop = True
                for pos in self.__copy_tetrino.get_positions():
                    if self.__board[pos.row][pos.col] != 2:
                        self.__board[pos.row][pos.col] = 3

    # update board and return number of lines cleared
    def update_board(self):
        cleared = 0
        i = 0
        while i < len(self.__board):
            row = self.__board[i]

            full = []
            new_row = []
            for k in range(len(row)):
                full.append(1)
                new_row.append(0)

            if row == full:
                cleared += 1
                self.__board.pop(i)
                self.__board.insert(len(self.__board)-1, new_row)
                i -= 1

                sound_obj = pygame.mixer.Sound("Sounds/ClearLine.mp3")
                sound_obj.set_volume(1)
                sound_obj.play()
                continue

            i += 1

        return cleared

    # todo add lose condition(make piece go up if needed). Stop pieces from becoming huge.
    def add_lines(self, amount):
        empty_row_idx = random.randint(0, self.length-1)

        # generate row to add
        new_row = []
        for i in range(self.length):
            if i != empty_row_idx:
                new_row.append(1)
            else:
                new_row.append(0)

        for k in range(amount):
            self.__board.insert(0, new_row)
            self.__board.pop(len(self.__board)-1)

        self.update_piece()
        self.update_copy()

    def __change_piece(self):
        self.__currentIdx += 1
        if self.__currentIdx == len(self.__tetrinos):
            self.__tetrinos = [
                TShape(self.__block_sizes, self.length, self.width),
                Square(self.__block_sizes, self.length, self.width),
                Line(self.__block_sizes, self.length, self.width),
                ZShapeL(self.__block_sizes, self.length, self.width),
                ZShapeR(self.__block_sizes, self.length, self.width),
                LShapeR(self.__block_sizes, self.length, self.width),
                LShapeL(self.__block_sizes, self.length, self.width)
            ]
            random.shuffle(self.__tetrinos)
            self.__currentIdx = 0

            # next tetrino cannot be spawned so board is unplayable
            for pos in self.__tetrinos[self.__currentIdx].get_positions():
                if self.__board[pos.row][pos.col] == 1:
                    self.__playable = False

            self.update_copy()
