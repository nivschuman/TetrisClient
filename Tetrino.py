from Block import Block
from Position import Position
from Exceptions import CannotMoveException


class Tetrino:
    def __init__(self, block_side: int, positions, direction=0):
        self._blocks = []
        for pos in positions:
            s = Block(block_side, pos)
            self._blocks.append(s)

        self._direction = direction
        self._blockSide = block_side

    def __copy__(self):
        positions = []
        for block in self._blocks:
            positions.append(block.pos)

        return Tetrino(self._blockSide, positions, self._direction)

    def rotate_right(self, board_length, board_width, board_status):
        new_direction = self._direction + 90
        if new_direction >= 360:
            new_direction -= 360
        self._set_direction(board_length, board_width, new_direction, board_status)
        self._direction = new_direction

    def rotate_left(self, board_length, board_width, board_status):
        new_direction = self._direction - 90
        if new_direction < 0:
            new_direction += 360
        self._set_direction(board_length, board_width, new_direction, board_status)
        self._direction = new_direction

    def _set_direction(self, board_length, board_width, direction, board_status):
        pass

    def move_right(self, board_length, board_status):
        new_blocks = []

        for block in self._blocks:
            if block.pos.col + 1 >= board_length:
                raise CannotMoveException("right")
            if board_status[block.pos.row][block.pos.col+1] == 1:
                raise CannotMoveException("right")

            new_blocks.append(Block(self._blockSide, Position(block.pos.col + 1, block.pos.row)))

        self._blocks = new_blocks;

    def move_left(self, board_status):
        new_blocks = []

        for block in self._blocks:
            if block.pos.col - 1 < 0:
                raise CannotMoveException("left")
            if board_status[block.pos.row][block.pos.col-1] == 1:
                raise CannotMoveException("left")

            new_blocks.append(Block(self._blockSide, Position(block.pos.col - 1, block.pos.row)))

        self._blocks = new_blocks

    def move_down(self, board_status):
        new_blocks = []

        for block in self._blocks:
            if block.pos.row - 1 < 0:
                raise CannotMoveException("down")
            if board_status[block.pos.row-1][block.pos.col] == 1:
                raise CannotMoveException("down")

            new_blocks.append(Block(self._blockSide, Position(block.pos.col, block.pos.row - 1)))

        self._blocks = new_blocks

    def get_positions(self):
        positions = []
        for block in self._blocks:
            positions.append(block.pos)

        return positions
