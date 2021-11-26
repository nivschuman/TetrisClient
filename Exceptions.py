class IllegalActionException(Exception):
    def __init__(self, message="Cannot perform action"):
        super().__init__(message)


class CannotMoveException(IllegalActionException):
    def __init__(self, move_type="there"):
        super().__init__("Tetrino cannot move " + move_type)


class CannotRotateExceptions(IllegalActionException):
    def __init__(self, degree):
        super().__init__("Tetrino cannot rotate to " + str(degree) + " degrees")
