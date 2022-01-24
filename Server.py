import socket


class Server:
    __instance = None

    @staticmethod
    def get_server():
        if Server.__instance is None:
            Server.__instance = Server()

        return Server.__instance

    def __init__(self):
        self.__header = 10
        self.__port = 5050
        self.__server = "54.167.236.170"
        self.__addr = (self.__server, self.__port)
        self.__format = "utf-8"
        self.__disconnect_message = "DISCONNECT"

        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__client.connect(self.__addr)

        self.__pin = None

    @property
    def pin(self):
        return self.__pin

    def create_game(self):
        self.__send("CREATEGAME")
        self.__pin = self.__receive()

        return self.__pin

    def join_game(self, pin):
        self.__send("JOINGAME")
        self.__send(pin)

        boolean = self.__receive()

        joined = True if boolean == "True" else False

        if joined:
            self.__pin = pin

        return joined

    def update_board(self, board):
        if self.__pin is None:
            raise Server.NotInGameException()

        self.__send("UPDATEBOARD")
        self.__send(Server.board_to_str(board))

    def get_status(self):
        if self.__pin is None:
            raise Server.NotInGameException()

        boards = []

        for k in range(int(self.__receive())):
            board = self.__receive()
            boards.append(Server.retrieve_board(board))

        attack = int(self.__receive())

        return boards, attack

    def attack(self, strength):
        if self.__pin is None:
            raise Server.NotInGameException()

        self.__send("ATTACK")
        self.__send(str(strength))

    def __send(self, msg):
        message = msg.encode(self.__format)
        msg_length = len(message)
        send_length = str(msg_length).encode(self.__format)
        send_length += b' ' * (self.__header - len(send_length))
        self.__client.send(send_length)
        self.__client.send(message)

    def __receive(self):
        msg_length = self.__client.recv(self.__header).decode(self.__format)
        if msg_length:
            msg_length = int(msg_length)
            return self.__client.recv(msg_length).decode(self.__format)

    @staticmethod
    def board_to_str(board):
        if board is None:
            return "None"

        board_str = ""
        for i in range(len(board)):
            for item in board[i]:
                board_str += str(item)

            if i != len(board)-1:
                board_str += "*"

        return board_str

    # todo deal with ValueError: invalid literal for int() with base 10: 'N'
    @staticmethod
    def retrieve_board(board_str):
        if board_str == "None":
            return None

        board = []
        for item in board_str.split("*"):
            col = []
            for char in item:
                col.append(int(char))

            board.append(col)

        return board

    class NotInGameException(Exception):
        def __init__(self):
            super().__init__("Server is not connected to game")
