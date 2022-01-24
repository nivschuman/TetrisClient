import pygame
import threading
from Text import Text


class Graphics:
    BACKGROUND_RGB = (0, 0, 0)

    def __init__(self):
        pygame.init()
        sizes = pygame.display.Info()
        w = sizes.current_w
        h = sizes.current_h
        self.__screen = pygame.display.set_mode((w, h))
        self.__screen.fill(Graphics.BACKGROUND_RGB)
        pygame.display.update()

    def create_button(self, x, y, width, height, rgb, text):
        return Graphics.Button(x, y, width, height, rgb, text, self.__screen)

    def create_label(self, x, y, text):
        return Graphics.Label(x, y, text, self.__screen)

    def create_text_box(self, x, y, width, height, rgb, text_font, text_color):
        return Graphics.TextBox(x, y, width, height, rgb, text_font, text_color, self.__screen)

    def draw_board(self, start_x, start_y, board, block_sizes, update=True):
        self.clear_board(start_x, start_y, board, block_sizes, False)
        # top left corner
        x = start_x
        y = start_y
        size = block_sizes

        for col in board:
            first_x1 = x
            for row in col:
                if row == 0:
                    pygame.draw.rect(self.__screen, (255, 255, 255), pygame.Rect(x, y, size, size), 2)
                elif row == 1:
                    pygame.draw.rect(self.__screen, (152, 153, 155), pygame.Rect(x, y, size, size))
                elif row == 2:
                    pygame.draw.rect(self.__screen, (0, 253, 0), pygame.Rect(x, y, size, size))
                elif row == 3:
                    pygame.draw.rect(self.__screen, (221, 0, 0), pygame.Rect(x, y, size, size))

                x = x+block_sizes

            y -= block_sizes
            x = first_x1

        if update:
            pygame.display.update()

    def clear_screen(self, update=True):
        self.__screen.fill(Graphics.BACKGROUND_RGB)

        if update:
            pygame.display.update()

    def clear_board(self, start_x, start_y, board, block_sizes, update=True):
        width = len(board) * block_sizes
        length = len(board[0]) * block_sizes
        top_left_x = start_x
        top_left_y = start_y - width + block_sizes

        pygame.draw.rect(self.__screen, Graphics.BACKGROUND_RGB, pygame.Rect(top_left_x, top_left_y, length, width))

        if update:
            pygame.display.update()

    class Label:
        def __init__(self, x, y, text, screen):
            self.__x = x
            self.__y = y
            self.__text = text
            self.__screen = screen

        @property
        def x(self):
            return self.__x

        @x.setter
        def x(self, value):
            self.hide(False)
            self.__x = value
            self.show()

        @property
        def y(self):
            return self.__y

        @y.setter
        def y(self, value):
            self.hide(False)
            self.__y = value
            self.show()

        @property
        def text(self):
            return self.__text

        @text.setter
        def text(self, value):
            self.hide(False)
            self.__text = value
            self.show()

        def hide(self, update=True):
            font = pygame.font.SysFont(None, self.__text.font_size)
            img = font.render(self.__text.text, True, Graphics.BACKGROUND_RGB)

            for k in range(15):
                self.__screen.blit(img, (self.__x, self.__y))

            if update:
                pygame.display.update()

        def show(self, update=True):
            font = pygame.font.SysFont(None, self.__text.font_size)
            img = font.render(self.__text.text, True, self.__text.color)
            self.__screen.blit(img, (self.__x, self.__y))

            if update:
                pygame.display.update()

    class Button:
        def __init__(self, x, y, width, height, rgb, text, screen):
            self._rect = pygame.Rect(x, y, width, height)
            self._rgb = rgb

            self._hidden = True

            self._clicks = 0

            self._text = text

            self._screen = screen

        @property
        def clicks(self):
            return self._clicks

        @property
        def text(self):
            return self._text

        @text.setter
        def text(self, value):
            self.hide(False)
            self._text = value
            self.show()

        def show(self, update=True):
            pygame.draw.rect(self._screen, self._rgb, self._rect)

            font = pygame.font.SysFont(None, self._text.font_size)
            img = font.render(self._text.text, True, self._text.color)

            self._screen.blit(img, (self._rect.x, self._rect.y))

            if update:
                pygame.display.update()

            self._hidden = False

        def hide(self, update=True):
            pygame.draw.rect(self._screen, Graphics.BACKGROUND_RGB, self._rect)

            if update:
                pygame.display.update()
            self._hidden = True

        def check_clicked(self, x, y):
            if self._rect.collidepoint(x, y):
                self._clicks += 1
                return True

            return False

    class TextBox(Button):
        def __init__(self, x, y, width, height, rgb, text_font, text_color, screen):
            super().__init__(x, y, width, height, rgb, Text("", text_font, text_color), screen)

            self.__activated = False
            self.__caps_lock_on = False

            self.__bar_idx = -1  # index of |

        @property
        def activated(self):
            return self.__activated

        @activated.setter
        def activated(self, value):
            self.__activated = value

            if self.__activated:
                self.__activate()
            else:
                self.__deactivate()

        @property
        def caps_lock_on(self):
            return self.__caps_lock_on

        @caps_lock_on.setter
        def caps_lock_on(self, value):
            self.__caps_lock_on = value

        def move_left(self):
            if self.__activated and self.__bar_idx != 0:
                new_text = self.text.text[:self.__bar_idx] + self.text.text[self.__bar_idx+1:]
                self.__bar_idx -= 1
                new_text = new_text[:self.__bar_idx] + "|" + new_text[self.__bar_idx:]

                self.text = Text(new_text, self.text.font_size, self.text.color)

        def move_right(self):
            if self.__activated and self.__bar_idx != len(self.text.text)-1:
                new_text = self.text.text[:self.__bar_idx] + self.text.text[self.__bar_idx + 1:]
                self.__bar_idx += 1
                new_text = new_text[:self.__bar_idx] + "|" + new_text[self.__bar_idx:]

                self.text = Text(new_text, self.text.font_size, self.text.color)

        def add_text(self, text):
            if self.__activated:
                if self.__caps_lock_on:
                    text = text.upper()

                new_text = self.text.text[:self.__bar_idx] + text + self.text.text[self.__bar_idx:]
                self.text = Text(new_text, self.text.font_size, self.text.color)
                self.__bar_idx += len(text)

        def delete_text(self, amount):
            new_text = ""
            if amount < len(self.text.text):
                new_text = self.text.text[:self.__bar_idx-amount] + self.text.text[self.__bar_idx:]
                self.__bar_idx -= amount
            else:
                new_text = "|"
                self.__bar_idx = 0

            self.text = Text(new_text, self.text.font_size, self.text.color)

        def check_clicked(self, x, y):
            if self._rect.collidepoint(x, y):
                self._clicks += 1
                self.activated = False if self.__activated else True

                return True

            return False

        def change_caps_lock_state(self):
            if self.__caps_lock_on:
                self.__caps_lock_on = False
            else:
                self.__caps_lock_on = True

        def __activate(self):
            new_text = self.text.text + "|"
            self.__bar_idx = len(new_text) - 1
            self.text = Text(new_text, self.text.font_size, self.text.color)

        def __deactivate(self):
            new_text = self.text.text[:self.__bar_idx] + self.text.text[self.__bar_idx+1:]
            self.__bar_idx -= 1
            self.text = Text(new_text, self.text.font_size, self.text.color)
