class Position:
    def __init__(self, col: int, row: int):
        self.col = col
        self.row = row

    def __copy__(self):
        return Position(self.col, self.row)
