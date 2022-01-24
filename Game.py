import pygame
from Graphics import Graphics
from Board import Board
from Exceptions import IllegalActionException
import threading
from Server import Server
from Text import Text


class Game:
    BOARD_X = 80
    BOARD_Y = 850
    SERVER = Server.get_server()

    def __init__(self):
        self.__graphics = Graphics()
        self.__board = Board(10, 20, 40)

    def main_menu(self):
        text1 = Text("create game", 90, (255, 255, 255))
        text2 = Text("join game", 120, (255, 255, 255))
        create_btn = self.__graphics.create_button(50, 350, 400, 200, (0, 0, 255), text1)
        join_btn = self.__graphics.create_button(900, 350, 400, 200, (255, 215, 0), text2)

        create_btn.show()
        join_btn.show()

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        x, y = pygame.mouse.get_pos()
                        if create_btn.check_clicked(x, y):
                            create_btn.hide()
                            join_btn.hide()
                            running = False
                            self.create_game()
                        elif join_btn.check_clicked(x, y):
                            create_btn.hide()
                            join_btn.hide()
                            running = False
                            self.join_game()

    def start(self):
        t1 = threading.Thread(target=Game.play_song)
        t1.start()
        Game.SERVER.update_board(self.__board.board)
        t2 = threading.Thread(target=self.show_others)
        t2.start()
        running = True
        self.__graphics.draw_board(Game.BOARD_X, Game.BOARD_Y, self.__board.board, self.__board.block_sizes)
        pygame.time.set_timer(pygame.USEREVENT, 500)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    try:
                        cleared = 0
                        if event.key == pygame.K_d:
                            cleared = self.__board.move_piece("right")
                        elif event.key == pygame.K_a:
                            cleared = self.__board.move_piece("left")
                        elif event.key == pygame.K_LEFT:
                            self.__board.rotate_piece("left")
                        elif event.key == pygame.K_RIGHT:
                            self.__board.rotate_piece("right")
                        elif event.key == pygame.K_SPACE:
                            cleared = self.__board.move_piece("drop")
                        self.__graphics.draw_board(Game.BOARD_X, Game.BOARD_Y, self.__board.board, self.__board.block_sizes)
                        Game.SERVER.get_server().update_board(self.__board.board)

                        Game.send_attack(cleared)
                    except IllegalActionException as e:
                        print(e)

                if event.type == pygame.USEREVENT:
                    cleared = self.__board.move_piece("down")
                    self.__graphics.draw_board(Game.BOARD_X, Game.BOARD_Y, self.__board.board, self.__board.block_sizes)
                    Game.SERVER.update_board(self.__board.board)

                    Game.send_attack(cleared)

                if not self.__board.playable:
                    Game.SERVER.update_board(None)
                    running = False

        while True:
            pygame.event.pump()

    def show_others(self):
        while True:
            status = Game.SERVER.get_status()
            boards = status[0]
            start_x = Game.BOARD_X + 450
            x = start_x
            y = Game.BOARD_Y + 30
            for k in range(len(boards)):
                board = boards[k]

                if board is None:
                    continue

                self.__graphics.draw_board(x, y, board, 10)

                if k % 4 == 0 and k != 0:
                    x = start_x
                    y -= 250
                else:
                    x += 150

            attack = status[1]
            if attack != 0 and self.__board.playable:
                self.__board.add_lines(attack)
                self.__graphics.draw_board(Game.BOARD_X, Game.BOARD_Y, self.__board.board, self.__board.block_sizes)

    def create_game(self):
        pin = Game.SERVER.create_game()
        pin_text = Text(pin, 50, (255, 255, 255))
        pin_label = self.__graphics.create_label(50, 50, pin_text)
        pin_label.show()

        while len(Game.SERVER.get_status()[0]) < 1:
            pass

        self.start()

    def join_game(self):
        text_box = self.__graphics.create_text_box(300, 400, 700, 100, (255, 255, 255), 56, (0, 0, 0))
        text_box.show()

        label = self.__graphics.create_label(300, 350, Text("Enter pin", 56, (255, 255, 255)))
        label.show()

        btn = self.__graphics.create_button(400, 600, 500, 100, (0, 0, 255), Text("Join", 56, (0, 0, 0)))
        btn.show()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        x, y = pygame.mouse.get_pos()
                        text_box.check_clicked(x, y)
                        if btn.check_clicked(x, y):
                            joined = Game.SERVER.join_game(text_box.text.text)
                            if joined:
                                running = False
                                break
                if event.type == pygame.KEYDOWN:
                    if text_box.activated:
                        if event.key == pygame.K_BACKSPACE:
                            text_box.delete_text(1)
                        elif event.key == pygame.K_DELETE:
                            text_length = len(text_box.text.text)
                            text_box.delete_text(text_length)
                        elif event.key == pygame.K_SPACE:
                            text_box.add_text(" ")
                        elif event.key == pygame.K_RETURN:
                            text_box.activated = False
                        elif event.key == pygame.K_LEFT:
                            text_box.move_left()
                        elif event.key == pygame.K_RIGHT:
                            text_box.move_right()
                        elif event.key == pygame.K_CAPSLOCK:
                            text_box.change_caps_lock_state()
                        else:
                            key_name = pygame.key.name(event.key)
                            text_box.add_text(key_name)

        text_box.hide()
        btn.hide()
        label.hide()

        pin = Server.get_server().pin
        pin_text = Text(pin, 50, (255, 255, 255))
        pin_label = self.__graphics.create_label(50, 50, pin_text)
        pin_label.show()

        while len(Game.SERVER.get_status()[0]) < 1:
            pass

        self.start()

    @staticmethod
    def send_attack(lines_cleared):
        if lines_cleared == 2:
            Game.SERVER.attack(1)
        elif lines_cleared == 3:
            Game.SERVER.attack(2)
        elif lines_cleared >= 4:
            Game.SERVER.attack(4)

    @staticmethod
    def play_song():
        while True:
            sound_obj = pygame.mixer.Sound("Sounds/TetrisSong.mp3")
            playing = sound_obj.play()
            while playing.get_busy():
                pygame.time.wait(100)
